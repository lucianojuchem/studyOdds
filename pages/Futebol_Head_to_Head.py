import streamlit as st
import pandas as pd

def carregar_dados():
    # Substitua pelo caminho correto do seu dataset
    df = pd.read_csv("FootballData.csv")
    df['Score'] = df['FTHG'].astype(str) + 'x' + df['FTAG'].astype(str)
    return df

def filtrar_dados(df, equipe_casa, equipe_fora, filtro_local):
    df_filtrado = df
    
    if filtro_local == "Todos":
        df_filtrado = df_filtrado[((df_filtrado['HomeTeam'] == equipe_casa) & (df_filtrado['AwayTeam'] == equipe_fora)) |
                                  ((df_filtrado['HomeTeam'] == equipe_fora) & (df_filtrado['AwayTeam'] == equipe_casa))]
    else:
        df_filtrado = df_filtrado[(df_filtrado['HomeTeam'] == equipe_casa) & (df_filtrado['AwayTeam'] == equipe_fora)]
    
    return df_filtrado

def criar_colunas_over_under_gols(data):
    # Criar a coluna 'Total Gols'
    data['Total Gols'] = data['FTHG'] + data['FTAG']
    
    # Criar colunas de Over e Under Gols de 0.5 até 7.5
    for over in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]:
        data[f'Over_{over}'] = (data['Total Gols'] > over).astype(int)
        data[f'Under_{over}'] = (data['Total Gols'] < over).astype(int)
    
    return data

def analisar_over_under_gols(data):
    resultados_over_under_gols = {}
    total_jogos = len(data)
    
    for over in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]:
        resultados_over_under_gols[f'Over_{over}'] = {
            'Ocorrência': data[f'Over_{over}'].sum(),
            'Frequência (%)': round(data[f'Over_{over}'].mean() * 100,2),
            'Odds': round(1 / data[f'Over_{over}'].mean(), 2) if data[f'Over_{over}'].mean() > 0 else 0
        }
        resultados_over_under_gols[f'Under_{over}'] = {
            'Ocorrência': data[f'Under_{over}'].sum(),
            'Frequência (%)': round(data[f'Under_{over}'].mean() * 100,2),
            'Odds': round(1 / data[f'Under_{over}'].mean(), 2) if data[f'Under_{over}'].mean() > 0 else 0
        }
    
    return resultados_over_under_gols


# Função para contar os resultados
def count_results(data, equipe_casa, equipe_fora):
    total_games = len(data)

    # Inicializando as vitórias
    home_wins = 0
    away_wins = 0
    draws = 0

    # Contagem de vitórias e empates
    for _, row in data.iterrows():
        if row['HomeTeam'] == equipe_casa and row['FTR'] == 'H':  # Vitória em casa para equipe_casa
            home_wins += 1
        elif row['AwayTeam'] == equipe_casa and row['FTR'] == 'A':  # Vitória fora para equipe_casa
            home_wins += 1
        elif row['HomeTeam'] == equipe_fora and row['FTR'] == 'H':  # Vitória em casa para equipe_fora
            away_wins += 1
        elif row['AwayTeam'] == equipe_fora and row['FTR'] == 'A':  # Vitória fora para equipe_fora
            away_wins += 1
        elif row['FTR'] == 'D':  # Empate
            draws += 1


    results = {
        'Vitórias da Casa': {
            'Contagem': home_wins,
            'Porcentagem': (home_wins / total_games) * 100 if total_games > 0 else 0,
            'Odds Decimais': 1 / (home_wins / total_games) if home_wins > 0 else 0
        },
        'Empates': {
            'Contagem': draws,
            'Porcentagem': (draws / total_games) * 100 if total_games > 0 else 0,
            'Odds Decimais': 1 / (draws / total_games) if draws > 0 else 0
        },
        'Vitórias do Visitante': {
            'Contagem': away_wins,
            'Porcentagem': (away_wins / total_games) * 100 if total_games > 0 else 0,
            'Odds Decimais': 1 / (away_wins / total_games) if away_wins > 0 else 0
        },
    }
    return results


def create_metric(title, value, frequency, odds, color):
    return f"""
    <div style="background-color: {color}; padding: 10px; border-radius: 25px;text-align: center; width: 240px; height: 180px; margin: 10px; padding: 10px;">
        <h3 style="font-size: 22px; margin: 0;">{title}</h3>
        <p style="font-size: 20px; margin: 5px 0;">{value} jogos</p>
        <p style="font-size: 20px; margin: 5px 0;">{frequency}</p>
        <p style="font-size: 20px; margin: 5px 0;">Odd: {odds}</p>
    </div>
    """


def count_score_frequencies(data):
    score_counts = data['Score'].value_counts().reset_index()
    score_counts.columns = ['Score', 'Frequência']
    score_counts['Porcentagem'] = (score_counts['Frequência'] / len(data)) * 100
    score_counts['Odd'] = 100 / score_counts['Porcentagem']  
    return score_counts


def display_score_results(score_counts):

    st.subheader('Frequências dos Resultados Corretos')

    # Cria colunas para exibir os resultados em uma grade horizontal
    num_cols = 5  # Número de colunas na grade
    num_rows = (len(score_counts) + num_cols - 1) // num_cols  # Calcula o número de linhas necessárias

    cols = st.columns(num_cols)  # Cria as colunas para exibir os resultados

    # Calcula a intensidade de cor com base na porcentagem máxima
    max_percentage = score_counts['Porcentagem'].max()

    for i in range(num_rows):
        for j in range(num_cols):
            index = i * num_cols + j
            if index < len(score_counts):
                score = score_counts.iloc[index]['Score']
                frequency = score_counts.iloc[index]['Frequência']
                percentage = score_counts.iloc[index]['Porcentagem']
                odd = score_counts.iloc[index]['Odd']

                # Calcula a cor com base na porcentagem
                color_intensity = int((percentage / max_percentage) * 150)
                color = f'rgb({200 - color_intensity}, {color_intensity}, 50)'

                with cols[j]:
                    st.markdown(
                        f"""
                        <div style="text-align: center; background-color: {color}; color: white; width: 200px; height: 160px; 
                        text-align: center; justify-content: center; margin: 5px; font-size: 22px; border-radius: 25px; padding: 10px;">
                            <strong>{score}</strong><br>
                            <span style="font-size: 18px;">Frequência: {frequency}<br> {percentage:.2f}%<br> Odd: {odd:.2f} </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

st.title("Análise Head to Head no Futebol")

df = carregar_dados()

equipes = df['HomeTeam'].unique()

equipe_casa = st.selectbox("Selecione a equipe da casa", equipes, index=18)
equipe_fora = st.selectbox("Selecione a equipe visitante", equipes, index=8)

filtro_local = st.radio("Filtrar por", ["Todos", "Casa/Fora"], horizontal=True, )

df_filtrado = filtrar_dados(df, equipe_casa, equipe_fora, filtro_local)


results = count_results(df_filtrado, equipe_casa, equipe_fora)

total_games = len(df_filtrado)
st.markdown(f"""
    <div style="text-align: center; padding: 0px; background-color: #061c96; border-radius: 25px;">
        <h4 style="color: white; font-size: 24px">Total de Confrontos</h4>
        <h1 style="color: white; font-size: 30px;">{total_games}</h1>
    </div>
""", unsafe_allow_html=True)

# Exibir Resultados com uma apresentação melhorada
st.subheader("Resultados para Análise")

# Criar colunas para exibir os resultados horizontalmente
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="text-align: center; background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;">Vitórias  {equipe_casa}</h4>
            <p style="color: white; font-size: 24px; margin: 0;">{results['Vitórias da Casa']['Contagem']}</p>
            <p style="color: white;font-size: 20px; margin: 0;"> {results['Vitórias da Casa']['Porcentagem']:.2f}%</p>
            <p style="color: white;font-size: 20px; margin: 0;"> Odd Justa: {results['Vitórias da Casa']['Odds Decimais']:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="text-align: center;background-color:#061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;">Empates</h4>
            <p style="color: white; font-size: 24px; margin: 0;"> {results['Empates']['Contagem']}</p>
            <p style="color: white;font-size: 20px; margin: 0;"> {results['Empates']['Porcentagem']:.2f}%</p>
            <p style="color: white; font-size: 20px; margin: 0;"> Odd Justa: {results['Empates']['Odds Decimais']:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="text-align: center;background-color: #061c96; padding: 10px; border-radius: 25px; margin-bottom: 10px;">
            <h4 style="color: white; margin-bottom: 5px;">Vitórias  {equipe_fora}</h4>
            <p style="color: white; font-size: 24px; margin: 0;"> {results['Vitórias do Visitante']['Contagem']}</p>
            <p style="color: white;font-size: 20px; margin: 0;">  {results['Vitórias do Visitante']['Porcentagem']:.2f}%</p>
            <p style="color: white;font-size: 20px; margin: 0;"> Odd Justa: {results['Vitórias do Visitante']['Odds Decimais']:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

score_counts = count_score_frequencies(df_filtrado)
display_score_results(score_counts)


OverGolsdata = criar_colunas_over_under_gols(df_filtrado)
resultados_over_under_gols = analisar_over_under_gols(OverGolsdata)

st.header('Análise de Over e Under Gols')

# Seção de Over Gols
st.subheader('Análise de Over Gols')
cols_over = st.columns(4)
for i, over in enumerate([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]):
    with cols_over[i % 4]:  # Distribuindo as colunas em múltiplas linhas
        color = "#04b846"  # Gradiente de cor
        st.markdown(create_metric(
            f"Over {over}",
            f"{resultados_over_under_gols[f'Over_{over}']['Ocorrência']}",
            f"{resultados_over_under_gols[f'Over_{over}']['Frequência (%)']}%",
            f"{resultados_over_under_gols[f'Over_{over}']['Odds']}",
            color
        ), unsafe_allow_html=True)

# Seção de Under Gols
st.subheader('Análise de Under Gols')
cols_under = st.columns(4)
for i, under in enumerate([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]):
    with cols_under[i % 4]:  # Distribuindo as colunas em múltiplas linhas
        color = "#FF6347"  # Gradiente de cor
        st.markdown(create_metric(
            f"Under {under}",
            f"{resultados_over_under_gols[f'Under_{under}']['Ocorrência']}",
            f"{resultados_over_under_gols[f'Under_{under}']['Frequência (%)']}%",
            f"{resultados_over_under_gols[f'Under_{under}']['Odds']}",
            color
        ), unsafe_allow_html=True)


st.write("### Confrontos Diretos")
st.dataframe(df_filtrado)
