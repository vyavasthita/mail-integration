from utils.datetime_helper import (
    get_today,
    subtract_days,
    add_days,
    change_format_from_datetime,
)


class QueryBuilder:
    SPACE = " "
    PLUS = "+"
    MINUS = "-"
    SEMICOLON = ";"
    NEW_LINE = "\n"
    SINGLE_QUOTE = "'"

    def __init__(self, rule: dict) -> None:
        self.rule = rule

    # SELECT message_id FROM email_sender WHERE MATCH (sender) AGAINST ("Abhijeet" IN BOOLEAN MODE)
    # UNION
    # SELECT message_id
    # FROM email_date
    # WHERE (received BETWEEN '2023-07-11' AND '2023-07-12');

    # SELECT message_id FROM email_sender WHERE sender = "Amin Boulouma <noreply@customers.gumroad.com>";

    def build(self):
        join_predicate = "AND"

        if self.rule["predicate"] == "any":
            join_predicate = "UNION"

        conditions = self.rule["conditions"]

        for index, condition in enumerate(conditions):
            table_name = str()
            column_name = str()

            condition_code = condition["code"]
            condition_predicate = condition["predicate"]

            if condition_code == 1:  # FROM
                table_name = "email_sender"
                column_name = "sender"
            elif condition_code == 2:  # To
                table_name = "email_receiver"
                column_name = "receiver"
            elif condition_code == 3:  # Subject
                table_name = "email_subject"
                column_name = "subject"
            elif condition_code == 4:  # Message
                table_name = "email_content"
                column_name = "content"
            elif condition_code == 5:  # Date Received
                table_name = "email_date"
                column_name = "received"

            query = "SELECT message_id FROM {}".format(table_name)

            predicate_code = condition_predicate["code"]
            predicate_value = condition_predicate["value"]

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

            # if (
            #     index != len(conditions) - 1
            # ):  # not processing last item, so add join predicate
            #     query += QueryBuilder.NEW_LINE + join_predicate

            query += QueryBuilder.SEMICOLON

            print(condition)
            print(query)
            print("*******************************************")
