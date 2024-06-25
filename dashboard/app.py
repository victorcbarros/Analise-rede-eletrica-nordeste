# importando as bibliotecas 
import pandas as pd
import streamlit as st
import plotly.express as px



# Funções 
def nome_mes(dados):
   meses_portugues = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril', 'May': 'Maio','June': 'Junho',
    'July': 'Julho','August': 'Agosto','September': 'Setembro','October': 'Outubro','November': 'Novembro','December': 'Dezembro'
    }
   dados['Mes'] = dados['InicioInterrupcao'].dt.month_name()
   dados['Mes'] = dados['Mes'].map(meses_portugues)

def rotulo_de_dados(figura,dados,variavel):
    """Exibe o rotulo de dados na tela

    Args:
        figura (fig): grafico que sera colocado o rotulo
        dados (dataframe): dataframe de onde sera retirado a coluna da variavel
        variavel (column): coluna da variavel
    """
    figura.update_traces(
    mode='lines+markers+text',  # Modo para exibir linhas, marcadores e texto
    text=dados[variavel],  # Dados para exibir como texto
    textposition='top center',  # Posição do texto (acima do ponto de dados)
    textfont=dict(size=12, color='black')  # Configurações de fonte do texto
)







# Header
st.set_page_config(layout = 'wide')
st.markdown("<h1 style='text-align: center;'>DASHBOARD DE INTERRUPÇÕES NO NORDESTE 2023</h1>", unsafe_allow_html=True)


#importando o arquivo do dashboard
df = pd.read_parquet('dash.parquet',engine='pyarrow')
df = df.reset_index()
df['InicioInterrupcao'] = pd.to_datetime(df['InicioInterrupcao'], format='%Y-%m-%d %H:%M:%S')
df['FimInterrupcao'] = pd.to_datetime(df['FimInterrupcao'], format='%Y-%m-%d %H:%M:%S')
distribuidoras = df['Distribuidora'].unique().tolist()
distribuidoras.append('TODAS')
st.sidebar.title('Filtros')

distribuidora = st.sidebar.selectbox('Distribuidora',distribuidoras)

if distribuidora == 'TODAS':
    distribuidora = ''

# media de interrupções por mes
media_mes = df.shape[0] / 12
media_mes = int(media_mes)
# quantidade de unidades consumidoras
numero_consumidores = df.groupby('Conjunto')['NumConsumidoresConjunto'].mean().round(0).reset_index()
numero_consumidores = (numero_consumidores['NumConsumidoresConjunto'].sum()) / 1_000_000
numero_consumidores = numero_consumidores.round(1)



#tabelas 
# Tabela 1 com o número de interrupções 
numero_interrupcoes_mes = df.set_index('InicioInterrupcao').groupby(pd.Grouper(freq='M'))['index'].count().reset_index()
nome_mes(numero_interrupcoes_mes) # Substituir os nomes dos meses
limite_superior_y_numero_interrupcoes = numero_interrupcoes_mes['index'].max() * 1.3 # Calcular o limite superior do eixo y com 10% a mais que o maior valor

# Tabela 2 contagem por estação 
contagem_estacao = df['Estacao'].value_counts().reset_index()
limite_superior_y_contagem_estacao = contagem_estacao['count'].max() * 1.3 # Calcular o limite superior do eixo y com 10% a mais que o maior valor


# Tabela 3 contagem por Turno
contagem_turno = df['Turno'].value_counts().reset_index()
limite_superior_y_contagem_turno = contagem_turno['count'].max() * 1.3 # Calcular o limite superior do eixo y com 10% a mais que o maior valor


#Tabela 2 media de duração por
# criando o dataframe com as mediana das variaveis numericas 
mediana_das_variaveis = df.set_index('InicioInterrupcao').groupby(pd.Grouper(freq='M'))[['Duracao','ConsumidoresAtingidos','CHI']].median().round(2).reset_index()
nome_mes(mediana_das_variaveis)
limite_superior_y_mediana_duracao = mediana_das_variaveis['Duracao'].max() * 1.3
limite_superior_y_mediana_consu = mediana_das_variaveis['ConsumidoresAtingidos'].max() * 1.3
limite_superior_y_mediana_chi = mediana_das_variaveis['CHI'].max() * 1.3


#Tabela 3 media de duração por
# criando o dataframe com as media das variaveis numericas 
media_das_variaveis = df.set_index('InicioInterrupcao').groupby(pd.Grouper(freq='M'))[['Duracao','ConsumidoresAtingidos','CHI']].mean().round(2).reset_index()
nome_mes(media_das_variaveis)
limite_superior_y_media_duracao = media_das_variaveis['Duracao'].max() * 1.3
limite_superior_y_media_consu = media_das_variaveis['ConsumidoresAtingidos'].max() * 1.3
limite_superior_y_media_chi = media_das_variaveis['CHI'].max() * 1.3









# Gráficos

# grafico 1
fig_numero_interrupcoes_mes = px.line(numero_interrupcoes_mes,
                                    x = 'Mes',
                                    y = 'index',
                                    markers = True,
                                    color_discrete_sequence=['#155952'],
                                    title = 'Número de Interrupções por Mês')
fig_numero_interrupcoes_mes.update_yaxes(range=[0, limite_superior_y_numero_interrupcoes])
fig_numero_interrupcoes_mes.update_layout(yaxis_title = 'Interrupções')
rotulo_de_dados(fig_numero_interrupcoes_mes,numero_interrupcoes_mes,'index')


#grafico estacao
fig_contagem_estacao = px.bar(contagem_estacao,
                              x = 'Estacao',
                              y = 'count',
                              text= 'count',
                              #title = 'Número de Ocorrências por Estação',
                              color_discrete_sequence=['#155952'])
fig_contagem_estacao.update_layout(yaxis_title = 'Estação')
fig_contagem_estacao.update_yaxes(range=[0, limite_superior_y_contagem_estacao])
fig_contagem_estacao.update_traces(texttemplate='%{text:.2s}', textposition='inside')


#grafico turno
fig_contagem_turno = px.bar(contagem_turno,
                              x = 'Turno',
                              y = 'count',
                              text = 'count',
                              #title = 'Número de Ocorrências por Turno',
                              color_discrete_sequence=['#155952'])
fig_contagem_turno.update_layout(yaxis_title = 'Turno')
fig_contagem_turno.update_yaxes(range=[0, limite_superior_y_contagem_turno])
fig_contagem_turno.update_traces(texttemplate='%{text:.2s}', textposition='inside')

# Grafico 3 media da duração
fig_media_duracao = px.line(media_das_variaveis,
                                    x = 'Mes',
                                    y = 'Duracao',
                                    markers = True,
                                    color_discrete_sequence=['#010440'],
                                    title = 'Média da Duração em horas por Mês')
fig_media_duracao.update_yaxes(range=[0, limite_superior_y_media_duracao])
fig_media_duracao.update_layout(yaxis_title = 'Duração')
rotulo_de_dados(fig_media_duracao,media_das_variaveis,'Duracao')


# Grafico 4 media dos consumidores atingidos
fig_media_consu = px.line(media_das_variaveis,
                                    x = 'Mes',
                                    y = 'ConsumidoresAtingidos',
                                    markers = True,
                                    color_discrete_sequence=['#148C26'],
                                    title = 'Media da Consumidores Atingidos  por Mês')

fig_media_consu.update_yaxes(range=[0, limite_superior_y_media_consu])
fig_media_consu.update_layout(yaxis_title = 'Unidades Consumidoras Atingidas')
rotulo_de_dados(fig_media_consu,media_das_variaveis,'ConsumidoresAtingidos')


# Grafico 5 media dos CHI
fig_media_chi = px.line(media_das_variaveis,
                                    x = 'Mes',
                                    y = 'CHI',
                                    markers = True,
                                    color_discrete_sequence=['#8C0E03'],
                                    title = 'Média de CHI  por Mês')
fig_media_chi.update_yaxes(range=[0, limite_superior_y_media_chi])
fig_media_chi.update_layout(yaxis_title = 'CHI')
rotulo_de_dados(fig_media_chi,media_das_variaveis,'CHI')



# Grafico 6 mediana da duracao
fig_mediana_duracao = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'Duracao',
                                    markers = True,
                                    color_discrete_sequence=['#010440'],
                                    title = 'Mediana da Duração em horas por Mês')
fig_mediana_duracao.update_yaxes(range=[0, limite_superior_y_mediana_duracao])
fig_mediana_duracao.update_layout(yaxis_title = 'Duração')
rotulo_de_dados(fig_mediana_duracao,mediana_das_variaveis,'Duracao')


# Grafico 7 mediana dos consumidores atingidos
fig_mediana_consu = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'ConsumidoresAtingidos',
                                    markers = True,
                                    color_discrete_sequence=['#148C26'],
                                    title = 'Mediana da Consumidores Atingidos  por Mês')

fig_mediana_consu.update_yaxes(range=[0, limite_superior_y_mediana_consu])
fig_mediana_consu.update_layout(yaxis_title = 'Unidades Consumidoras Atingidas')
rotulo_de_dados(fig_mediana_consu,mediana_das_variaveis,'ConsumidoresAtingidos')


# Grafico 8 mediana dos CHI
fig_mediana_chi = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'CHI',
                                    markers = True,
                                    color_discrete_sequence=['#8C0E03'],
                                    title = 'Mediana da CHI  por Mês')
fig_mediana_chi.update_yaxes(range=[0, limite_superior_y_mediana_chi])
fig_mediana_chi.update_layout(yaxis_title = 'CHI')
rotulo_de_dados(fig_mediana_chi,mediana_das_variaveis,'CHI')





aba1, aba2 = st.tabs(['Período','Fator Gerador'])


with aba1:
# primeiro bloco do Dashboard
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Número Total de Interrupções em 2023',df.shape[0])
    with col2:
        st.metric('Mediana de Duração em horas',df['Duracao'].median().round(2))
    with col3:
        st.metric('Mediana de Consumidores Atingidos',df['ConsumidoresAtingidos'].median().round(2))
    with col4:
        st.metric('Mediana de CHI',df['CHI'].median().round(2))

    st.plotly_chart(fig_numero_interrupcoes_mes,use_container_width= True)

    # segundo bloco do Dashboard
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2 style='text-align: center;'>Quantidade de Interrupções por Estação</h2>", unsafe_allow_html=True)
        st.plotly_chart(fig_contagem_estacao,use_container_width= True)

    with col2:
        st.markdown("<h2 style='text-align: center;'>Quantidade de Interrupções por Turno</h2>", unsafe_allow_html=True)
        st.plotly_chart(fig_contagem_turno,use_container_width= True)


    # terceiro bloco do Dashboard
    st.markdown("<h2 style='text-align: center;'>Duração</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_media_duracao,use_container_width= True)
    with col2:
        st.plotly_chart(fig_mediana_duracao,use_container_width= True)
    
    # quarto bloco do Dashboard
    st.markdown("<h2 style='text-align: center;'>Consumidores Atingidos</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_media_consu,use_container_width= True)
    with col2:
        st.plotly_chart(fig_mediana_consu,use_container_width= True)

    # quinto bloco do Dashboard
    st.markdown("<h2 style='text-align: center;'>CHI</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_media_chi,use_container_width= True)
    with col2:
        st.plotly_chart(fig_mediana_chi,use_container_width= True)


with aba2:
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Número Total de Interrupções em 2023',df.shape[0])
    with col2:
        st.metric('Mediana de Duração em horas',df['Duracao'].median().round(2))
    with col3:
        st.metric('Mediana de Consumidores Atingidos',df['ConsumidoresAtingidos'].median().round(2))
    with col4:
        st.metric('Mediana de CHI',df['CHI'].median().round(2))