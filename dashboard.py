import streamlit as st
import pandas as pd
from collections import Counter
import random

st.set_page_config(layout="wide", page_title="Análise de Picks e Bans")

st.title('PICKS E BANS - ELEVATE vs FURIA')
st.header('Análise de frequência dos mapas nos últimos 3 jogos')
st.write('Análise baseada nos últimos 3 confrontos de cada time para a MD3 do VCB.')
st.markdown("---")

bans = ['Ascent', 'Pearl', 'Ascent', 'Pearl', 'Ascent', 'Pearl']
picks = ['Split', 'Lotus', 'Split', 'Lotus', 'Icebox']

bans_90d = ['Ascent', 'Haven', 'Ascent','Ascent', 'Pearl', 'Ascent', 'Pearl', 'Ascent', 'Pearl', 'Split', 'Haven', 'Icebox', 'Pearl', 'Icebox', 'Ascent', 'Pearl', 'Split', 'Pearl', 'Pearl']
picks_90d = ['Pearl', 'Lotus', 'Pearl', 'Split', 'Split', 'Lotus', 'Split', 'Lotus', 'Icebox', 'Pearl', 'Ascent', 'Ascent', 'Haven', 'Split', 'Lotus', 'Haven', 'Pearl', 'Lotus', 'Split', 'Lotus', 'Split']

bans_5series = ['Ascent', 'Pearl', 'Ascent', 'Pearl', 'Ascent', 'Pearl', 'Ascent', 'Ascent']
picks_5series  = ['Split', 'Lotus', 'Split', 'Lotus', 'Icebox', 'Lotus', 'Pearl', 'Split', 'Pearl']



def freq (dados, titulo):
    if not dados:
        st.warning('Não há dados para serem exibidos')
    contador = Counter(dados)
    df = pd.DataFrame(contador.items(), columns=['Mapa', 'Frequência'])
    df = df.set_index('Mapa')  # Define a coluna 'Mapa' como o eixo do gráfico

    # Exibir o título e o gráfico
    st.subheader(f"**{titulo}**")
    st.bar_chart(df['Frequência'])

st.markdown("---")
st.subheader('Últimos 3 jogos da Furia')
freq(bans, 'Bans Furia')
freq(picks, 'Picks & Sobras Furia')

st.markdown("---")
st.subheader('Ultima season da Furia')
freq(bans_90d, 'Bans Furia')
freq(picks_90d, 'Picks & Sobras Furia')

st.markdown("---")
st.subheader('Ultimos 5 jogos da Furia')
freq(bans_5series, 'Bans Furia')
freq(picks_5series, 'Picks & Sobras Furia')

st.markdown("---")
st.subheader('Probabilidades sugeridas')
st.subheader('Ultimos 5 jogos da Furia (sugerido)')
st.text('BANS FURIA\nAscent - 100% \nPearl - 60% \nHaven - 20%')
st.text('PICKS FURIA\nSplit - 60%^\nLotus - 60%\nIcebox - 20%\nPearl - 60%')

MAP_POOL = ['Ascent', 'Pearl', 'Split', 'Lotus', 'Icebox', 'Sunset', 'Haven']
st.sidebar.header('⚙️ Configurações da Simulação')

# --- Controles do Seu Time ---
st.sidebar.subheader('Sua Estratégia')
map_options_ban1 = MAP_POOL.copy()
seu_ban1 = st.sidebar.selectbox('Seu 1º Ban:', map_options_ban1, index=MAP_POOL.index('Sunset'))

map_options_ban2 = [m for m in MAP_POOL if m != seu_ban1]
seu_ban2 = st.sidebar.selectbox('Seu 2º Ban:', map_options_ban2, index=map_options_ban2.index('Split'))

map_options_pick = [m for m in MAP_POOL if m not in [seu_ban1, seu_ban2]]
seu_pick = st.sidebar.selectbox('Seu Pick:', map_options_pick, index=map_options_pick.index('Lotus'))

# --- Controles do Adversário (FURIA) ---
st.sidebar.subheader('Probabilidades da FURIA')
furia_ban_probs = {}
st.sidebar.write("**Probabilidade de Ban**")
for mapa in MAP_POOL:
    # Valores padrão para os sliders
    if mapa in ['Pearl']:
        default_value = 60
    elif mapa in ['Ascent']:
        default_value = 100
    elif mapa in ['Haven']:
        default_value = 20
    else:
        default_value = 0
    furia_ban_probs[mapa] = st.sidebar.slider(f'Ban {mapa}', 0, 100, default_value) / 100.0

furia_pick_probs = {}
st.sidebar.write("**Probabilidade de Pick**")
for mapa in MAP_POOL:
    if mapa in ['Split', 'Lotus', 'Pearl']:
        default_value = 60
    elif mapa in ['Icebox']:
        default_value = 20
    else:
        default_value = 0
    furia_pick_probs[mapa] = st.sidebar.slider(f'Pick {mapa}', 0, 100, default_value) / 100.0

# --- Configurações da Simulação ---
st.sidebar.subheader('Parâmetros da Simulação')
N = st.sidebar.number_input('Número de Simulações:', min_value=100, max_value=10000, value=1000, step=100)


# --- Lógica da Simulação ---
@st.cache_data  # Usar cache para não re-executar a simulação a cada pequena mudança
def run_simulation(_N, _seu_ban1, _seu_ban2, _seu_pick, _furia_ban_probs, _furia_pick_probs):
    pick_count = Counter()
    decider_count = Counter()
    map_combo_count = Counter()  # NOVO: Contador para as combinações de mapas

    for _ in range(_N):
        mapas_disponiveis = MAP_POOL.copy()
        furia_pick_realizado = None
        seu_pick_realizado = None

        # Função auxiliar para fazer uma escolha com base em probabilidades
        def make_choice(options, probs):
            valid_options = [m for m in options if m in probs and probs[m] > 0]
            if not valid_options: return None
            weights = [probs[m] for m in valid_options]
            return random.choices(valid_options, weights=weights, k=1)[0]

        # FASE DE BANS 1
        ban1_furia = make_choice(mapas_disponiveis, _furia_ban_probs)
        if ban1_furia and ban1_furia in mapas_disponiveis: mapas_disponiveis.remove(ban1_furia)

        if _seu_ban1 in mapas_disponiveis: mapas_disponiveis.remove(_seu_ban1)

        # FASE DE PICKS
        furia_pick = make_choice(mapas_disponiveis, _furia_pick_probs)
        if furia_pick and furia_pick in mapas_disponiveis:
            mapas_disponiveis.remove(furia_pick)
            pick_count[furia_pick] += 1
            furia_pick_realizado = furia_pick

        if _seu_pick in mapas_disponiveis:
            mapas_disponiveis.remove(_seu_pick)
            pick_count[_seu_pick] += 1
            seu_pick_realizado = _seu_pick

        # NOVO: Registrar a combinação de picks se ambos ocorreram
        if furia_pick_realizado and seu_pick_realizado:
            # Ordenar para tratar ('A', 'B') e ('B', 'A') como a mesma combinação
            combo = tuple(sorted((furia_pick_realizado, seu_pick_realizado)))
            map_combo_count[combo] += 1

        # FASE DE BANS 2
        ban3_furia = make_choice(mapas_disponiveis, _furia_ban_probs)
        if ban3_furia and ban3_furia in mapas_disponiveis: mapas_disponiveis.remove(ban3_furia)

        if _seu_ban2 in mapas_disponiveis: mapas_disponiveis.remove(_seu_ban2)

        # MAPA DECISIVO
        if len(mapas_disponiveis) == 1:
            decider = mapas_disponiveis[0]
            decider_count[decider] += 1

    return decider_count, pick_count, map_combo_count


# --- Execução e Exibição dos Resultados ---
decider_results, pick_results, combo_results = run_simulation(N, seu_ban1, seu_ban2, seu_pick, furia_ban_probs,
                                                              furia_pick_probs)

st.markdown("---")
st.header('📊 Resultados da Simulação')

# Sumário da estratégia
st.write(f"**Sua Estratégia:** 1º Ban em **{seu_ban1}**, 2º Ban em **{seu_ban2}**, e Pick em **{seu_pick}**.")
st.write(f"Simulando **{N}** confrontos...")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chance de cada mapa ser o Decider")
    if not decider_results:
        st.warning("Nenhum mapa decider foi gerado com as configurações atuais.")
    else:
        decider_df = pd.DataFrame(decider_results.items(), columns=['Mapa', 'Ocorrências'])
        decider_df['Probabilidade (%)'] = (decider_df['Ocorrências'] / N) * 100
        decider_df = decider_df.sort_values('Probabilidade (%)', ascending=False).set_index('Mapa')
        st.bar_chart(decider_df['Probabilidade (%)'])

with col2:
    st.subheader("Frequência de Picks Individuais")
    if not pick_results:
        st.warning("Nenhum mapa foi pickado com as configurações atuais.")
    else:
        # Usamos N como base para a porcentagem de picks, pois cada simulação tem 2 picks.
        pick_df = pd.DataFrame(pick_results.items(), columns=['Mapa', 'Ocorrências'])
        total_picks = sum(pick_df['Ocorrências'])
        pick_df['Probabilidade de ser Pickado (%)'] = (pick_df['Ocorrências'] / N) * 100 if N > 0 else 0
        pick_df = pick_df.sort_values('Probabilidade de ser Pickado (%)', ascending=False).set_index('Mapa')
        st.bar_chart(pick_df['Probabilidade de ser Pickado (%)'])

# --- NOVA VISUALIZAÇÃO: Combinações de Mapas ---
st.markdown("---")
st.header("🎲 Combinações de Mapas Mais Prováveis (Picks da MD3)")
if not combo_results:
    st.warning("Nenhuma combinação de mapas foi gerada com as configurações atuais.")
else:
    # Processa os dados de combinação para o gráfico
    combo_df = pd.DataFrame(combo_results.items(), columns=['Combinação', 'Ocorrências'])
    # Formata a tupla ('MapaA', 'MapaB') para uma string "MapaA & MapaB"
    combo_df['Combinação'] = combo_df['Combinação'].apply(lambda x: f"{x[0]} & {x[1]}")
    combo_df['Probabilidade (%)'] = (combo_df['Ocorrências'] / N) * 100
    combo_df = combo_df.sort_values('Probabilidade (%)', ascending=False).set_index('Combinação')

    st.write(
        "Este gráfico mostra a chance de uma combinação específica de mapas (Seu Pick + Pick da FURIA) acontecer na série.")
    st.bar_chart(combo_df['Probabilidade (%)'])

st.markdown("---")
st.info(
    "💡 **Como interpretar:** O gráfico de **Decider** mostra a probabilidade de um mapa sobrar no final. O de **Picks** a chance de um mapa ser escolhido por qualquer um dos times. O gráfico de **Combinações** mostra a chance de a MD3 ser composta por aquele par de mapas específicos.")

