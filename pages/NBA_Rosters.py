import streamlit as st
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import CommonTeamRoster, PlayerGameLog
from functions import get_team_roster as getTeamRoster
from functions import get_player_gamelog as playerGamelog

# Função para obter o roster da equipe selecionada
# def get_team_roster(team_id, season):
#     roster = CommonTeamRoster(team_id=team_id, season=season)
#     roster_data = roster.get_data_frames()[0]
#     return roster_data

# Função para obter os dados de jogo de um jogador
# def get_player_gamelog(player_id, season):
#     gamelog = PlayerGameLog(player_id=player_id, season=season)
#     return gamelog.get_data_frames()[0]

# Função para calcular frequências, porcentagens, odds e desvio padrão para a análise de overs
def calculate_over_analysis(data, column, total_games, threshold):
    over_count = (data[column] >= threshold).sum()
    std_dev = data[column].std()  # Cálculo do desvio padrão
    
    freq_df = pd.DataFrame({
        'Total Jogos': [total_games],
        'Frequência': [over_count],
        'Porcentagem': [(over_count / total_games * 100).round(1)],
        'Odds': [(total_games / over_count).round(2) if over_count > 0 else None],
        'Desvio Padrão': [std_dev.round(2)],  # Adiciona o desvio padrão à tabela
    })
    return freq_df

# Função para exibir a tabela com estilo
def display_styled_table(data):
    styled_table = '<div style="display: flex; flex-direction: row; gap: 10px;">'
    for _, row in data.iterrows():
        styled_table += f'''
        <div style="background-color: #4CAF50;text-align: center; font-size: 24px; color: white; padding: 20px; border-radius: 5px; flex: 1;">
            <strong> {row['Total Jogos']} jogos na temporada</strong><br>
            <strong>{row['Frequência']} ocorrências</strong><br>
            <strong>{row['Porcentagem']}%</strong> <br>
            <strong>Odd: {row['Odds']} </strong> <br>
            <strong>Desvio Padrão <br> {row['Desvio Padrão']}</strong> 
        </div>
        '''
    styled_table += '</div>'
    st.markdown(styled_table, unsafe_allow_html=True)


# Obter as equipes da NBA
nba_teams = teams.get_teams()
team_names = {team['full_name']: team['id'] for team in nba_teams}

# Título da página
st.title("Análise de Jogadores da NBA")

#Selecionar Temporada
selected_season = st.sidebar.selectbox("Selecione uma temporada",options=['2024-25','2023-24','2022-23','2021-22'])

# Selecionar uma equipe
selected_team = st.sidebar.selectbox("Selecione uma equipe da NBA", options=list(sorted(team_names.keys())))

# Obter o ID da equipe selecionada
team_id = team_names[selected_team]

# Obter o roster da equipe
roster_data = getTeamRoster(team_id, selected_season)

# Selecionar um jogador
selected_player = st.sidebar.selectbox("Selecione um jogador", options=sorted(roster_data['PLAYER'].tolist()))
player_id = roster_data.loc[roster_data['PLAYER'] == selected_player, 'PLAYER_ID'].values[0]

# Obter os dados de jogo do jogador
gamelog_data = playerGamelog(player_id, selected_season)

# Gerar análises para estatísticas selecionadas
if not gamelog_data.empty:
    totalgames = len(gamelog_data)
    st.write(f"Total de {totalgames} partidas para {selected_player}")

    # Selecionar uma estatística para análise
    analyze_statistic = st.selectbox("Selecione uma estatística para análise", options=['PTS', 'REB', 'AST', 'FG3M'])

    if analyze_statistic == 'PTS':
        threshold = st.number_input("Defina o número de pontos para análise", min_value=0, value=5, step=5, max_value=150)
        freq_points_df = calculate_over_analysis(gamelog_data, 'PTS', totalgames, threshold)

        st.subheader(f"Análise de pontos para {selected_player} : {threshold} + PTS ")
        display_styled_table(freq_points_df)
        
        # Gráfico de frequência para pontos
        st.write("Gráfico com frêquencias  de PONTOS")
        st.bar_chart(gamelog_data['PTS'].value_counts())

    elif analyze_statistic == 'REB':
        threshold = st.number_input("Defina o número de rebotes para análise", min_value=0, value=1)
        freq_rebounds_df = calculate_over_analysis(gamelog_data, 'REB', totalgames, threshold)

        st.subheader(f"Análise de rebotes para {selected_player} : {threshold} + REB")
        display_styled_table(freq_rebounds_df)
        
        # Gráfico de frequência para rebotes
        st.write("Gráfico com frêquencias  de REBOTES")
        st.bar_chart(gamelog_data['REB'].value_counts())

    elif analyze_statistic == 'AST':
        threshold = st.number_input("Defina o número de assistências para análise ", min_value=0, value=1)
        freq_assists_df = calculate_over_analysis(gamelog_data, 'AST', totalgames, threshold)

        st.subheader(f"Análise de assistências para {selected_player} : {threshold} + AST")
        display_styled_table(freq_assists_df)
        
        # Gráfico de frequência para assistências
        st.write("Gráfico com frêquencias  de ASSISTÊNCIAS")
        st.bar_chart(gamelog_data['AST'].value_counts())

    elif analyze_statistic == 'FG3M':
        threshold = st.number_input("Defina o número de cestas de 3 pontos para análise", min_value=0, value=1)
        freq_3pm_df = calculate_over_analysis(gamelog_data, 'FG3M', totalgames, threshold)

        st.subheader(f"Análise de bolas de 3 pontos para {selected_player} : {threshold} + 3PTS")
        display_styled_table(freq_3pm_df)
        
        # Gráfico de frequência para cestas de 3 pontos
        st.write("Gráfico com frêquencias  de 3 PONTOS")
        st.bar_chart(gamelog_data['FG3M'].value_counts())

