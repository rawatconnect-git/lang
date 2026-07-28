import pytest
import time

from agent.agent import user_lookup
from utils.excel_reader import get_user_lookup_data
from evaluators.result_logger import log_result


test_data = get_user_lookup_data()


@pytest.mark.parametrize(
    "data",
    test_data,
    ids=[row["test_id"] for row in test_data]
)
def test_user_lookup(data):

    start_time = time.time()

    status = "PASS"
    error = ""

    try:

        actual_result = user_lookup.invoke(
            {
                "username": data["username"]
            }
        )

        expected_result = data["expected_result"]

        assert actual_result == expected_result, \
            f"Test ID: {data['test_id']} | Expected: {expected_result} | Actual: {actual_result}"

    except AssertionError as e:

        status = "FAIL"
        error = str(e)

        raise

    except Exception as e:

        status = "FAIL"
        error = str(e)

        actual_result = "EXCEPTION"
        expected_result = data["expected_result"]

        raise

    finally:

        execution_time = round(
            time.time() - start_time,
            3
        )

        log_result(
            test_id=data["test_id"],
            input_data=data["username"],
            expected=expected_result,
            actual=actual_result,
            status=status,
            execution_time=execution_time,
            tool_name="user_lookup",
            error=error
        )