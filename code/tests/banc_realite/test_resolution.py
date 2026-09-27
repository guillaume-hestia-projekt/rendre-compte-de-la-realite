"""Résolution d'entité et d'attribut par paliers cumulatifs — tests et contre-exemples."""

from banc_realite.resolution import (
    PALIERS,
    ResolutionContext,
    build_inventaire_from_claims,
    build_resolution_context,
    entities_match,
    attributes_match,
    normalize_entity_form,
    strip_role_prefix,
    strip_year_period_suffix,
)


def _ctx(claims: list[dict] | None = None) -> ResolutionContext:
    claims = claims or []
    inv = build_inventaire_from_claims(claims)
    return build_resolution_context(inv, claims)


def _fait(
    entity_id: str,
    attribute_id: str | None = None,
    value: str = "",
    qualifiers: dict | None = None,
) -> dict:
    quals = dict(qualifiers or {})
    if attribute_id is not None:
        quals["attribute_id"] = attribute_id
    return {"entity_id": entity_id, "value": value, "qualifiers": quals}


def test_p0_strict_entity_match():
    ctx = _ctx()
    a = _fait("copper_kettle", "nombre_collectes")
    b = _fait("copper_kettle", "nombre_collectes")
    assert entities_match(a, b, "P0", ctx)


def test_p0_counter_example_different_entities():
    ctx = _ctx()
    a = _fait("copper_kettle", "nombre_collectes")
    b = _fait("quarry_tower", "nombre_collectes")
    assert not entities_match(a, b, "P0", ctx)


def test_p1_strip_role_prefix_compte():
    ctx = _ctx(
        [
            {"entity_id": "copper_kettle", "value": "x", "qualifiers": {}},
            {"entity_id": "compte_copper_kettle", "value": "y", "qualifiers": {}},
        ]
    )
    a = _fait("compte_copper_kettle", "site")
    b = _fait("copper_kettle", "site")
    assert not entities_match(a, b, "P0", ctx)
    assert entities_match(a, b, "P1", ctx)


def test_p1_strip_numeric_document_prefix():
    ctx = _ctx(
        [
            {"entity_id": "collection_register", "value": "x", "qualifiers": {}},
            {"entity_id": "17_collection_register", "value": "y", "qualifiers": {}},
        ]
    )
    a = _fait("17_collection_register", "weighings")
    b = _fait("collection_register", "weighings")
    assert entities_match(a, b, "P1", ctx)


def test_p1_counter_example_different_subjects_after_prefix_strip():
    ctx = _ctx()
    a = _fait("compte_copper_kettle", "site")
    b = _fait("compte_quarry_tower", "site")
    assert not entities_match(a, b, "P1", ctx)


def test_p2_inclusion_word_boundary():
    ctx = _ctx()
    a = _fait("copper_kettle", "site")
    b = _fait("copper_kettle_station_house", "site")
    assert not entities_match(a, b, "P1", ctx)
    assert entities_match(a, b, "P2", ctx)


def test_p2_simple_plural():
    ctx = _ctx()
    a = _fait("mosswheel_service", "charge")
    b = _fait("mosswheel_services", "charge")
    assert entities_match(a, b, "P2", ctx)


def test_p2_counter_example_homonym_different_roots():
    ctx = _ctx()
    a = _fait("circuit_a", "capacity")
    b = _fait("circuit_b", "capacity")
    assert not entities_match(a, b, "P2", ctx)


def test_p3_bilingual_attribute_pair():
    claims = [
        {
            "entity_id": "copper_kettle",
            "value": "12",
            "qualifiers": {"attribute_id": "collected_sites"},
        },
        {
            "entity_id": "copper_kettle",
            "value": "12",
            "qualifiers": {"attribute_id": "sites_collectes"},
        },
    ]
    ctx = _ctx(claims)
    a = _fait("copper_kettle", "collected_sites")
    b = _fait("copper_kettle", "sites_collectes")
    assert not attributes_match(a, b, "P2", ctx)
    assert attributes_match(a, b, "P3", ctx)


def test_p3_strip_year_suffix_when_period_in_qualifiers():
    a = _fait(
        "copper_kettle",
        "collected_sites_2024",
        qualifiers={"period": "2024"},
    )
    b = _fait("copper_kettle", "collected_sites", qualifiers={"period": "2024"})
    ctx = _ctx([a, b])
    assert attributes_match(a, b, "P3", ctx)
    assert strip_year_period_suffix("collected_sites_2024", {"period": "2024"}) == "collected_sites"


def test_p3_counter_example_different_periods():
    a = _fait("copper_kettle", "collected_sites_2024", qualifiers={"period": "2024"})
    b = _fait("copper_kettle", "collected_sites_2025", qualifiers={"period": "2025"})
    ctx = _ctx([a, b])
    assert not attributes_match(a, b, "P3", ctx)


def test_p4_customer_key_from_claim_text():
    claims = [
        {
            "entity_id": "17_collection_register",
            "value": "Collection register — Copper Kettle / Prior-year invoice",
            "qualifiers": {},
        },
        {
            "entity_id": "24_customer_review",
            "value": "Copper Kettle — annual service review and update / Collection activity",
            "qualifiers": {},
        },
    ]
    ctx = _ctx(claims)
    a = _fait("17_collection_register", value=claims[0]["value"])
    b = _fait("24_customer_review", value=claims[1]["value"])
    assert not entities_match(a, b, "P3", ctx)
    assert entities_match(a, b, "P4", ctx)


def test_p4_counter_example_same_customer_different_sites_stay_distinct_entities():
    ctx = _ctx(
        [
            {
                "entity_id": "station_house",
                "value": "Copper Kettle — Station House site profile",
                "qualifiers": {},
            },
            {
                "entity_id": "quarry_tower",
                "value": "Copper Kettle — Quarry Tower site profile",
                "qualifiers": {},
            },
        ]
    )
    a = _fait("station_house", value="Copper Kettle — Station House site profile")
    b = _fait("quarry_tower", value="Copper Kettle — Quarry Tower site profile")
    assert not entities_match(a, b, "P4", ctx)


def test_paliers_are_cumulative():
    assert PALIERS == ("P0", "P1", "P2", "P3", "P4")
    assert strip_role_prefix("compte_copper_kettle", ["compte_"]) == "copper_kettle"
    assert normalize_entity_form("Copper-Kettle") == "copper_kettle"
