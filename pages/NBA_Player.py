import streamlit as st
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import players
import pandas as pd
import numpy as np

# Função para buscar jogadores
def search_players(active_only=False):
    all_players = players.get_players()
    if active_only:
        active_players = [player for player in all_players if player['is_active']]
        return active_players
    else:
        return all_players

# Função para buscar o ID do jogador pelo nome completo
def get_player_id(player_name, player_list):
    player = [player for player in player_list if player['full_name'].lower() == player_name.lower()]
    if player:
        return player[0]['id']
    else:
        return None

# Função para buscar as temporadas do jogador
def get_player_seasons(player_id):
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    seasons = info.get_data_frames()[0]['FROM_YEAR'].values[0], info.get_data_frames()[0]['TO_YEAR'].values[0]
    return list(range(int(seasons[0]), int(seasons[1]) + 1))

# Função para buscar os boxscores
def get_player_boxscores(player_id, season='2023'):
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = gamelog.get_data_frames()[0]  # Converte para DataFrame
    return df

# Função para calcular médias
def calculate_averages(df, columns):
    return df[columns].mean()

# Função para calcular médias dos últimos 5 ou 10 jogos
def calculate_last_n_games_average(df, columns, n):
    return df[columns].tail(n).mean()

# Streamlit interface
st.title("Análise de Jogadores da NBA")

# Checkbox para selecionar se deseja exibir apenas jogadores ativos
active_only = st.checkbox("Mostrar apenas jogadores ativos", value=True)

# Buscar lista de todos os jogadores (com base no checkbox)
nba_players = search_players(active_only=active_only)

# Lista de nomes dos jogadores
player_names = sorted([player['full_name'] for player in nba_players])

# Campo de seleção de jogador
selected_player_name = st.selectbox("Selecione um jogador", player_names)

# Buscar o ID do jogador selecionado
player_id = get_player_id(selected_player_name, nba_players)

if player_id:
    # Buscar as temporadas disponíveis para o jogador
    available_seasons = get_player_seasons(player_id)
    
    # Ordenar as temporadas em ordem decrescente
    available_seasons = sorted(available_seasons, reverse=True)
    
    season = st.selectbox("Selecione a temporada", available_seasons)

    # Buscar os boxscores do jogador na temporada selecionada
    df = get_player_boxscores(player_id, str(season))

    if not df.empty:
        # Exibir número de partidas disputadas na temporada
        total_games = len(df)
        st.subheader(f"{selected_player_name} disputou {total_games} partidas na temporada {season}")

        # Selecionar estatísticas para análise
        stats_options = ['PTS', 'AST', 'REB', 'FG3M','FG3A', 'STL', 'BLK', 'TOV','MIN']
        selected_stat = st.selectbox("Selecione a estatística para o gráfico de frequência", stats_options)

        # Exibir gráfico de frequência para a estatística selecionada
        st.subheader(f"Frequência de {selected_stat}")
        st.bar_chart(df[selected_stat].value_counts().sort_index())

        # Definir as faixas de pontos
        point_thresholds = [5, 10, 15, 20, 25, 30, 35, 40]  # Faixas de 5 em 5 até 40
        games_in_ranges = []

        # Calcular a quantidade de jogos em cada faixa
        for threshold in point_thresholds:
            count = df[df['PTS'] >= threshold].shape[0]
            games_in_ranges.append(count)

        # Criar um DataFrame para exibir os resultados
        ranges_df = pd.DataFrame({
            'Faixa de Pontos': [f"{threshold}+" for threshold in point_thresholds],
            'Jogos': games_in_ranges,
        })

        # Calcular a frequência relativa
        total_games = df.shape[0]
        ranges_df['Frequência Relativa (%)'] = (ranges_df['Jogos'] / total_games * 100).round(1)
        ranges_df['Odds'] = (100 / ranges_df['Frequência Relativa (%)']).round(2)
        ranges_df.set_index('Faixa de Pontos', inplace=True)
               
        # Médias da temporada
        season_averages = calculate_averages(df, stats_options).round(1)       

        # Médias dos últimos 3 jogos
        if total_games >= 3:           
            last_3_games_avg = calculate_last_n_games_average(df, stats_options, 3).round(1)
        else:
            st.write("Menos de 3 jogos disputados na temporada.")

        # Médias dos últimos 5 jogos
        if total_games >= 5:
            
            last_5_games_avg = calculate_last_n_games_average(df, stats_options, 5).round(1)
           
        else:
            st.write("Menos de 5 jogos disputados na temporada.")

        # Médias dos últimos 10 jogos
        if total_games >= 10:
            last_10_games_avg = calculate_last_n_games_average(df, stats_options, 10).round(1)
        else:
            st.write("Menos de 10 jogos disputados na temporada.")

        # Exibir médias gerais e últimas médias de forma mais visual
        st.subheader("Médias Gerais e Recente dos Jogos")

        # Criar colunas para mostrar as médias
        col1, col2, col3, col4 = st.columns(4)

        # Exibir as médias da temporada
        with col1:
            st.subheader("Temporada Total")
            for stat in stats_options:
                st.metric(label=stat, value=season_averages[stat])

        # Exibir as médias dos últimos 3 jogos (se houver)
        if total_games >= 3:
            with col2:
                st.subheader("Últimos 3 Jogos")
                for stat in stats_options:
                    delta_value = (last_3_games_avg[stat] - season_averages[stat]).round(1)
                    st.metric(label=stat, value=last_3_games_avg[stat], delta=delta_value)
        else:
            col2.write("Menos de 3 jogos.")

        # Exibir as médias dos últimos 5 jogos (se houver)
        if total_games >= 5:
            with col3:
                st.subheader("Últimos 5 Jogos")
                for stat in stats_options:
                    delta_value = (last_5_games_avg[stat] - season_averages[stat]).round(1)
                    st.metric(label=stat, value=last_5_games_avg[stat], delta=delta_value)
        else:
            col3.write("Menos de 5 jogos.")

        # Exibir as médias dos últimos 10 jogos (se houver)
        if total_games >= 10:
            with col4:
                st.subheader("Últimos 10 Jogos")
                for stat in stats_options:
                    delta_value = (last_10_games_avg[stat] - season_averages[stat]).round(1)
                    st.metric(label=stat, value=last_10_games_avg[stat], delta=delta_value)
        else:
            col4.write("Menos de 10 jogos.")

        #st.dataframe(df)  
    else:
        st.write(f"Sem dados disponíveis para a temporada {season}.")
else:
    st.write(f"Erro ao buscar o jogador {selected_player_name}.")
