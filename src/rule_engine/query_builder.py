# Ref: https://dev.mysql.com/doc/refman/8.0/en/fulltext-boolean.html
from enum import Enum, IntEnum


from src.utils.datetime_helper import (
    get_today,
    subtract_days,
    add_days,
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

    def gen_table_query_str(self, condition_code: int):
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

    def gen_match_query_str(self, column: str, predicate_value: str):
        # MATCH (sender) AGAINST ('"Naukri"' IN BOOLEAN MODE)
        return f"MATCH ({column}) AGAINST ('\"{predicate_value}\"' IN BOOLEAN MODE)"

    def get_date_duration(self, predicate_value: str, predicate_duration: str):
        return (
            predicate_value * 30 if predicate_duration == "months" else predicate_value
        )

    def get_date_field_dates(self, predicate_code: int, days_duration: str):
        today_date = get_today()
        start = None
        end = None

        if predicate_code == QueryBuilder.Predicate.LESS_THAN:
            end = today_date
            start = subtract_days(end, days_duration)
        elif predicate_code == QueryBuilder.Predicate.GREATOR_THAN:
            start = today_date
            end = add_days(start, days_duration)

        start_date = change_format_from_datetime(start, "%Y-%m-%d")
        end_date = change_format_from_datetime(end, "%Y-%m-%d")

        return start_date, end_date

    def gen_date_field_query_str(
        self,
        column: str,
        predicate_code: int,
        predicate_value: str,
        predicate_duration: str,
    ):
        # (received BETWEEN '2023-06-20' AND '2023-07-20')
        start_date, end_date = self.get_date_field_dates(
            predicate_code, self.get_date_duration(predicate_value, predicate_duration)
        )

        return f"({column} BETWEEN '{start_date}' AND '{end_date}')"

    def gen_str_field_query_str(self, column, condition_predicate: dict):
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

    def gen_field_query_str(self, column: str, condition: dict):
        condition_predicate = condition["predicate"]

        if condition["code"] == QueryBuilder.Field.DATE_RECEIVED:
            return self.gen_date_field_query_str(
                column,
                condition_predicate["code"],
                condition_predicate["value"],
                condition_predicate["duration"],
            )

        return self.gen_str_field_query_str(column, condition_predicate)

    def build_condition_query(self, condition):
        table, column = self.gen_table_query_str(condition_code=condition["code"])

        return (
            "SELECT message_id FROM {}".format(table)
            + QueryBuilder.Operator.SPACE
            + "WHERE"
            + QueryBuilder.Operator.SPACE
            + self.gen_field_query_str(column, condition)
        )


class AllQueryBuilder(QueryBuilder):
    def get_where_conditions(self, conditions: list):
        query = str()

        for index, condition in enumerate(conditions):
            table, column = self.gen_table_query_str(condition_code=condition["code"])
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

    def gen_join_condition(self, conditions: list):
        # JOIN email_receiver using (message_id)
        # JOIN email_subject using (message_id)
        joining_column = "message_id"
        query = str()
        processed_conditions = set()

        for index, condition in enumerate(conditions):
            table, column = self.gen_table_query_str(condition_code=condition["code"])

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

    def build_all_predicate(self, conditions: list):
        # SELECT email_sender.message_id,
        # MATCH(email_sender.sender) AGAINST('+interviews') as sender,
        # MATCH(email_receiver.receiver) AGAINST('+gmail.com') as receiver
        # FROM email_sender
        # LEFT JOIN email_receiver ON email_sender.message_id = email_receiver.message_id
        # WHERE
        # MATCH(email_sender.sender) AGAINST('+interviews');
        return (
            self.gen_join_condition(conditions)
            + "WHERE"
            + QueryBuilder.Operator.NEW_LINE
            + QueryBuilder.Operator.SPACE
            + self.get_where_conditions(conditions)
            + QueryBuilder.Operator.SEMICOLON
        )


class AnyQueryBuilder(QueryBuilder):
    def build_any_predicate(self, conditions):
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

