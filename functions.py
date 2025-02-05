from nba_api.stats.endpoints import playergamelog, commonplayerinfo,  CommonTeamRoster, PlayerGameLog
from nba_api.stats.static import players

# Função para buscar jogadores
def search_players(active_only=False):
    all_players = players.get_players()
    if active_only:
        active_players = [player for player in all_players if player['is_active']]
        return active_players
    else:
        return all_players
    
# Função para obter o roster da equipe selecionada
def get_team_roster(team_id, season):
    roster = CommonTeamRoster(team_id=team_id, season=season)
    roster_data = roster.get_data_frames()[0]
    return roster_data

# Função para obter os dados de jogo de um jogador
def get_player_gamelog(player_id, season):
    gamelog = PlayerGameLog(player_id=player_id, season=season)
    return gamelog.get_data_frames()[0]