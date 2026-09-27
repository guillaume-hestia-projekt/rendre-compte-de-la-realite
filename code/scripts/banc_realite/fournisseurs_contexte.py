"""Adaptateurs fournisseurs de contexte pour le banc comparatif étage 2."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from brain.call_frame import _build_structured_query, _render_markdown_with_budget

from .config import BANC_ROOT, SORTIES
from .dossiers import Dossier, dossier_courant
from .couche_brute_search import search_passages_hybrid
from .etage3_config_gagnante import CONFIGURATIONS as ETAGE3_CONFIGS
from .etage3 import compile_cadre_prod
from .measure_etage2 import _load_embed_cache, cached_embed_factory
from .mesure_porte_phrase import build_evidence_for_porte_phrase_config
from .porte_voisinage import enrichir_porte_voisinage

COMPARATIF_DIR = BANC_ROOT / "sorties" / "comparatif"


@runtime_checkable
class FournisseurContexte(Protocol):
    etiquette: str

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        ...


def _conversation_state(dossier: Dossier | None = None) -> dict[str, Any]:
    current = dossier if dossier is not None else dossier_courant()
    return {"responsibility_context": current.responsibility_context}


def _require_question_vector(question: dict[str, Any], embed_cache: dict[str, list[float]]) -> list[float]:
    text = question["question"]
    if text not in embed_cache:
        raise RuntimeError(f"cache froid : embedding absent ({text[:60]}…)")
    return embed_cache[text]


def _elements_to_evidence(elements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in elements:
        rank = int(item.get("rank") or len(out) + 1)
        source = item.get("source") or ""
        out.append(
            {
                "kind": "file_hit",
                "memory_type": "semantic",
                "id": f"{source}:{rank}",
                "score": float(item.get("score") or 0.0),
                "rank": rank,
                "text": item.get("text") or "",
                "source": source,
                "snippet": (item.get("text") or "")[:280],
                "payload": {"metadata": item.get("provenance") or {}},
                "provenance": item.get("provenance") or {"source_file_path": source},
            }
        )
    return out


def _source_etiquette(item: dict[str, Any]) -> str:
    source = str(item.get("source") or "").strip()
    if not source:
        provenance = item.get("provenance") or {}
        source = str(provenance.get("source_file_path") or "").strip()
    return source or "source inconnue"


def _render_texte_simple(elements: list[dict[str, Any]], *, budget_chars: int) -> tuple[str, list[dict[str, Any]]]:
    kept = list(elements)
    while kept:
        rendered = "\n\n".join(
            f"- [{_source_etiquette(item)}] {item.get('text') or ''}" for item in kept
        ).strip()
        if len(rendered) <= budget_chars:
            return rendered, kept
        kept.pop()
    return "", []


def rendre_contexte(
    elements: list[dict[str, Any]],
    *,
    budget_chars: int,
    question_id: str = "banc-comparatif",
    style: str = "brain",
    dossier: Dossier | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Rendu texte + éléments gardés sous le budget caractères."""
    current = dossier if dossier is not None else dossier_courant()
    if style == "brain":
        rendered, dropped = _render_markdown_with_budget(
            "banc-realite",
            current.responsibility_context,
            f"banc-comparatif-{question_id}",
            None,
            _conversation_state(current),
            elements,
            None,
            max_chars=budget_chars,
        )
        kept = elements[: max(len(elements) - dropped, 0)]
        return rendered, kept
    return _render_texte_simple(elements, budget_chars=budget_chars)


class RagNaif:
    etiquette = "rag_naif"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        qtext = question["question"]
        vector = _require_question_vector(question, self._embed_cache)
        structured = _build_structured_query(
            qtext,
            self._dossier.responsibility_context,
            {"responsibility_context": self._dossier.responsibility_context},
        )
        return search_passages_hybrid(
            connection,
            structured,
            query_vector=vector,
            top_k=k,
            vault_ref=self._dossier.vault_ref,
        )


class BrainProd:
    etiquette = "brain_prod"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del connection
        _require_question_vector(question, self._embed_cache)
        cadre = compile_cadre_prod(
            question,
            top_k=k,
            embed_cache=self._embed_cache,
            dossier=self._dossier,
        )
        return list(cadre.get("evidence") or [])


class BrainBanc:
    etiquette = "brain_banc"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g12"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return evidence


class BrainBancG24:
    etiquette = "brain_banc_g24"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g24"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return evidence


class BrainBancG48:
    etiquette = "brain_banc_g48"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g48"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return evidence


class BrainBancG36:
    etiquette = "brain_banc_g36"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g36"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return evidence


class BrainBancV1:
    etiquette = "brain_banc_v1"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g12"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return enrichir_porte_voisinage(
            evidence,
            connection=connection,
            vault_ref=self._dossier.vault_ref,
            arêtes=1,
        )


class BrainBancV3:
    etiquette = "brain_banc_v3"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g12"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return enrichir_porte_voisinage(
            evidence,
            connection=connection,
            vault_ref=self._dossier.vault_ref,
            arêtes=1,
            rendu="phrase",
            question=question,
        )


class BrainBancV4:
    etiquette = "brain_banc_v4"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g12"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return enrichir_porte_voisinage(
            evidence,
            connection=connection,
            vault_ref=self._dossier.vault_ref,
            arêtes=2,
            rendu="phrase",
            question=question,
        )


class BrainBancV2:
    etiquette = "brain_banc_v2"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        self._config = ETAGE3_CONFIGS["hybride_fenetres_g12"]["porte_phrase_config"]

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return enrichir_porte_voisinage(
            evidence,
            connection=connection,
            vault_ref=self._dossier.vault_ref,
            arêtes=2,
        )


class BrainBancCalibre:
    etiquette = "brain_banc_calibre"

    def __init__(
        self,
        embed_cache: dict[str, list[float]] | None = None,
        phrases_cache: dict[str, list[float]] | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self._dossier = dossier if dossier is not None else dossier_courant()
        self._embed_cache = (
            embed_cache if embed_cache is not None else _load_embed_cache(self._dossier)
        )
        self._phrases_cache = phrases_cache
        from .embarquer_phrases import load_fenetre_calibree

        meta = load_fenetre_calibree(self._dossier)
        self._config = json.loads(
            json.dumps(ETAGE3_CONFIGS["hybride_fenetres_calibrees"]["porte_phrase_config"])
        )
        self._config["phrases"]["fenetre"] = int(meta["fenetre_phrases"])

    def _phrases(self) -> dict[str, list[float]]:
        if self._phrases_cache is not None:
            return self._phrases_cache
        cache_path = self._dossier.cache_phrases_embeddings_calibrees
        if not cache_path.is_file():
            raise RuntimeError(f"cache unités calibrées absent : {cache_path}")
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if not payload:
            raise RuntimeError(f"cache unités calibrées vide : {cache_path}")
        self._phrases_cache = payload
        return payload

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del k
        _require_question_vector(question, self._embed_cache)
        evidence, _brute, _stats = build_evidence_for_porte_phrase_config(
            connection,
            question,
            self._config,
            embed_cache=self._embed_cache,
            phrases_cache=self._phrases(),
            dossier=self._dossier,
        )
        return evidence


class FournisseurFichier:
    def __init__(
        self,
        etiquette: str,
        chemin: Path | str | None = None,
        *,
        dossier: Dossier | None = None,
    ) -> None:
        self.etiquette = etiquette
        if etiquette == "mem0":
            if chemin is not None:
                raise ValueError("mem0 résout son fichier par k — ne pas passer chemin")
            self.chemin = None
        else:
            if chemin is None:
                raise ValueError(f"chemin requis pour {etiquette}")
            self.chemin = Path(chemin)
        self._dossier = dossier
        self._index_by_path: dict[Path, dict[str, list[dict[str, Any]]]] = {}
        self._k_max_by_path: dict[Path, int] = {}
        self._meta_by_path: dict[Path, dict[str, Any]] = {}

    def _exiger_prefixe_dossier(self, question_ids: list[str]) -> None:
        if self._dossier is None or self._dossier.nom == "greenloop":
            return
        prefix = self._dossier.prefixe_question
        invalid = sorted(qid for qid in question_ids if not str(qid).startswith(prefix))
        if invalid:
            raise ValueError(
                f"contextes {self.etiquette} incohérents pour dossier {self._dossier.nom!r} : "
                f"préfixe attendu {prefix!r}, trouvé sur {invalid[:3]}"
                f"{'…' if len(invalid) > 3 else ''} dans {self.chemin}"
            )

    def _chemin_pour_k(self, k: int) -> Path:
        if self.etiquette == "mem0":
            from .tiers_mem0 import comparatif_context_path as mem0_context_path

            return mem0_context_path("mem0", dossier=self._dossier, k=k)
        assert self.chemin is not None
        return self.chemin

    @property
    def meta(self) -> dict[str, Any]:
        chemin = self._chemin_pour_k(20)
        self._load(chemin)
        return dict(self._meta_by_path.get(chemin) or {})

    def ensure_fichiers(self, ks: list[int]) -> None:
        fichiers = {self._chemin_pour_k(k) for k in ks}
        for chemin in fichiers:
            self._load(chemin)

    def _load(self, chemin: Path | None = None) -> dict[str, list[dict[str, Any]]]:
        if chemin is None:
            chemin = self._chemin_pour_k(20) if self.etiquette == "mem0" else self.chemin
        assert chemin is not None
        if chemin in self._index_by_path:
            return self._index_by_path[chemin]
        # Un fichier absent ou une question manquante est une mesure fausse (contexte vide
        # compté comme un vrai zéro) : on refuse, on ne devine pas (revue Codex #123).
        if not chemin.is_file():
            raise FileNotFoundError(
                f"contextes {self.etiquette} absents pour k demandé : {chemin} — "
                f"lancer `tiers_mem0.py contextes --k …` d'abord"
            )
        index: dict[str, list[dict[str, Any]]] = {}
        k_max = 20
        meta: dict[str, Any] = {}
        lines = [line for line in chemin.read_text(encoding="utf-8").splitlines() if line.strip()]
        start = 0
        if lines:
            first = json.loads(lines[0])
            if "meta" in first:
                meta = dict(first["meta"])
                k_max = int(meta.get("k") or 20)
                start = 1
        for line in lines[start:]:
            row = json.loads(line)
            index[str(row["question_id"])] = list(row.get("elements") or [])
        self._exiger_prefixe_dossier(list(index))
        self._k_max_by_path[chemin] = k_max
        self._meta_by_path[chemin] = meta
        self._index_by_path[chemin] = index
        return index

    def contexte(self, question: dict[str, Any], *, k: int, connection) -> list[dict[str, Any]]:
        del connection
        chemin = self._chemin_pour_k(k)
        index = self._load(chemin)
        self._exiger_prefixe_dossier([str(question["id"])])
        k_max = self._k_max_by_path[chemin]
        if k > k_max:
            raise ValueError(
                f"contextes {self.etiquette} : k={k} > k_max={k_max} dans {chemin}"
            )
        if question["id"] not in index:
            raise KeyError(
                f"contextes {self.etiquette} incomplets : {question['id']} absent de {chemin}"
            )
        return _elements_to_evidence(index[question["id"]][:k])


def missing_embed_texts(questions: list[dict[str, Any]], embed_cache: dict[str, list[float]]) -> list[str]:
    return sorted(q["question"] for q in questions if q["question"] not in embed_cache)


def embed_factory_or_raise(
    embed_cache: dict[str, list[float]] | None = None,
    *,
    dossier: Dossier | None = None,
):
    cache = embed_cache if embed_cache is not None else _load_embed_cache(dossier)
    return cached_embed_factory(cache), cache


def comparatif_context_path(
    etiquette: str,
    dossier: Dossier | None = None,
    *,
    k: int = 20,
) -> Path:
    current = dossier if dossier is not None else dossier_courant()
    if etiquette == "mem0":
        from .tiers_mem0 import comparatif_context_path as mem0_context_path

        return mem0_context_path(etiquette, dossier=current, k=k)
    return current.comparatif_dir / f"contextes-{etiquette}.jsonl"


def default_sorties_path(dossier: Dossier | None = None) -> Path:
    current = dossier if dossier is not None else dossier_courant()
    return current.cache_embeddings_questions
