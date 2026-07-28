import pytest

from agent.agent import system_status
from utils.excel_reader import get_system_status_data


test_data = get_system_status_data()


@pytest.mark.parametrize(
    "data",
    test_data,
    ids=[row["test_id"] for row in test_data]
)
def test_system_status(data):

    actual_result = system_status.invoke(
        {
            "system_name": data["system_name"]
        }
    )

    expected_result = data["expected_result"]

    assert actual_result == expected_result, \
        f"""
        Test ID: {data['test_id']}
        System Name: {data['system_name']}
        Expected: {expected_result}
        Actual: {actual_result}
        """