import pandas as pd
import gspread as gs
import streamlit as st

gc = gs.service_account(filename=FILENAME)

dados = gc.open_by_url("https://docs.google.com/spreadsheets/d/1LyRKhG6ofCX20SEskr4mb00rw0nl38NbQvG_h3aL_0U/edit?gid=1735547126#gid=1735547126").worksheet("BRA")

data = pd.DataFrame()

data = dados.get_all_values()

st.dataframe(data)
