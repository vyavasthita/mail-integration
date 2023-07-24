"""Generates query from email_rules.json

@file query_builder.py
@author Dilip Kumar Sharma
@date 22nd July 2023

About; -
--------
    This module is responsible for creating queries as per rules defined in email_rules.json.

    Ref: https://dev.mysql.com/doc/refman/8.0/en/fulltext-boolean.html
"""
# Core python packages
from enum import Enum, IntEnum
from datetime import datetime

# Application packages
from src.utils.datetime_helper import (
    get_today,
    subtract_days,
    change_format_from_datetime,
)


class QueryBuilder:
    class Operator(str, Enum):
        SPACE = " "
        PLUS = "+"
        MINUS = "-"
        SEMICOLON = ";"
        NEW_LINE = "\n"
        SINGLE_QUOTE = "'"
        COMMA = ","
        NOT = "NOT"
        EQUAL = "="
        NOT_EQUAL = "!="
        TAB = "\t"
        LESS_THAN = "<"
        GREATOR_THAN = ">"

    class Field(IntEnum):
        FROM = 1
        TO = 2
        SUBJECT = 3
        MESSAGE = 4
        DATE_RECEIVED = 5

    class Predicate(IntEnum):
        CONTAINS = 1
        DOES_NOT_CONTAIN = 2
        EQUALS = 3
        DOES_NOT_EQUAL = 4
        LESS_THAN = 5
        GREATOR_THAN = 6

    def get_table_info(self, condition_code: int) -> tuple:
        """
        Get table and column name based on the field in email_rules.json

        Args:
            condition_code (int): Code for given field

        Returns:
            tuple: table and column names
        """
        table = str()
        column = str()

        if condition_code == QueryBuilder.Field.FROM:
            table = "email_sender"
            column = "sender"
        elif condition_code == QueryBuilder.Field.TO:
            table = "email_receiver"
            column = "receiver"
        elif condition_code == QueryBuilder.Field.SUBJECT:
            table = "email_subject"
            column = "subject"
        elif condition_code == QueryBuilder.Field.MESSAGE:
            table = "email_content"
            column = "content"
        elif condition_code == QueryBuilder.Field.DATE_RECEIVED:
            table = "email_date"
            column = "received"

        return table, column

    def gen_match_query_str(self, column: str, predicate_value: str) -> str:
        """
        This method generates query for match part of string

        Args:
            column (str): Column of table for which query is being constructed.
            predicate_value (str): Value of predicate which needs to be matched in database.

        Returns:
            str: _description_
        """
        # MATCH (sender) AGAINST ('"Naukri"' IN BOOLEAN MODE)
        return f"MATCH ({column}) AGAINST ('\"{predicate_value}\"' IN BOOLEAN MODE)"

    def get_date_duration(self, predicate_value: str, predicate_duration: str) -> None:
        """
        Generate duration between which date query needs to be executed.

        Args:
            predicate_value (str): Value of predicate which needs to be matched in database.
            predicate_duration (str): Months or days
        """

        return (
            predicate_value * 30 if predicate_duration == "months" else predicate_value
        )

    def get_start_date(self, days_duration: str) -> datetime:
        """
        Get start date starting which query needs to be executed.

        Args:
            days_duration (str): Months or days
        """
        return change_format_from_datetime(
            subtract_days(get_today(), days_duration), "%Y-%m-%d"
        )

    def gen_date_field_query_str(
        self,
        column: str,
        predicate_code: int,
        predicate_value: str,
        predicate_duration: str,
    ) -> str:
        """
        Generate query for date field.

        Args:
            column (str): No table column on which date query is to be applied
            predicate_code (int): Less than or greator than condition
            predicate_value (str): Value of predicate which needs to be matched in database.
            predicate_duration (str): Months or days

        Returns:
            str: _description_
        """
        start_date = self.get_start_date(
            self.get_date_duration(predicate_value, predicate_duration)
        )

        condition_operator = str()

        if predicate_code == QueryBuilder.Predicate.LESS_THAN:
            condition_operator = QueryBuilder.Operator.GREATOR_THAN
        elif predicate_code == QueryBuilder.Predicate.GREATOR_THAN:
            condition_operator = QueryBuilder.Operator.LESS_THAN

        return f"{column} {condition_operator} '{start_date}'"

    def gen_str_field_query_str(self, column: str, condition_predicate: dict) -> None:
        """
        Generate query string for 'Contains', 'Does not contain', 'Equals' and 'Does not equal'

        Args:
            column (str): Name of column on which query needs to be applied.
            condition_predicate (dict): Details of condition for which query string to be generated.

        Returns:
            _type_: _description_
        """
        predicate_code = condition_predicate["code"]
        predicate_value = condition_predicate["value"]

        match_string = self.gen_match_query_str(column, predicate_value)

        if predicate_code == QueryBuilder.Predicate.CONTAINS:
            pass
        elif predicate_code == QueryBuilder.Predicate.DOES_NOT_CONTAIN:
            match_string = (
                QueryBuilder.Operator.NOT.value
                + QueryBuilder.Operator.SPACE.value
                + match_string
            )
        elif predicate_code == QueryBuilder.Predicate.EQUALS:
            # LENGTH(subject) = LENGTH("tenmiles.com")
            match_string = (
                match_string
                + QueryBuilder.Operator.SPACE.value
                + "AND"
                + QueryBuilder.Operator.SPACE.value
                + f"LENGTH({column}) = LENGTH('{predicate_value}')"
            )
        elif predicate_code == QueryBuilder.Predicate.DOES_NOT_EQUAL:
            # content != 'Scheduled'
            match_string = (
                f"{column} {QueryBuilder.Operator.NOT_EQUAL.value} '{predicate_value}'"
            )

        return match_string

    def gen_field_query_str(self, column: str, condition: dict) -> str:
        """
        Generate query for single field.
        {
            "field": "From",
            "code": 1,
            "predicate": {
                "type": "str",
                "code": 1,
                "name": "contains",
                "value": "interviews"
            }
        }

        Args:
            column (str): Name of column of table on which query needs to be applied.
            condition (dict): _description_

        Returns:
            str: Query string
        """
        condition_predicate = condition["predicate"]

        if condition["code"] == QueryBuilder.Field.DATE_RECEIVED:
            return self.gen_date_field_query_str(
                column,
                condition_predicate["code"],
                condition_predicate["value"],
                condition_predicate["duration"],
            )

        return self.gen_str_field_query_str(column, condition_predicate)

    def build_condition_query(self, condition: dict) -> str:
        """
        Build query for a given condition.
        {
            "field": "From",
            "code": 1,
            "predicate": {
                "type": "str",
                "code": 1,
                "name": "contains",
                "value": "interviews"
            }
        }

        Args:
            condition (dict): Condition for which query needs to be generated.

        Returns:
            str: Query string
        """
        table, column = self.get_table_info(condition_code=condition["code"])

        return (
            "SELECT message_id FROM {}".format(table)
            + QueryBuilder.Operator.SPACE
            + "WHERE"
            + QueryBuilder.Operator.SPACE
            + self.gen_field_query_str(column, condition)
        )


class AllQueryBuilder(QueryBuilder):
    def get_where_conditions(self, conditions: list) -> str:
        """
        Generates where conditions query.

        MATCH(email_sender.sender) AGAINST('"interview"' IN BOOLEAN MODE)
        AND MATCH(email_receiver.receiver) AGAINST('"gmail"' IN BOOLEAN MODE)
        AND MATCH (email_subject.subject) AGAINST ('"sharma bharat"' IN BOOLEAN MODE)
        AND LENGTH(subject) = LENGTH("sharma bharat");

        Args:
            conditions (list): List of conditions

        Returns:
            str: Query string
        """
        query = str()

        for index, condition in enumerate(conditions):
            table, column = self.get_table_info(condition_code=condition["code"])
            query += self.gen_field_query_str(column, condition)

            if (
                index != len(conditions) - 1
            ):  # not processing last item, so add AND condition followed by a SPACE
                query = (
                    query
                    + QueryBuilder.Operator.NEW_LINE
                    + QueryBuilder.Operator.SPACE
                    + "AND"
                    + QueryBuilder.Operator.SPACE
                )
        return query

    def gen_join_condition(self, conditions: list) -> str:
        """
        Constructs query for join conditions

        JOIN email_receiver using (message_id)
        JOIN email_subject using (message_id)

        Args:
            conditions (list): Conditions for which query needs to be generated.

        Returns:
            str: Query string
        """
        joining_column = "message_id"
        query = str()
        processed_conditions = set()

        for index, condition in enumerate(conditions):
            table, column = self.get_table_info(condition_code=condition["code"])

            if index == 0:
                query = (
                    query
                    + "SELECT message_id FROM {}".format(table)
                    + QueryBuilder.Operator.NEW_LINE
                )
                continue

            # If same condition is added twice, we should not add join condition twice
            if table not in processed_conditions:
                query = (
                    query
                    + f"{QueryBuilder.Operator.SPACE}JOIN {table} using ({joining_column})"
                    + QueryBuilder.Operator.NEW_LINE
                )
                processed_conditions.add(table)

        return query

    def build_all_predicate(self, conditions: list) -> str:
        """
        Generate the complete query for 'All' predicate.

        SELECT email_sender.message_id,
        MATCH(email_sender.sender) AGAINST('+interviews') as sender,
        MATCH(email_receiver.receiver) AGAINST('+gmail.com') as receiver
        FROM email_sender
        LEFT JOIN email_receiver ON email_sender.message_id = email_receiver.message_id
        WHERE
        MATCH(email_sender.sender) AGAINST('+interviews');

        Args:
            conditions (list): Conditions for which query needs to be generated.

        Returns:
            str: Query string
        """

        return (
            self.gen_join_condition(conditions)
            + "WHERE"
            + QueryBuilder.Operator.NEW_LINE
            + QueryBuilder.Operator.SPACE
            + self.get_where_conditions(conditions)
            + QueryBuilder.Operator.SEMICOLON
        )


class AnyQueryBuilder(QueryBuilder):
    def build_any_predicate(self, conditions: dict) -> str:
        """
        Generate the complete query for 'Any' predicate.

        SELECT message_id FROM email_sender WHERE MATCH (sender) AGAINST ('+tenmiles.com' IN BOOLEAN MODE)
        UNION
        SELECT message_id FROM email_receiver WHERE receiver = 'www.amazon.com'
        UNION
        SELECT message_id FROM email_subject WHERE MATCH (subject) AGAINST ('-Interview' IN BOOLEAN MODE)
        UNION
        SELECT message_id FROM email_content WHERE content != 'Scheduled'
        UNION
        SELECT message_id FROM email_date WHERE (received BETWEEN '2023-06-20' AND '2023-07-20')
        UNION
        SELECT message_id FROM email_date WHERE (received BETWEEN '2023-07-20' AND '2023-07-31');

        Args:
            conditions (dict): Conditions for which query needs to be generated.

        Returns:
            str: Query string
        """
        cumulative_query = str()

        for index, condition in enumerate(conditions):
            cumulative_query += self.build_condition_query(condition)

            if index != (
                len(conditions) - 1
            ):  # not processing last item, so add join predicate
                cumulative_query += (
                    QueryBuilder.Operator.NEW_LINE
                    + "UNION"
                    + QueryBuilder.Operator.NEW_LINE
                )

        cumulative_query += QueryBuilder.Operator.SEMICOLON

        return cumulative_query
