import streamlit as st

# Configuração da página
st.set_page_config(page_title="Meu Aplicativo de Análise Esportiva", layout="wide")

# Título da página
st.title("Bem-vindo ao Inteligência Esportiva!")

# Introdução
st.markdown("""
Este aplicativo oferece análises de futebol, tênis e NBA baseadas em dados históricos e estatísticas avançadas. Use o menu lateral para navegar entre as funcionalidades.
            
**Ajude a manter o projeto com mais funcionalidades e melhorias!**
""")

st.image("qrcode-pix.png", caption="Pix de Contribuição ao Projeto", )

# Seção da Página 'Futebol Backtest'
st.header("Futebol Backtest")
st.markdown("""
Na página **Futebol Backtest**, você pode avaliar a performance de estratégias aplicadas a resultados passados, com base em métricas como:

- **Retorno de Estratégias:** Teste e otimize estratégias com base em dados históricos.

Essas análises são feitas para otimizar suas decisões futuras com base em estratégias bem testadas.
""")

# Seção da Página 'Futebol Odds'
st.header("Análises de Futebol pelas Odds")
st.markdown("""
Na página **Futebol Odds**, você encontrará análises detalhadas sobre:

- **Médias de Gols:** Verifique o desempenho ofensivo e defensivo de equipes.
- **Odds Históricas:** Explore padrões de odds e descubra tendências para futuros jogos.
- **Placares Frequentes:** Identifique os resultados mais comuns em diversas ligas.
- **Eficiência nas Finalizações:** Analise a eficácia das equipes em transformar finalizações em gols.

Essas informações ajudam a prever tendências e possíveis comportamentos em jogos futuros.
""")

# Seção da Página 'NBA Player'
st.header("Análise de Jogadores da NBA")
st.markdown("""
Na página **NBA Player**, você pode consultar as estatísticas de jogadores ativos ou inativos da NBA:

- **Estatísticas de Temporadas:** Veja o desempenho de um jogador em cada temporada de sua carreira.

Essas análises são ideais para acompanhar o desenvolvimento dos atletas e avaliar seu impacto nas partidas.
""")

# Seção da Página 'NBA Roster'
st.header("Análises para Apostas em Jogadores da NBA")
st.markdown("""
Na página **NBA Rosters**, você encontrará:

- **Estatísticas de Jogadores por Equipe:** Veja o desempenho atual de jogadores por franquias da NBA.
- **Análise para Apostas:** Utilize as estatísticas para identificar oportunidades de apostas relacionadas a jogadores.

Essas informações ajudam a prever desempenhos e tendências para suas decisões de apostas.
""")

# Seção da Página 'Tennis Odds'
st.header("Análise de Partidas de Tênis")
st.markdown("""
Na página **Tenis Odds**, você encontrará:

- **Odds de Partidas:** Veja como as odds evoluem e influenciam as previsões de resultados.

Use essas análises para tomar decisões mais informadas sobre apostas ou prever resultados de partidas de tênis.
""")

# Seção de Instruções
st.header("Como Usar")
st.markdown("""
1. **Use o menu lateral:** Navegue entre as páginas **Futebol Backtest**, **Futebol Odds**, **NBA Player**, **NBA Roster** e **Tenis Odds**.
2. **Analise os dados:** Utilize as ferramentas para uma análise profunda das partidas e odds.
3. **Faça previsões:** Baseie suas decisões nas previsões e análises oferecidas.

Aproveite a plataforma para insights detalhados em esportes!
""")
