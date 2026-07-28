import pandas as pd


def get_user_lookup_data():

    df = pd.read_excel(
        "datasets/user_lookup.xlsx"
    )

    return df.to_dict("records")

def get_password_reset_data():

    df = pd.read_excel(
        "datasets/password_reset.xlsx"
    )

    return df.to_dict("records")

def get_system_status_data():

    df = pd.read_excel(
        "datasets/system_status.xlsx"
    )

    return df.to_dict("records")

    
def get_router_data():

    df = pd.read_excel(
        "datasets/router_status.xlsx"
    )
    return df.to_dict("records")

def get_workflow_data():

    df = pd.read_excel(
        "datasets/workflow.xlsx"
    )

    return df.to_dict("records")

def get_e2e_data():

    df = pd.read_excel(
        "datasets/e2e_test_data.xlsx"
    )

    return df.to_dict("records")    