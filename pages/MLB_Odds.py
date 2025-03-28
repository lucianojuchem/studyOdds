import pandas as pd
import gspread as gs
import streamlit as st
from google.oauth2.service_account import Credentials
import plotly.express as px

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

def analyze_handicap(filtered_data):
    filtered_data["diff_runs"] = filtered_data["HomeRuns"] - filtered_data["AwayRuns"]
    filtered_data["handicap_win"] = filtered_data["diff_runs"] * (-1) + 1
    
    handicap_counts = filtered_data["handicap_win"].value_counts().sort_index()

    # Contagem de handicap positivo e negativo
    positive_handicap = len(filtered_data[filtered_data["handicap_win"] >= 0])
    negative_handicap = len(filtered_data[filtered_data["handicap_win"] < 0])
    
    return handicap_counts, positive_handicap, negative_handicap

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
gc = gs.authorize(creds)

urlSheet = "https://docs.google.com/spreadsheets/d/1GWj9aNoCO57hW97vu9gJb0XESbisyOjE_8vcZ-G7H-c/edit?gid=1552921644#gid=1552921644"

dados = gc.open_by_url(urlSheet).worksheet("Matches")

data = dados.get_all_values()

data = pd.DataFrame(data)

data.columns = data.iloc[0]
data = data[1:].reset_index(drop=True)
data["OddsHome"] = data["OddsHome"].str.replace(",", ".").astype(float)
data["OddsAway"] = data["OddsAway"].str.replace(",", ".").astype(float)
data["HomeRuns"] = data["HomeRuns"].astype(int)
data["AwayRuns"] = data["AwayRuns"].astype(int)

# Criar a coluna de resultado
data["Result"] = data.apply(lambda row: "H" if row["HomeRuns"] > row["AwayRuns"] else "A", axis=1)

st.sidebar.header("Filtros")
option = st.sidebar.radio("Selecione o tipo de jogo:", ["Home", "Away"], horizontal=True)
min_odd = st.sidebar.number_input("Odd mínima:", min_value= 1.01, value=1.01, step=0.01)
max_odd = st.sidebar.number_input("Odd máxima:", min_value= 1.01, value= 10.0, step=0.01)
odd_media = (min_odd + max_odd) / 2
st.sidebar.write(f"Odd Média do Filtro: {odd_media:.2f}")

teams = st.sidebar.multiselect("Selecione as franquias:", options=sorted(data["HomeTeam"].unique()))

# Filtragem dos dados
if option == "Home":
    filtered_data = data[(data["OddsHome"] >= min_odd) & (data["OddsHome"] <= max_odd)]
    if teams:
        filtered_data = filtered_data[filtered_data["HomeTeam"].isin(teams)]
else:
    filtered_data = data[(data["OddsAway"] >= min_odd) & (data["OddsAway"] <= max_odd)]
    if teams:
        filtered_data = filtered_data[filtered_data["AwayTeam"].isin(teams)]


# Levantamento de frequência, porcentagem e odds por resultado
total_games = len(filtered_data)
result_counts = filtered_data["Result"].value_counts()
result_percentages = result_counts / total_games * 100
result_odds = total_games / result_counts

# Separar valores para H e A
h_freq = result_counts.get("H", 0)
a_freq = result_counts.get("A", 0)
h_perc = result_percentages.get("H", 0)
a_perc = result_percentages.get("A", 0)
h_odd = result_odds.get("H", 0)
a_odd = result_odds.get("A", 0)

st.header("Análise de Resultados da MLB 2023 e 2024 (incluindo Playoffs)")

st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #061c96; border-radius: 25px;">
        <h4 style="color: white;;font-size: 24px">Total de Jogos Filtrados</h4>
        <h1 style="color: white;; font-size: 35px;">{total_games}</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Resultados")

col1, col2 = st.columns(2)
    
with col1:
        st.markdown(
        f"""
        <div style="text-align: center; background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;"> Vitórias Home</h4>
            <p style="color: white; font-size: 24px; margin: 0;">{h_freq}</p>
            <p style="color: white;font-size: 20px; margin: 0;"> {h_perc:.2f} %</p>
            <p style="color: white;font-size: 20px; margin: 0;"> Odd Justa: {h_odd:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
        st.markdown(
        f"""
        <div style="text-align: center; background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;"> Vitórias Away</h4>
            <p style="color: white; font-size: 24px; margin: 0;">{a_freq}</p>
            <p style="color: white;font-size: 20px; margin: 0;"> {a_perc:.2f} %</p>
            <p style="color: white;font-size: 20px; margin: 0;"> Odd Justa: {a_odd:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Analisando handicap
total_handicap, positive_handicap, negative_handicap = analyze_handicap(filtered_data)
pos_porcent = 0
neg_porcent = 0

if total_games > 0:
      pos_porcent = positive_handicap / total_games * 100
      neg_porcent = negative_handicap / total_games * 100
else: st.subheader("Não há jogos filtrados com esses critérios. Revise seus filtros!")

st.subheader("Handicaps")

col1, col2 = st.columns(2)
    
with col1:
        st.markdown(
        f"""
        <div style="text-align: center; background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;"> Handicap - </h4>
            <p style="color: white; font-size: 24px; margin: 0;">{negative_handicap}</p>
            <p style="color: white; font-size: 24px; margin: 0;">{neg_porcent:.2f} %</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
        st.markdown(
        f"""
        <div style="text-align: center; background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;"> Handicap + </h4>
            <p style="color: white; font-size: 24px; margin: 0;">{positive_handicap}</p>
            <p style="color: white; font-size: 24px; margin: 0;">{pos_porcent:.2f} %</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# Exibir análise de handicap
st.write("### Gráfico de Handicap")
handicap_df = total_handicap.reset_index()
handicap_df.columns = ['Handicap', 'Frequência']  # Renomeando colunas para melhor compreensão

# Usando o índice correto no gráfico
fig = px.bar(handicap_df, x="Handicap", y="Frequência", labels={"Handicap": "Handicap", "Frequência": "Frequência"}, title="Distribuição de Handicap")
st.plotly_chart(fig)

# Exibir os dados filtrados
st.write("### Jogos Filtrados")
st.dataframe(filtered_data[["Season","HomeTeam","AwayTeam","HomeRuns","AwayRuns","diff_runs","handicap_win"]])
