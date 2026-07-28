import csv
import os

from datetime import datetime


REPORT_FOLDER = "reports/history"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

RESULT_FILE = (
    f"{REPORT_FOLDER}/results_{timestamp}.csv"
)


def log_result(
    test_id,
    input_data,
    expected,
    actual,
    status,
    execution_time,
    tool_name,
    error=""
):

    file_exists = os.path.exists(
        RESULT_FILE
    )

    with open(
        RESULT_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "test_id",
                    "tool_name",
                    "input",
                    "expected",
                    "actual",
                    "status",
                    "execution_time",
                    "error",
                    "execution_date"
                ]
            )

        writer.writerow(
            [
                test_id,
                tool_name,
                input_data,
                expected,
                actual,
                status,
                execution_time,
                error,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ]
        )