"""Partage figé des 28 disputes — moitié réglage, moitié écart."""

from banc_realite import etage3 as e3
from banc_realite.partage_disputes import GRAINE, partager


def test_partage_ids_figes():
    reglage, ecart = partager(e3.load_questions())
    assert [q["id"] for q in reglage] == [
        "gl-q084",
        "gl-q086",
        "gl-q087",
        "gl-q080",
        "gl-q077",
        "gl-q076",
        "gl-q090",
        "gl-q097",
        "gl-q098",
        "gl-q078",
        "gl-q085",
        "gl-q079",
        "gl-q081",
        "gl-q082",
    ]
    assert [q["id"] for q in ecart] == [
        "gl-q096",
        "gl-q091",
        "gl-q073",
        "gl-q092",
        "gl-q089",
        "gl-q074",
        "gl-q094",
        "gl-q072",
        "gl-q088",
        "gl-q075",
        "gl-q083",
        "gl-q099",
        "gl-q093",
        "gl-q095",
    ]


def test_partage_deux_moitites_disjointes_reunion_28():
    reglage, ecart = partager(e3.load_questions())
    reglage_ids = {q["id"] for q in reglage}
    ecart_ids = {q["id"] for q in ecart}
    assert len(reglage_ids) == 14
    assert len(ecart_ids) == 14
    assert reglage_ids.isdisjoint(ecart_ids)
    assert reglage_ids | ecart_ids == {
        q["id"] for q in e3.load_questions() if q.get("shape") == "dispute"
    }
    assert len({q["id"] for q in e3.load_questions() if q.get("shape") == "dispute"}) == 28


def test_partage_deux_appels_identiques():
    questions = e3.load_questions()
    first = partager(questions)
    second = partager(questions)
    assert [q["id"] for q in first[0]] == [q["id"] for q in second[0]]
    assert [q["id"] for q in first[1]] == [q["id"] for q in second[1]]


def test_graine_ne_change_pas():
    assert GRAINE == 20260922
