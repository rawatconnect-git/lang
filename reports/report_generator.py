import json


with open(
    "traces/execution_logs.json",
    "r"
) as f:

    results = json.load(f)


total = len(results)

passed = len(
    [
        r
        for r in results
        if r["status"] == "PASS"
    ]
)

failed = total - passed

pass_rate = round(
    (passed / total) * 100,
    2
)