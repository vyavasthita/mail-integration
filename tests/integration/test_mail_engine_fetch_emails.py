import pytest
from mail_helper import MailHelper

test_schema_dir = "tests/integration/schema"


@pytest.mark.integration
def test_any_predicate(mocker, db_connection):
    def mock_process_labels(self):
        self.data["label"] = [
            ("DUMMY_LABEL_ID_1", "DUMMY_LABEL_1"),
            ("DUMMY_LABEL_ID_2", "DUMMY_LABEL_2"),
            ("DUMMY_LABEL_ID_3", "DUMMY_LABEL_3"),
        ]

    def mock_process_emails(self):
        message_id_1 = "temp_message_id_1"
        message_id_2 = "temp_message_id_2"
        message_id_3 = "temp_message_id_3"

        self.data["email"].extend(
            [(message_id_1, True), (message_id_2, False), (message_id_3, True)]
        )
        self.data["sender"].extend(
            [
                (message_id_1, "sender_1"),
                (message_id_2, "sender_2"),
                (message_id_3, "sender_3"),
            ]
        )
        self.data["receiver"].extend(
            [
                (message_id_1, "receiver_1"),
                (message_id_2, "receiver_2"),
                (message_id_3, "receiver_3"),
            ]
        )
        self.data["subject"].extend(
            [
                (message_id_1, "subject_1"),
                (message_id_2, "subject_2"),
                (message_id_3, "subject_3"),
            ]
        )
        self.data["content"].extend(
            [
                (message_id_1, "body_1"),
                (message_id_2, "body_2"),
                (message_id_3, "body_3"),
            ]
        )
        self.data["date"].extend(
            [
                (message_id_1, "2023-07-25"),
                (message_id_2, "2023-07-24"),
                (message_id_3, "2023-06-10"),
            ]
        )

    mail_helper = MailHelper()

    mocker.patch("mail_helper.MailEngine.process_labels", mock_process_labels)
    mocker.patch("mail_helper.MailEngine.process_emails", mock_process_emails)

    mail_helper.initialize()

    mail_helper.start_mail_engine()  # This will write data to database

    # verify email table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    # verify email_sender table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email_sender")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    assert set([result[1] for result in result_set]) == set(
        [
            "sender_1",
            "sender_2",
            "sender_3",
        ]
    )

    # verify email_receiver table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email_receiver")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    assert set([result[1] for result in result_set]) == set(
        [
            "receiver_1",
            "receiver_2",
            "receiver_3",
        ]
    )

    # verify email_subject table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email_subject")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    assert set([result[1] for result in result_set]) == set(
        [
            "subject_1",
            "subject_2",
            "subject_3",
        ]
    )

    # verify email_content table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email_content")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    assert set([result[1] for result in result_set]) == set(
        [
            "body_1",
            "body_2",
            "body_3",
        ]
    )

    # verify email_date table data
    cursor = db_connection.cursor()
    cursor.execute("select * from email_date")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "temp_message_id_1",
            "temp_message_id_2",
            "temp_message_id_3",
        ]
    )

    assert set([result[1].strftime("%Y-%m-%d") for result in result_set]) == set(
        [
            "2023-07-25",
            "2023-07-24",
            "2023-06-10",
        ]
    )

    # verify label table data
    cursor = db_connection.cursor()
    cursor.execute("select * from label")
    result_set = cursor.fetchall()

    assert set([result[0] for result in result_set]) == set(
        [
            "DUMMY_LABEL_ID_1",
            "DUMMY_LABEL_ID_2",
            "DUMMY_LABEL_ID_3",
        ]
    )

    assert set([result[1] for result in result_set]) == set(
        [
            "DUMMY_LABEL_1",
            "DUMMY_LABEL_2",
            "DUMMY_LABEL_3",
        ]
    )
