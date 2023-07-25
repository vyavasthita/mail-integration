import os
import json
import pytest
from datetime import timedelta, date
from src.rule_engine.query_builder import AnyQueryBuilder


test_schema_dir = "tests/integration/schema"


# Test 4
any_predicate = os.path.join(test_schema_dir, "any_predicate_rules_1.json")


def read_any_predicate(file_name):
    with open(file_name) as f:
        return [json.load(f)]


def subtract_days(source_date: date, no_of_days: int) -> date:
    return source_date - timedelta(days=no_of_days)


@pytest.mark.integration
@pytest.mark.parametrize(
    "conditions",
    read_any_predicate(any_predicate),
)
def test_any_predicate(db_connection, set_up_test_data_1, today_date, conditions):
    any_query_builder = AnyQueryBuilder()

    subtracted_date = subtract_days(today_date, conditions[1]["predicate"]["value"] - 1)

    query = any_query_builder.build_any_predicate(conditions)

    expected_query = """SELECT message_id FROM email_subject WHERE NOT MATCH (subject) AGAINST ('"scheduled"' IN BOOLEAN MODE)
UNION
SELECT message_id FROM email_date WHERE received > '{}';""".format(
        subtracted_date
    )

    assert query == expected_query

    # now fetch records from db
    cursor = db_connection.cursor()
    cursor.execute(query)
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "message_id_2",
            "message_id_3",
            "message_id_4",
        ]
    )
