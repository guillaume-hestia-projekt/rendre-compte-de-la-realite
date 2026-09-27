"""Tests hors ligne — tiers_mem0 (sans import mem0 au chargement)."""
from __future__ import annotations

import json

import pytest

import banc_realite.tiers_mem0 as tm
from banc_realite.dossiers import dossier_courant


def test_a_blanc_compte_pieces_et_morceaux(monkeypatch, tmp_path):
    pieces = [tmp_path / "a.md", tmp_path / "b.md", tmp_path / "c.md"]
    for idx, piece in enumerate(pieces, 1):
        piece.write_text("para\n\n" + ("x" * 100 * idx), encoding="utf-8")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "q?"}] * 3)
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    payload = tm.estimer_a_blanc()
    assert payload["pieces"] == 3
    assert payload["appels_prevus"] >= 3
    assert payload["cout_ingestion_eur"] >= 0
    assert (tmp_path / "ingestion-mem0-mistral.a-blanc.json").is_file()


def test_decouper_piece_aux_paragraphes():
    long_para = "z" * 7000
    text = "intro\n\n" + long_para + "\n\nfin"
    parts = tm.decouper_piece(text)
    assert all(len(part) <= tm.MAX_MORCEAU_CHARS for part in parts)
    assert len(parts) >= 2


def test_contextes_format_elements(monkeypatch, tmp_path):
    captured: list[dict] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def search(self, query, *, filters, top_k):
            captured.append({"query": query, "user_id": filters["user_id"], "limit": top_k})
            return {
                "results": [
                    {"memory": "souvenir", "score": 0.9, "metadata": {"piece": "a.md"}},
                ]
            }

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr(
        "brain.adapters.mistral_embeddings.load_api_key",
        lambda api_key=None: "secret",
    )
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "question nue"}])
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr("banc_realite.fournisseurs_contexte.COMPARATIF_DIR", tmp_path)
    out = tm.contextes(k=5)
    assert out["status"] == "complete"
    lines = (tmp_path / "contextes-mem0.jsonl").read_text(encoding="utf-8").strip().split("\n")
    meta = json.loads(lines[0])["meta"]
    assert meta["k"] == 20
    assert captured[0]["limit"] == 5
    assert meta["extracteur"] == "mistral"
    assert meta["modele"] == "mistral-large-latest"
    row = json.loads(lines[1])
    assert row["question_id"] == "gl-q001"
    assert row["elements"][0]["source"] == "a.md"
    assert captured[0]["query"] == "question nue"


def test_ingerer_refuse_au_dessus_plafond(monkeypatch):
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 10.0},
    )
    with pytest.raises(RuntimeError, match="plafond"):
        tm.ingerer(executer=True, plafond_eur=1.0, extracteur="mistral")


def test_a_blanc_cursor_affiche_quota_cursor(monkeypatch, tmp_path):
    pieces = [tmp_path / "a.md"]
    pieces[0].write_text("x" * 100, encoding="utf-8")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "q?"}])
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    payload = tm.estimer_a_blanc(extracteur="cursor")
    assert payload["extracteur"] == "cursor"
    assert payload["cout_ingestion_eur"] is None
    assert payload["cout_total_eur"] is None
    assert payload["cout_contextes_eur"] >= 0
    assert payload["cout"].startswith("quota Cursor,")
    assert payload["modele_extraction"] == tm.CURSOR_MODEL


def test_contextes_conserve_k_demande(monkeypatch, tmp_path):
    captured: list[int] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def search(self, query, *, filters, top_k):
            captured.append(top_k)
            return {
                "results": [
                    {"memory": f"souvenir-{idx}", "score": 0.9, "metadata": {"piece": "a.md"}}
                    for idx in range(top_k)
                ]
            }

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr(
        "brain.adapters.mistral_embeddings.load_api_key",
        lambda api_key=None: "secret",
    )
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "question nue"}])
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr("banc_realite.fournisseurs_contexte.COMPARATIF_DIR", tmp_path)
    out = tm.contextes(k=25)
    assert out["status"] == "complete"
    assert captured == [25]
    lines = (tmp_path / "contextes-mem0-k25.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert json.loads(lines[0])["meta"]["k"] == 25
    row = json.loads(lines[1])
    assert len(row["elements"]) == 25


def test_build_memory_config_cursor_pointe_relais():
    config = tm._build_memory_config("secret", "mistral-large-latest", extracteur="cursor")
    assert config["llm"]["config"]["model"] == tm.CURSOR_MODEL
    assert config["llm"]["config"]["openai_base_url"] == tm.CURSOR_RELAY_BASE
    assert config["llm"]["config"]["api_key"] == "relais"
    assert config["embedder"]["config"]["model"] == "mistral-embed"
    assert config["embedder"]["config"]["openai_base_url"] == tm.MISTRAL_BASE


def test_contextes_accepte_results_vide(monkeypatch, tmp_path):
    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def search(self, query, *, filters, top_k):
            return {"results": []}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr(
        "brain.adapters.mistral_embeddings.load_api_key",
        lambda api_key=None: "secret",
    )
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "question nue"}])
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr("banc_realite.fournisseurs_contexte.COMPARATIF_DIR", tmp_path)
    out = tm.contextes(k=5)
    assert out["status"] == "complete"
    lines = (tmp_path / "contextes-mem0.jsonl").read_text(encoding="utf-8").strip().split("\n")
    row = json.loads(lines[1])
    assert row["elements"] == []


def test_ingerer_reprend_au_morceau(monkeypatch, tmp_path):
    pieces = [tmp_path / "piece-x.md"]
    pieces[0].write_text(("x" * 5000) + "\n\n" + ("y" * 5000), encoding="utf-8")
    chunks = tm.decouper_piece(pieces[0].read_text(encoding="utf-8"))
    assert len(chunks) == 2

    added: list[int] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def add(self, chunk, *, user_id, metadata):
            added.append(len(chunk))
            return {"results": [{"id": f"m{len(added)}"}]}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    journal_mistral = tmp_path / "appels-ingestion-mem0-mistral.jsonl"
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 0.01},
    )
    monkeypatch.setattr(tm, "compter_souvenirs_par_piece", lambda *a, **k: {})

    class FakeConn:
        autocommit = False

        def execute(self, *_args, **_kwargs):
            return None

        def close(self):
            return None

    monkeypatch.setattr("psycopg.connect", lambda *_args, **_kwargs: FakeConn())
    monkeypatch.setattr(tm, "_ensure_database", lambda _conn: None)
    monkeypatch.setattr(tm, "PAUSE_ENTRE_APPELS_S", 0)

    tm._journaliser(
        journal_mistral,
        {
            "fournisseur": "mem0",
            "extracteur": "mistral",
            "modele": "mistral-large-latest",
            "piece": "piece-x.md",
            "morceau": 0,
            "morceaux": len(chunks),
            "souvenirs": 1,
            "secondes": 0.1,
        },
    )

    tm.ingerer(executer=True, plafond_eur=10.0, extracteur="mistral")
    assert len(added) == 1


def test_ingerer_cursor_ne_saute_pas_morceau_journalise_par_mistral(monkeypatch, tmp_path):
    pieces = [tmp_path / "piece-x.md"]
    pieces[0].write_text(("x" * 5000) + "\n\n" + ("y" * 5000), encoding="utf-8")
    chunks = tm.decouper_piece(pieces[0].read_text(encoding="utf-8"))
    assert len(chunks) == 2

    added: list[int] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def add(self, chunk, *, user_id, metadata):
            added.append(len(chunk))
            return {"results": [{"id": f"m{len(added)}"}]}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 0.01},
    )
    monkeypatch.setattr(tm, "compter_souvenirs_par_piece", lambda *a, **k: {})

    class FakeConn:
        autocommit = False

        def execute(self, *_args, **_kwargs):
            return None

        def close(self):
            return None

    monkeypatch.setattr("psycopg.connect", lambda *_args, **_kwargs: FakeConn())
    monkeypatch.setattr(tm, "_ensure_database", lambda _conn: None)
    monkeypatch.setattr(tm, "PAUSE_ENTRE_APPELS_S", 0)

    tm._journaliser(
        tmp_path / "appels-ingestion-mem0-mistral.jsonl",
        {
            "fournisseur": "mem0",
            "extracteur": "mistral",
            "modele": "mistral-large-latest",
            "piece": "piece-x.md",
            "morceau": 0,
            "morceaux": len(chunks),
            "souvenirs": 1,
            "secondes": 0.1,
        },
    )

    tm.ingerer(executer=True, plafond_eur=10.0, extracteur="cursor")
    assert len(added) == 2


def test_build_memory_config_collection_par_extracteur():
    mistral = tm._build_memory_config(
        "secret", "mistral-large-latest", extracteur="mistral", dossier="greenloop"
    )
    cursor = tm._build_memory_config(
        "secret", "mistral-large-latest", extracteur="cursor", dossier="greenloop"
    )
    assert mistral["vector_store"]["config"]["collection_name"] == "mem0_greenloop_mistral_mistral_large_latest"
    assert cursor["vector_store"]["config"]["collection_name"] == "mem0_greenloop_cursor_mistral_large_latest"


def test_mem0_chemins_greenloop_inchange(monkeypatch, tmp_path):
    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    chemins = tm.Mem0Chemins(greenloop)
    assert chemins.racine == tmp_path
    assert chemins.journal_ingestion("cursor") == tmp_path / "appels-ingestion-mem0-cursor.jsonl"
    assert chemins.contextes_path == tmp_path / "contextes-mem0.jsonl"
    assert chemins.journal_contextes == tmp_path / "appels-contextes-mem0.jsonl"


def test_mem0_chemins_moreau(tmp_path):
    moreau = dossier_courant("moreau")
    chemins = tm.Mem0Chemins(moreau)
    assert chemins.racine == moreau.corpus_dir.parent / "mem0"
    assert chemins.journal_ingestion("cursor").name == "appels-ingestion-mem0.jsonl"
    assert chemins.contextes_path.name == "contextes-mem0.jsonl"


def test_build_memory_config_isolation_dossiers():
    gl = tm._build_memory_config(
        "secret", tm.CURSOR_MODEL, extracteur="cursor", dossier="greenloop"
    )
    mo = tm._build_memory_config(
        "secret", tm.CURSOR_MODEL, extracteur="cursor", dossier="moreau"
    )
    assert gl["vector_store"]["config"]["collection_name"] == "mem0_greenloop_cursor_cursor_grok_4_5_high"
    assert mo["vector_store"]["config"]["collection_name"] == "mem0_moreau_cursor_cursor_grok_4_5_high"


def test_ingerer_utilise_user_id_dossier(monkeypatch, tmp_path):
    pieces = [tmp_path / "piece-x.md"]
    pieces[0].write_text("contenu test", encoding="utf-8")
    captured: list[str] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def add(self, chunk, *, user_id, metadata):
            captured.append(user_id)
            return {"results": [{"id": "m1"}]}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    moreau = dossier_courant("moreau")
    mem0_root = tmp_path / "mem0"
    monkeypatch.setattr(
        tm.Mem0Chemins,
        "racine",
        property(lambda self: mem0_root if self.dossier.nom == "moreau" else tmp_path),
    )

    class FakeConn:
        autocommit = False

        def execute(self, *_args, **_kwargs):
            return None

        def close(self):
            return None

    monkeypatch.setattr("psycopg.connect", lambda *_args, **_kwargs: FakeConn())
    monkeypatch.setattr(tm, "_ensure_database", lambda _conn: None)
    monkeypatch.setattr(tm, "PAUSE_ENTRE_APPELS_S", 0)
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 0.01},
    )
    monkeypatch.setattr(tm, "compter_souvenirs_par_piece", lambda *a, **k: {})

    tm.ingerer(executer=True, plafond_eur=10.0, extracteur="mistral", dossier=moreau)
    assert captured == ["moreau"]


def test_plafond_arrete_ingestion(monkeypatch, tmp_path):
    pieces = [tmp_path / f"p{i}.md" for i in range(3)]
    for piece in pieces:
        piece.write_text("x" * 100, encoding="utf-8")

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def add(self, chunk, *, user_id, metadata):
            return {"results": [{"id": "m1"}]}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    mem0_root = tmp_path / "mem0"
    monkeypatch.setattr(
        tm.Mem0Chemins,
        "racine",
        property(lambda self: mem0_root if self.dossier.nom == "moreau" else tmp_path),
    )
    monkeypatch.setattr(tm, "MOREAU_MAX_EXTRACTION", 1)
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 0.01},
    )
    monkeypatch.setattr(tm, "compter_souvenirs_par_piece", lambda *a, **k: {})

    class FakeConn:
        autocommit = False

        def execute(self, *_args, **_kwargs):
            return None

        def close(self):
            return None

    monkeypatch.setattr("psycopg.connect", lambda *_args, **_kwargs: FakeConn())
    monkeypatch.setattr(tm, "_ensure_database", lambda _conn: None)
    monkeypatch.setattr(tm, "PAUSE_ENTRE_APPELS_S", 0)

    out = tm.ingerer(executer=True, plafond_eur=10.0, extracteur="cursor", dossier="moreau")
    assert out["status"] == "arret"
    assert out["cause"] == "plafond_appels_extraction"


def test_build_memory_config_mistral_inchange():
    config = tm._build_memory_config("secret", "mistral-large-latest", extracteur="mistral")
    assert config["llm"]["config"]["model"] == "mistral-large-latest"
    assert config["llm"]["config"]["openai_base_url"] == tm.MISTRAL_BASE


def test_contextes_refuse_ecrasement_autre_extracteur(monkeypatch, tmp_path):
    out_path = tmp_path / "contextes-mem0.jsonl"
    out_path.write_text(
        json.dumps({"meta": {"k": 5, "extracteur": "mistral", "modele": "mistral-large-latest"}}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr(
        "banc_realite.fournisseurs_contexte.COMPARATIF_DIR",
        tmp_path,
    )
    with pytest.raises(RuntimeError, match="refus d'écraser"):
        tm.contextes(k=5, extracteur="cursor")


def test_ingerer_bilan_agrege_usage_morceaux_repris(monkeypatch, tmp_path):
    pieces = [tmp_path / "piece-x.md"]
    pieces[0].write_text(("x" * 5000) + "\n\n" + ("y" * 5000), encoding="utf-8")
    chunks = tm.decouper_piece(pieces[0].read_text(encoding="utf-8"))
    assert len(chunks) == 2

    added: list[int] = []

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def add(self, chunk, *, user_id, metadata):
            added.append(len(chunk))
            return {
                "results": [{"id": f"m{len(added)}"}],
                "usage": {"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60},
            }

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "lister_pieces", lambda dossier=None: pieces)
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    journal_mistral = tmp_path / "appels-ingestion-mem0-mistral.jsonl"
    monkeypatch.setattr(
        tm,
        "estimer_a_blanc",
        lambda **kwargs: {"cout_ingestion_eur": 0.01},
    )
    monkeypatch.setattr(tm, "compter_souvenirs_par_piece", lambda *a, **k: {})

    class FakeConn:
        autocommit = False

        def execute(self, *_args, **_kwargs):
            return None

        def close(self):
            return None

    monkeypatch.setattr("psycopg.connect", lambda *_args, **_kwargs: FakeConn())
    monkeypatch.setattr(tm, "_ensure_database", lambda _conn: None)
    monkeypatch.setattr(tm, "PAUSE_ENTRE_APPELS_S", 0)

    tm._journaliser(
        journal_mistral,
        {
            "fournisseur": "mem0",
            "extracteur": "mistral",
            "modele": "mistral-large-latest",
            "piece": "piece-x.md",
            "morceau": 0,
            "morceaux": len(chunks),
            "souvenirs": 1,
            "usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120},
            "secondes": 0.1,
        },
    )

    tm.ingerer(executer=True, plafond_eur=10.0, extracteur="mistral")
    assert len(added) == 1
    bilan = [
        json.loads(line)
        for line in journal_mistral.read_text(encoding="utf-8").splitlines()
        if json.loads(line).get("bilan")
    ][0]
    assert bilan["usage"]["total_tokens"] == 180
