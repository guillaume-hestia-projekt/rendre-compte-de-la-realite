"""Tri déterministe dispute / trajectoire — cinq issues."""

from banc_realite.classer_couple import classer_couple, normaliser_quantite


def _fait(
    *,
    entity_id: str = "ent-site-a",
    attribute_id: str = "attr-collections",
    value: str = "12",
    qualifiers: dict | None = None,
) -> dict:
    quals = {"attribute_id": attribute_id}
    if qualifiers:
        quals.update(qualifiers)
    return {
        "entity_id": entity_id,
        "value": value,
        "qualifiers": quals,
    }


def test_classer_couple_accord():
    a = _fait(value="657 collections", qualifiers={"period": "2024-01"})
    b = _fait(value="657", qualifiers={"period": "2024-01"})
    out = classer_couple(a, b)
    assert out["issue"] == "accord"
    assert out["raison"]


def test_classer_couple_faits_distincts_site():
    a = _fait(value="12", qualifiers={"site": "Station House", "period": "2024-01"})
    b = _fait(value="12", qualifiers={"site": "Quarry Tower", "period": "2024-01"})
    out = classer_couple(a, b)
    assert out["issue"] == "faits_distincts"
    assert "site" in out["raison"].lower() or "portee" in out["raison"].lower()


def test_classer_couple_trajectoire():
    a = _fait(value="GBP 14.83", qualifiers={"since": "2024-11", "valid_to": "2025-09-08"})
    b = _fait(value="GBP 24.67", qualifiers={"since": "2025-09-08"})
    out = classer_couple(a, b)
    assert out["issue"] == "trajectoire"
    assert out["qualifiers_a"]
    assert out["qualifiers_b"]


def test_classer_couple_dispute():
    a = _fait(value="2 containers", qualifiers={"period": "2025-03", "site": "Station House"})
    b = _fait(value="3 containers", qualifiers={"period": "2025-03", "site": "Station House"})
    out = classer_couple(a, b)
    assert out["issue"] == "dispute"
    assert out["raison"]


def test_classer_couple_indecidable():
    a = _fait(value="2 containers", qualifiers={"site": "Station House"})
    b = _fait(value="3 containers", qualifiers={"period": "2025-03", "site": "Station House"})
    out = classer_couple(a, b)
    assert out["issue"] == "indecidable"
    assert "portee" in out["raison"].lower() or "portée" in out["raison"].lower()


def test_normaliser_quantite_piege_tonnes_kg():
    left = normaliser_quantite("13,334 t")
    right = normaliser_quantite("13334,000 kg")
    assert left is not None and right is not None
    assert left["unite_base"] == right["unite_base"] == "kg"
    assert left["valeur_base"] == right["valeur_base"] == 13334.0


def test_classer_couple_accord_piege_unites():
    a = _fait(value="13,334 t", qualifiers={"period": "2024"})
    b = _fait(value="13334,000 kg", qualifiers={"period": "2024"})
    out = classer_couple(a, b)
    assert out["issue"] == "accord"


def test_classer_couple_pas_accord_unites_differentes():
    """Z2 : « 2 containers » ≠ « 2 visits » — pas d'accord sur le premier entier."""
    a = _fait(value="2 containers", qualifiers={"period": "2025-03", "site": "Station House"})
    b = _fait(value="2 visits", qualifiers={"period": "2025-03", "site": "Station House"})
    out = classer_couple(a, b)
    assert out["issue"] != "accord"


def test_classer_couple_pas_accord_montants_devise_differents():
    """Z2 : « GBP 14.83 » ≠ « GBP 14.99 » — valeur numérique complète."""
    a = _fait(value="GBP 14.83", qualifiers={"period": "2024-11", "site": "Station House"})
    b = _fait(value="GBP 14.99", qualifiers={"period": "2024-11", "site": "Station House"})
    out = classer_couple(a, b)
    assert out["issue"] == "dispute"


def test_classer_couple_accord_montants_devise_identiques():
    a = _fait(value="GBP 14.83", qualifiers={"period": "2024-11"})
    b = _fait(value="GBP 14.83", qualifiers={"period": "2024-11"})
    out = classer_couple(a, b)
    assert out["issue"] == "accord"


def test_classer_couple_p4_resolves_document_entities():
    a = {
        "entity_id": "17_collection_register",
        "value": "Collection register — Copper Kettle / Prior-year invoice",
        "qualifiers": {"attribute_id": "collections"},
    }
    b = {
        "entity_id": "24_customer_review",
        "value": "Copper Kettle — annual service review / Collection activity",
        "qualifiers": {"attribute_id": "collections"},
    }
    assert classer_couple(a, b, palier="P0")["issue"] == "faits_distincts"
    out = classer_couple(a, b, palier="P4")
    assert out["issue"] != "faits_distincts" or "entité" not in out["raison"]
