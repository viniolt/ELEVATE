# Análise de Picks e Bans - VCB

Este projeto é uma ferramenta de análise e simulação para a fase de Picks e Bans (escolha e banimento de mapas) de partidas competitivas de Valorant, com um foco específico na análise da equipe FURIA para um confronto contra a Elevate no VCB (VALORANT Champions Tour Brazil).

A ferramenta utiliza dados históricos de partidas para analisar as preferências de mapa da FURIA e oferece um dashboard interativo para simular o processo de veto de mapas, ajudando na preparação estratégica para uma partida no formato MD3 (melhor de três).

## 📜 Visão Geral do Projeto

O objetivo principal é prever os mapas mais prováveis de serem jogados em uma partida contra a FURIA, com base em suas tendências passadas de picks e bans. O projeto é dividido em duas partes principais: a coleta e análise de dados, e um dashboard de simulação interativo.

## ✨ Funcionalidades

  * **Análise de Frequência**: Gráficos que mostram a frequência com que a FURIA baniu ou escolheu cada mapa em seus jogos recentes (últimos 3, 5 e 90 dias).
  * **Simulação de Veto (Pick/Ban)**: Uma ferramenta interativa para simular o processo de escolhas e banimentos de mapas para uma série MD3.
  * **Configuração de Estratégia**: Permite que o usuário defina a estratégia de sua própria equipe (definindo seus bans e pick) para ver como isso impacta o resultado do veto.
  * **Análise Preditiva**: Com base em milhares de simulações, o dashboard calcula as probabilidades de cada mapa ser o "Decider" (o mapa final restante), a frequência de picks individuais e as combinações de mapas mais prováveis para a série.
  * **Coleta de Dados**: Um notebook Jupyter (`furia.ipynb`) está incluído para consultar a API da GRID.gg e baixar dados detalhados de partidas da FURIA.

## 🗂️ Componentes do Projeto

O projeto é composto pelos seguintes arquivos principais:

  * **`dashboard.py`**: O arquivo principal que executa o dashboard interativo usando a biblioteca Streamlit. Ele contém a lógica de simulação e a interface do usuário para análise preditiva.
  * **`picksnbans.ipynb`**: Um notebook Jupyter para a análise exploratória de dados. Ele calcula e visualiza as frequências de picks e bans de mapas da FURIA com base em dados históricos, servindo como base para as probabilidades usadas no dashboard.
  * **`furia.ipynb`**: Um notebook Jupyter focado na coleta de dados. Ele contém scripts para fazer requisições à API da GRID.gg, buscar IDs de séries de partidas da FURIA e baixar os arquivos de dados correspondentes (end-state e eventos).

## 🚀 Como Usar

Para executar o dashboard de simulação, você precisa ter Python e as dependências do projeto instaladas.

### **Pré-requisitos**

  * Python 3.x
  * Bibliotecas: `streamlit`, `pandas`, `matplotlib`, `requests`, `python-box`.

Você pode instalar as dependências com o pip:

```bash
pip install streamlit pandas matplotlib requests python-box
```

### **Executando o Dashboard**

1.  Navegue até o diretório do projeto no seu terminal.
2.  Execute o seguinte comando:
    ```bash
    streamlit run dashboard.py
    ```
3.  O dashboard será aberto no seu navegador.

### **Utilizando a Simulação**

1.  Na barra lateral do dashboard, você encontrará a seção **"⚙️ Configurações da Simulação"**.
2.  **Defina a Sua Estratégia**: Escolha o primeiro e o segundo mapa que sua equipe irá banir e o mapa que sua equipe irá escolher.
3.  **Ajuste as Probabilidades da FURIA**: Modifique as probabilidades de a FURIA banir ou escolher cada mapa. Os valores padrão são baseados na análise dos últimos 5 jogos da equipe.
4.  **Execute a Simulação**: Defina o número de simulações a serem executadas e observe os resultados, que são atualizados em tempo real.

Os gráficos mostrarão as combinações de mapas mais prováveis, a chance de cada mapa ser o decider e a frequência de picks, ajudando a visualizar os cenários mais prováveis para a partida.
