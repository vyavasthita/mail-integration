# Ref: https://dev.mysql.com/doc/refman/8.0/en/fulltext-boolean.html
from enum import Enum, IntEnum


from utils.datetime_helper import (
    get_today,
    subtract_days,
    add_days,
    change_format_from_datetime,
)


class QueryBuilder:
    class StrOperator(str, Enum):
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

    def __init__(self, rule: dict) -> None:
        self.rule = rule

    def gen_table_query_str(self, condition_code: int):
        table_name = str()
        column = str()

        if condition_code == QueryBuilder.Field.FROM:
            table_name = "email_sender"
            column = "sender"
        elif condition_code == QueryBuilder.Field.TO:
            table_name = "email_receiver"
            column = "receiver"
        elif condition_code == QueryBuilder.Field.SUBJECT:
            table_name = "email_subject"
            column = "subject"
        elif condition_code == QueryBuilder.Field.MESSAGE:
            table_name = "email_content"
            column = "content"
        elif condition_code == QueryBuilder.Field.DATE_RECEIVED:
            table_name = "email_date"
            column = "received"

        return table_name, column

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
                QueryBuilder.StrOperator.NOT.value
                + QueryBuilder.StrOperator.SPACE.value
                + match_string
            )
        elif predicate_code == QueryBuilder.Predicate.EQUALS:
            # LENGTH(subject) = LENGTH("tenmiles.com")
            match_string = (
                match_string
                + QueryBuilder.StrOperator.SPACE.value
                + "AND"
                + QueryBuilder.StrOperator.SPACE.value
                + f"LENGTH({column}) = LENGTH('{predicate_value}')"
            )
        elif predicate_code == QueryBuilder.Predicate.DOES_NOT_EQUAL:
            # content != 'Scheduled'
            match_string = f"{column} {QueryBuilder.StrOperator.NOT_EQUAL.value} '{predicate_value}'"

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

    def build_condition_query(self, predicate: str, condition):
        select_columns = "*" if predicate == "all" else "message_id"

        table_name, column = self.gen_table_query_str(condition_code=condition["code"])

        return (
            "SELECT {} FROM {}".format(select_columns, table_name)
            + QueryBuilder.StrOperator.SPACE
            + "WHERE"
            + QueryBuilder.StrOperator.SPACE
            + self.gen_field_query_str(column, condition)
        )

    def build_all_predicate(self, predicate: str):
        # SELECT email_sender.message_id,
        # MATCH(email_sender.sender) AGAINST('+interviews') as sender,
        # MATCH(email_receiver.receiver) AGAINST('+gmail.com') as receiver
        # FROM email_sender
        # LEFT JOIN email_receiver ON email_sender.message_id = email_receiver.message_id
        # WHERE
        # MATCH(email_sender.sender) AGAINST('+interviews');

        cumulative_query = str()

        conditions = self.rule["conditions"]

        for index, condition in enumerate(conditions):
            query = "SELECT {}.message_id FROM {}"

            table_name = str()
            column_name = str()

            condition_code = condition["code"]
            condition_predicate = condition["predicate"]

            if condition_code == 1:  # FROM
                table_name = "email_sender"
                column_name = "sender"
                query = query.format(table_name, table_name)
            elif condition_code == 2:  # To
                table_name = "email_receiver"
                column_name = "receiver"
                query = query + QueryBuilder.COMMA + QueryBuilder.SPACE + table_name
            elif condition_code == 3:  # Subject
                table_name = "email_subject"
                column_name = "subject"
                query = query + QueryBuilder.COMMA + QueryBuilder.SPACE + table_name
            elif condition_code == 4:  # Message
                table_name = "email_content"
                column_name = "content"
                query = query + QueryBuilder.COMMA + QueryBuilder.SPACE + table_name
            elif condition_code == 5:  # Date Received
                table_name = "email_date"
                column_name = "received"
                query = query + QueryBuilder.COMMA + QueryBuilder.SPACE + table_name

            predicate_code = condition_predicate["code"]
            predicate_value = condition_predicate["value"]

            query = query + QueryBuilder.NEW_LINE + "WHERE" + QueryBuilder.NEW_LINE

            if predicate_code == 1 or predicate_code == 2:
                full_text_index_op = str()

                if predicate_code == 1:  # contains
                    full_text_index_op = QueryBuilder.PLUS
                elif predicate_code == 2:  # Does not contain
                    full_text_index_op = QueryBuilder.MINUS

                query = (
                    query
                    + QueryBuilder.SPACE
                    + "WHERE MATCH"
                    + QueryBuilder.SPACE
                    + f"({column_name})"
                    + QueryBuilder.SPACE
                    + "AGAINST"
                    + QueryBuilder.SPACE
                    + f"('{full_text_index_op}{predicate_value}' IN BOOLEAN MODE)"
                )
            elif predicate_code == 3 or predicate_code == 4:
                equality_condition = str()

                if predicate_code == 3:  # Equals
                    equality_condition = "="
                elif predicate_code == 4:  # Does not equal
                    equality_condition = "!="

                query = (
                    query
                    + QueryBuilder.SPACE
                    + "WHERE"
                    + QueryBuilder.SPACE
                    + column_name
                    + QueryBuilder.SPACE
                    + equality_condition
                    + QueryBuilder.SPACE
                    + QueryBuilder.SINGLE_QUOTE
                    + predicate_value
                    + QueryBuilder.SINGLE_QUOTE
                )
            elif predicate_code == 5 or predicate_code == 6:
                predicate_duration = condition_predicate["duration"]

                if predicate_duration == "months":
                    predicate_value *= 30

                today_date = get_today()
                start = None
                end = None

                if predicate_code == 5:  # is less than
                    end = today_date
                    start = subtract_days(end, predicate_value)
                elif predicate_code == 6:  # is greator than
                    start = today_date
                    end = add_days(start, predicate_value)

                start = change_format_from_datetime(start, "%Y-%m-%d")
                end = change_format_from_datetime(end, "%Y-%m-%d")

                query = (
                    query
                    + QueryBuilder.SPACE
                    + "WHERE"
                    + QueryBuilder.SPACE
                    + f"({column_name} BETWEEN '{start}' AND '{end}')"
                )

        return cumulative_query

    def build_any_predicate(self, predicate: str):
        cumulative_query = str()

        conditions = self.rule["conditions"]

        for index, condition in enumerate(conditions):
            cumulative_query += self.build_condition_query(predicate, condition)

            if (
                index != len(conditions) - 1
            ):  # not processing last item, so add join predicate
                cumulative_query += (
                    QueryBuilder.StrOperator.NEW_LINE
                    + "UNION"
                    + QueryBuilder.StrOperator.NEW_LINE
                )

        cumulative_query += QueryBuilder.StrOperator.SEMICOLON

        return cumulative_query

    def build(self):
        predicate = self.rule["predicate"]
        if predicate == "all":
            return self.build_all_predicate(predicate)
        elif predicate == "any":
            return self.build_any_predicate(predicate)
