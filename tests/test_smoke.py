from fixm4b.helpers.cleaners import fix_smart_quotes, minimalist_title
from fixm4b.ol_lookup import parse_ol_ref, title_sim


def test_fix_smart_quotes():
    assert fix_smart_quotes("“Hello”") == '"Hello"'


def test_title_sim_basic():
    ratio, token = title_sim("Eon", "Eon")
    assert ratio == 1.0
    assert token == 1.0


def test_parse_ol_ref():
    assert parse_ol_ref("OL29358192W") == ("works", "OL29358192W")


def test_minimalist_title_basic():
    assert minimalist_title("The Hobbit") == "The Hobbit"
    assert isinstance(minimalist_title("Eon: Dragoneye Reborn"), str)
