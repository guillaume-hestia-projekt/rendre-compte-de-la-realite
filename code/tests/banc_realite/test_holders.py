"""Tests hors ligne — mode présence verbatim / valeur."""
from __future__ import annotations

from banc_realite.fidelite import load_gold
from banc_realite.holders import classify_pair, discriminants


def _assertion(*, quote: str, source: str = "documents/piece-a.md") -> dict:
    return {
        "id": "a-test",
        "source": source,
        "quote": quote,
        "content": quote,
    }


def _file_element(*, text: str, source: str = "documents/piece-a.md") -> dict:
    return {
        "kind": "file_hit",
        "id": "f1",
        "text": text,
        "source": source,
    }


def test_verbatim_paraphrase_non():
    assertion = _assertion(quote="somme de 1 720,00 euros bruts")
    element = _file_element(text="montant revendique de 1720,00 euros sur la periode")
    assert classify_pair(assertion, element, {}, mode_presence="verbatim") == "non"


def test_valeur_paraphrase_same_piece_tient():
    assertion = _assertion(quote="somme de 1 720,00 euros bruts")
    element = _file_element(text="montant revendique de 1720,00 euros sur la periode")
    assert classify_pair(assertion, element, {}, mode_presence="valeur") == "tient"


def test_valeur_paraphrase_wrong_piece_non():
    assertion = _assertion(quote="somme de 1 720,00 euros bruts")
    element = _file_element(
        text="montant revendique de 1720,00 euros sur la periode",
        source="documents/piece-b.md",
    )
    assert classify_pair(assertion, element, {}, mode_presence="valeur") == "non"


def test_valeur_86_not_in_1986():
    assertion = _assertion(quote="total revendique 86 heures")
    element = _file_element(text="reference interne 1986 pour archivage")
    assert classify_pair(assertion, element, {}, mode_presence="valeur") == "non"


def test_valeur_number_formats():
    assertion = _assertion(quote="montant de 1 720 €")
    assert (
        classify_pair(assertion, _file_element(text="solde 1720,00 EUR"), {}, mode_presence="valeur")
        == "tient"
    )
    assert (
        classify_pair(assertion, _file_element(text="total 1 720 euros"), {}, mode_presence="valeur")
        == "tient"
    )
    assert classify_pair(assertion, _file_element(text="solde 1720,00"), {}, mode_presence="valeur") == "non"


def test_valeur_percent_anchored_not_bare_number():
    assertion = _assertion(quote="The annual fee is 3 percent")
    assert (
        classify_pair(
            assertion,
            _file_element(text="Appendix 3 describes another subject"),
            {},
            mode_presence="valeur",
        )
        == "non"
    )
    assert (
        classify_pair(
            assertion,
            _file_element(text="frais annuels de 3 %"),
            {},
            mode_presence="valeur",
        )
        == "tient"
    )


def test_valeur_lexical_note_not_application():
    assertion = _assertion(quote="No bank statement accompanies this note.")
    assert (
        classify_pair(
            assertion,
            _file_element(text="No bank statement accompanies this application."),
            {},
            mode_presence="valeur",
        )
        == "non"
    )
    assert (
        classify_pair(
            assertion,
            _file_element(text="No bank statement accompanies this note in the file."),
            {},
            mode_presence="valeur",
        )
        == "tient"
    )


def test_valeur_reformulation_factuelle_chiffree():
    assertion = _assertion(quote="CA 2023 : 4,2 M€")
    element = _file_element(
        text="Le chiffre d affaires 2023 s eleve a 4,2 millions d euros sur l exercice"
    )
    assert classify_pair(assertion, element, {}, mode_presence="valeur") == "tient"


def test_valeur_date_formats():
    assertion = _assertion(quote="embauche a compter du 15 septembre 2019")
    assert (
        classify_pair(assertion, _file_element(text="date d entree 15/09/2019"), {}, mode_presence="valeur")
        == "tient"
    )
    assert (
        classify_pair(assertion, _file_element(text="debut contrat 2019-09-15"), {}, mode_presence="valeur")
        == "tient"
    )


def test_valeur_clause_sans_chiffre_repli_lexical():
    assertion = _assertion(
        quote="clause de non concurrence de deux ans apres depart du salarie"
    )
    sans_suite = _file_element(text="autre passage sans lien sur la meme piece")
    avec_suite = _file_element(
        text="la clause de non concurrence de deux ans s applique apres depart du salarie"
    )
    assert classify_pair(assertion, sans_suite, {}, mode_presence="valeur") == "non"
    assert classify_pair(assertion, avec_suite, {}, mode_presence="valeur") == "tient"


def test_discriminants_rg_est_texte():
    disc = discriminants("saisine du CPH le 5 mars 2024 (R.G. 24/01984)")
    assert "24/01984" in disc["textes"]
    number_values = [value for value, _anchor in disc["nombres"]]
    assert 24 not in number_values
    assert 1984 not in number_values


def test_invariant_valeur_contient_verbatim_sur_tout_or():
    ecarts: dict[str, int] = {"greenloop": 0, "moreau": 0}
    for dossier_name in ("greenloop", "moreau"):
        gold = load_gold(dossier_name)
        for assertion in gold["assertions"]:
            quote = str(assertion.get("quote") or assertion.get("content") or "")
            source = str(assertion.get("source") or "")
            element = _file_element(text=quote, source=source)
            if classify_pair(assertion, element, {}, mode_presence="verbatim") != "tient":
                continue
            if classify_pair(assertion, element, {}, mode_presence="valeur") != "tient":
                ecarts[dossier_name] += 1
    assert ecarts == {"greenloop": 0, "moreau": 0}


def test_valeur_tabular_row_anchoring():
    row = "| 2025-01 | Beacon Court | SITE-BC | 5 | 143.574 | 0.000 | 143.574 |"
    assertion = _assertion(
        quote=row,
        source="documents/17-collection-register.md",
    )
    same = _file_element(text=row, source="documents/17-collection-register.md")
    other = _file_element(
        text="| 2025-01 | Beacon Court | SITE-BC | 8 | 999.000 | 0.000 | 999.000 |",
        source="documents/17-collection-register.md",
    )
    assert classify_pair(assertion, same, {}, mode_presence="valeur") == "tient"
    assert classify_pair(assertion, other, {}, mode_presence="valeur") == "non"
