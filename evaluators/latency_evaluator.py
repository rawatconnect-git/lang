"""
Latency Evaluator

Purpose:
Checks whether the execution time of a test is within the
acceptable threshold (SLA).
"""


def evaluate_latency(execution_time, threshold=1.0):
    """
    Evaluate execution latency.

    Args:
        execution_time (float): Actual execution time in seconds.
        threshold (float): Maximum allowed execution time.

    Returns:
        dict:
        {
            "status": "PASS" or "FAIL",
            "message": "<evaluation message>"
        }
    """

    if execution_time <= threshold:
        return {
            "status": "PASS",
            "message": (
                f"Execution time {execution_time:.3f}s "
                f"is within threshold ({threshold}s)."
            )
        }

    return {
        "status": "FAIL",
        "message": (
            f"Execution time {execution_time:.3f}s "
            f"exceeded threshold ({threshold}s)."
        )
    }