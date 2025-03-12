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

#gc = gs.service_account(filename = credentials_json)

dados = gc.open_by_url("https://docs.google.com/spreadsheets/d/1LyRKhG6ofCX20SEskr4mb00rw0nl38NbQvG_h3aL_0U/edit?gid=1735547126#gid=1735547126").worksheet("BRA")

data = pd.DataFrame()

data = dados.get_all_values()

#st.dataframe(data)
st.subheader("Página em desenvolvimento!")