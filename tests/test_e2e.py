import pytest
import time

from agent.agent import graph
from utils.excel_reader import get_e2e_data
from evaluators.result_logger import log_result
from evaluators.latency_evaluator import evaluate_latency


test_data = get_e2e_data()


@pytest.mark.parametrize(
    "data",
    test_data,
    ids=[row["test_id"] for row in test_data]
)
def test_agent_e2e(data):

    start_time = time.time()

    status = "PASS"
    error = ""

    try:

        result = graph.invoke(
            {
                "user_input": data["user_input"]
            }
        )

        actual_response = str(result)

        expected_response = data["expected_response"]

        assert expected_response.lower() in \
            actual_response.lower(), \
            f"""
            Test ID: {data['test_id']}
            Input: {data['user_input']}
            Expected: {expected_response}
            Actual: {actual_response}
            """

    except AssertionError as e:

        status = "FAIL"
        error = str(e)

        raise

    except Exception as e:

        status = "FAIL"
        error = str(e)

        actual_response = "EXCEPTION"
        expected_response = data["expected_response"]

        raise

    finally:

        execution_time = round(
            time.time() - start_time,
            3
        )

        latency_result = evaluate_latency(
            execution_time=execution_time,
            threshold=1.0
        )

        if latency_result["status"] == "FAIL":
            status = "FAIL"
            error = error + " | " + latency_result["message"]

        log_result(
            test_id=data["test_id"],
            input_data=data["user_input"],
            expected=expected_response,
            actual=actual_response,
            status=status,
            execution_time=execution_time,
            tool_name="e2e_agent",
            error=error
        )