import pytest
from table import read_csv, apply_filter, aggregate

ROWS = [
    {"name": "A", "price": "100", "rating": "4.5"},
    {"name": "B", "price": "200", "rating": "4.8"},
    {"name": "C", "price": "300", "rating": "4.2"},
]

# ------- read_csv --------

def test_read_csv_missing_file():
    with pytest.raises(SystemExit):
        read_csv("not_exists.csv")

# ------- apply_filter --------

def test_filter_no_filter():
    assert apply_filter(ROWS, None) == ROWS

def test_filter_equal():
    result = apply_filter(ROWS, "name=B")
    assert len(result) == 1 and result[0]["name"] == "B"

def test_filter_greater():
    result = apply_filter(ROWS, "price>150")
    assert {r["name"] for r in result} == {"B", "C"}

def test_filter_less():
    result = apply_filter(ROWS, "rating<4.6")
    assert {r["name"] for r in result} == {"A", "C"}

def test_filter_unknown_column():
    with pytest.raises(SystemExit):
        apply_filter(ROWS, "foo=bar")

def test_filter_bad_format_double_operator():
    with pytest.raises(SystemExit):
        apply_filter(ROWS, "price>>100")

def test_filter_bad_format_symbol():
    with pytest.raises(SystemExit):
        apply_filter(ROWS, "price#100")

# ------- aggregate --------

def test_aggregate_avg():
    result = aggregate(ROWS, "avg=price")
    assert result.startswith("AVG(price) =")

def test_aggregate_min():
    assert aggregate(ROWS, "min=rating") == "MIN(rating) = 4.2"

def test_aggregate_max():
    result = aggregate(ROWS, "max=price")
    assert result.startswith("MAX(price) =")
    assert "300" in result

def test_aggregate_no_param():
    assert aggregate(ROWS, None) == ""

def test_aggregate_unknown_column():
    with pytest.raises(SystemExit):
        aggregate(ROWS, "avg=foo")

def test_aggregate_non_numeric():
    with pytest.raises(SystemExit):
        aggregate(ROWS, "avg=name")

def test_aggregate_bad_format():
    with pytest.raises(SystemExit):
        aggregate(ROWS, "avgprice")

def test_aggregate_unknown_function():
    with pytest.raises(SystemExit):
        aggregate(ROWS, "sum=price")