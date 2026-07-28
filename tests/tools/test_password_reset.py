import pytest

from agent.agent import password_reset
from utils.excel_reader import get_password_reset_data


test_data = get_password_reset_data()


@pytest.mark.parametrize(
    "data",
    test_data,
    ids=[row["test_id"] for row in test_data]
)
def test_password_reset(data):

    actual_result = password_reset.invoke(
        {
            "username": data["username"]
        }
    )

    expected_result = data["expected_result"]

    assert actual_result == expected_result, \
        f"Expected {expected_result} but got {actual_result}"