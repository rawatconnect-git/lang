import pytest

from agent.agent import graph
from utils.excel_reader import get_workflow_data


test_data = get_workflow_data()


@pytest.mark.parametrize(
    "data",
    test_data
)
def test_workflow(data):

    result = graph.invoke(
        {
            "user_input": data["user_input"],
            "execution_path": []
        }
    )

    actual_path = result[
        "execution_path"
    ]

    expected_path = [
        node.strip()
        for node in
        data["expected_workflow"].split(",")
    ]

    assert actual_path == expected_path