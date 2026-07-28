import pytest
import time

from agent.agent import router
from utils.excel_reader import get_router_data
from evaluators.result_logger import log_result
from evaluators.latency_evaluator import evaluate_latency


test_data = get_router_data()


@pytest.mark.parametrize(
    "data",
    test_data,
    ids=[row["test_id"] for row in test_data]
)
def test_router_node(data):

    start_time = time.time()

    status = "PASS"
    error = ""
    actual_actions = ""
    expected_actions = ""

    try:
        state = {
            "user_input": data["user_input"]
        }

        result = router(state)

        actual_actions = result["actions"]

        expected_actions = [
            action.strip()
            for action in data["expected_actions"].split(",")
        ]

        assert actual_actions == expected_actions, \
            f"""
            Test ID: {data['test_id']}
            User Input: {data['user_input']}
            Expected Actions: {expected_actions}
            Actual Actions: {actual_actions}
            """

    except AssertionError as e:
        status = "FAIL"
        error = str(e)
        raise

    except Exception as e:
        status = "FAIL"
        error = str(e)
        actual_actions = "EXCEPTION"
        raise

    finally:
        execution_time = round(time.time() - start_time, 3)

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
            expected=str(expected_actions),
            actual=str(actual_actions),
            status=status,
            execution_time=execution_time,
            tool_name="router_node",
            error=error
        )