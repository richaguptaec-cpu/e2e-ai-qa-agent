import pandas as pd
import json


def create_excel(testcase_json):

    data = json.loads(testcase_json)

    rows = []

    for tc in data["test_cases"]:

        rows.append({
            "Test ID": tc["test_id"],
            "Title": tc["title"],
            "Type": tc["type"],
            "Priority": tc["priority"],
            "Precondition": tc["precondition"],
            "Steps": "\n".join(tc["steps"]),
            "Expected Result": tc["expected_result"]
        })

    df = pd.DataFrame(rows)

    file_path = "exports/testcases.xlsx"

    df.to_excel(
        file_path,
        index=False
    )

    return file_path