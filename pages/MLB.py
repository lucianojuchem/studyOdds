import pandas as pd
import gspread as gs
import streamlit as st
from google.oauth2.service_account import Credentials

credentials_json = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain" : st.secrets["universe_domain"]
}

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
gc = gs.authorize(creds)

urlSheet = "https://docs.google.com/spreadsheets/d/1GWj9aNoCO57hW97vu9gJb0XESbisyOjE_8vcZ-G7H-c/edit?gid=1552921644#gid=1552921644"

dados = gc.open_by_url(urlSheet).worksheet("Matches")
equipes = gc.open_by_url(urlSheet).worksheet("Teams")


teams = equipes.get_all_values()
data = dados.get_all_values()

data = pd.DataFrame(data)
teams = pd.DataFrame(teams)

st.dataframe(data)
