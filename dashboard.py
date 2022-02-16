import streamlit as st
import streamlit_authenticator as stauth
from google.cloud import bigquery
from google.oauth2 import service_account
import json
import pandas as pd
from pprint import pprint

credentials = service_account.Credentials.from_service_account_file("dashboard-service-account-key.json")
bigquery_client = bigquery.Client(credentials=credentials)

def get_data(user):
    project_id = "adept-insight-335504"
    dataset_id = "dashboard_antartica"
    env = f"{project_id}.{dataset_id}"
    query = f"""SELECT 
                    re.end, re.amount, ri.name 
                FROM {env}.rewards re 
                INNER JOIN {env}.riggs ri 
                    ON re.rigg_id = ri.id
                INNER JOIN {env}.users_access us 
                    ON ri.id = us.rigg_id
                WHERE us.mail = '{user}'
                ;"""

    try:
        query_job = bigquery_client.query(query)
        # print("===== bbbbb  ===== \n \n ======= bbbbb =====")
        return query_job.result()
    except Exception as e:
        # print("Error")
        # print(e)
        # print("===== ahahhaha a===== \n \n ======= aofjda =====")
        return None


def main(user):
    bq_data = get_data(user)
    st.write(f"Welcome {user}")
    st.title("Antartica Dashboard")

    riggs = set()
    data = []
    for row in bq_data:
        riggs.add(row[2])
        data.append({"time": row[0].replace(tzinfo=None), "reward": row[1], "rigg_id":row[2]})

    if data:
        chart_data = pd.json_normalize(data).set_index("time")
        rigg = st.selectbox("Select rigg", list(riggs))
        st.line_chart(chart_data.loc[chart_data.rigg_id==rigg, "reward"])
    else:
        st.write(f"{user} has no data")



names = ['matedennehy@gmail.com','mineriaantartica@gmail.com', 'test1']
usernames = ['matedennehy@gmail.com','mineriaantartica@gmail.com', 'test1']
passwords = ['antartica_mate','mineria_antartica', 'test1']

hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names, usernames, hashed_passwords, 'some_cookie_name','some_signature_key', cookie_expiry_days=1)

name, authentication_status = authenticator.login('Comercial Antartica', 'main')

if st.session_state['authentication_status']:
    main(st.session_state["name"])
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
