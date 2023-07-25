import os
import json
import csv
import pytest
from datetime import timedelta, date
from src.rule_engine.query_builder import QueryBuilder, AllQueryBuilder


test_schema_dir = "tests/unit/schema"

# Test 1
table_column_info = os.path.join(test_schema_dir, "table_column_info.csv")


def subtract_days(source_date: date, no_of_days: int) -> date:
    return source_date - timedelta(days=no_of_days)


def read_table_column_info(file_name):
    with open(file_name, newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        next(data)  # skip header row

        return [[int(row[0]), row[1], row[2]] for row in data if row]


@pytest.mark.parametrize(
    "condition_code, expected_table_name, expected_column_name",
    read_table_column_info(table_column_info),
)
def test_get_table_info(condition_code, expected_table_name, expected_column_name):
    query_builder = QueryBuilder()

    # Get table info for From field
    table, column = query_builder.get_table_info(condition_code)

    assert table == expected_table_name

    assert column == expected_column_name


# Test 2
match_query_string = os.path.join(test_schema_dir, "match_query_string.csv")


def read_match_query_string(file_name):
    with open(file_name, newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        next(data)  # skip header row
        return [[row[0], row[1], row[2]] for row in data if row]


@pytest.mark.parametrize(
    "column, predicate_value, expected_query",
    read_match_query_string(match_query_string),
)
def test_gen_match_query_str(column, predicate_value, expected_query):
    query_builder = QueryBuilder()

    query_string = query_builder.gen_match_query_str(column, predicate_value)

    assert query_string == expected_query


# Test 3
date_duration = os.path.join(test_schema_dir, "date_duration.csv")


def read_date_duration(file_name):
    with open(file_name, newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        next(data)  # skip header row
        return [[int(row[0]), row[1], int(row[2])] for row in data if row]


@pytest.mark.parametrize(
    "predicate_value, predicate_duration, date_duration",
    read_date_duration(date_duration),
)
def test_get_date_duration(predicate_value, predicate_duration, date_duration):
    query_builder = QueryBuilder()

    duration = query_builder.get_date_duration(predicate_value, predicate_duration)

    assert duration == date_duration


# Test 4
any_predicate = os.path.join(test_schema_dir, "any_predicate_rules.json")


def read_any_predicate(file_name):
    with open(file_name) as f:
        return [json.load(f)]


@pytest.mark.parametrize(
    "conditions",
    read_any_predicate(any_predicate),
)
def test_build_any_predicate(conditions, today_date):
    all_query_builder = AllQueryBuilder()

    subtracted_date = subtract_days(today_date, conditions[1]["predicate"]["value"] - 1)

    query = all_query_builder.build_all_predicate(conditions)
    expected_query = """SELECT message_id FROM email_subject
 JOIN email_date using (message_id)
WHERE
 MATCH (subject) AGAINST ('"some testing subject"' IN BOOLEAN MODE)
 AND received > '{}';""".format(
        subtracted_date
    )

    assert query == expected_query
