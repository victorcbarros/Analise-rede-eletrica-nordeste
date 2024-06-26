# importando as bibliotecas 
import pandas as pd
import streamlit as st
import plotly.express as px



# Funções *****************************************************************************
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


# Configurações *****************************************************************************************************
st.set_page_config(layout = 'wide')
st.markdown("<h3 style='text-align: center;'>INTERRUPÇÕES DE ENERGIA ELÉTRICA NA REDE DE DISTRIBUIÇÃO DO NORDESTE EM 2023 💡</h3>", unsafe_allow_html=True)


#importando o arquivo do dashboard
df = pd.read_parquet('app/dash.parquet',engine='pyarrow')
df = df.reset_index()
df['InicioInterrupcao'] = pd.to_datetime(df['InicioInterrupcao'], format='%Y-%m-%d %H:%M:%S')
df['FimInterrupcao'] = pd.to_datetime(df['FimInterrupcao'], format='%Y-%m-%d %H:%M:%S')
nome_mes(df)
df['Mes_num'] = df['InicioInterrupcao'].dt.month
meses = df['Mes'].unique().tolist()
distribuidoras = df['Distribuidora'].unique().tolist()
distribuidoras.sort()

st.sidebar.title('Filtros')

#filtro mes
mes_inicial, mes_final = st.sidebar.select_slider('Meses:',options=meses,value=(meses[0],meses[-1]))
mes_num_map = {month: i for i, month in enumerate(meses, 1)} # Mapeamento dos nomes dos meses para números
mes_inicial_num = mes_num_map[mes_inicial] # Filtrar os dados com base no intervalo selecionado
mes_final_num = mes_num_map[mes_final]
df_filtrado = df[
    (df['Mes_num'] >= mes_inicial_num) & 
    (df['Mes_num'] <= mes_final_num) # Filtrando o DataFrame
]
#filtro distribuidora
filtro_distribuidora = st.sidebar.multiselect('Distribuidoras:',distribuidoras)
if filtro_distribuidora:
    df_filtrado = df_filtrado[df_filtrado['Distribuidora'].isin(filtro_distribuidora)]
#filtro expurgo
expurgos = df_filtrado['MotivoExpurgo'].unique().tolist()
expurgos.sort()
expurgos.insert(0,'TODOS')
filtro_expurgo = st.sidebar.selectbox('Motivo do Expurgo:',expurgos)
if filtro_expurgo == 'TODOS':
    df_filtrado2 = df_filtrado
else:
    df_filtrado2 = df_filtrado[df_filtrado['MotivoExpurgo'] == filtro_expurgo]
#filtro responsabilidade
responsabilidades = df_filtrado['Responsabilidade'].unique().tolist()
responsabilidades.sort()
responsabilidades.insert(0,'TODAS')
filtro_responsabilidade = st.sidebar.selectbox('Responsabilidade:',responsabilidades)
if filtro_responsabilidade == 'TODAS':
    df_filtrado3 = df_filtrado2
else:
    df_filtrado3 = df_filtrado2[df_filtrado2['Responsabilidade'] == filtro_responsabilidade]
#filtro Causa
causas = df_filtrado['Causa'].unique().tolist()
causas.sort()
filtro_causa = st.sidebar.multiselect('Causa:',causas)
if filtro_causa:
    df_filtrado = df_filtrado[df_filtrado['Causa'].isin(filtro_causa)]


# Tabelas **************************************************************************

# Tabela 1 com o número de interrupções 
numero_interrupcoes_mes = df_filtrado.set_index('InicioInterrupcao').groupby(pd.Grouper(freq='M'))['index'].count().reset_index()
numero_interrupcoes_mes.columns = ['InicioInterrupcao', 'Quantidade']
nome_mes(numero_interrupcoes_mes) 
limite_superior_y_numero_interrupcoes = numero_interrupcoes_mes['Quantidade'].max() * 1.3

# Tabela 2 contagem por estação 
contagem_estacao = df_filtrado['Estacao'].value_counts().reset_index()
contagem_estacao.columns = ['Estacao', 'Quantidade']
limite_superior_y_contagem_estacao = contagem_estacao['Quantidade'].max() * 1.3 

#Tabela 3 mediana de duração por
mediana_das_variaveis = df_filtrado.set_index('InicioInterrupcao').groupby(pd.Grouper(freq='M'))[['Duracao','ConsumidoresAtingidos','CHI']].median().round(2).reset_index()
nome_mes(mediana_das_variaveis)
limite_superior_y_mediana_duracao = mediana_das_variaveis['Duracao'].max() * 1.3
limite_superior_y_mediana_consu = mediana_das_variaveis['ConsumidoresAtingidos'].max() * 1.3
limite_superior_y_mediana_chi = mediana_das_variaveis['CHI'].max() * 1.3

# Tabela 4 contagem por responsabilidade
contagem_resp = df_filtrado['Responsabilidade'].value_counts().sort_values(ascending=True).reset_index()
contagem_resp.columns = ['Responsabilidade', 'Quantidade']
limite_superior_y_contagem_resp = contagem_resp['Quantidade'].max() * 1.3 

# Tabela 5 contagem por causa
contagem_causa = df_filtrado['Causa'].value_counts().sort_values(ascending=True).reset_index()
contagem_causa.columns = ['Causa', 'Quantidade']
limite_superior_y_contagem_causa = contagem_causa['Quantidade'].max() * 1.3 

# Tabela 6 Medianas Responsabilidades 
mediana_resp = df_filtrado.groupby('Responsabilidade')[['Duracao','ConsumidoresAtingidos','CHI']].median().reset_index()
limite_superior_y_mediana_resp_duracao = mediana_resp['Duracao'].max() * 1.3
limite_superior_y_mediana_resp_consu = mediana_resp['ConsumidoresAtingidos'].max() * 1.3
limite_superior_y_mediana_resp_chi = mediana_resp['CHI'].max() * 1.3

# Tabela 7 Medianas Causa 
mediana_causa = df_filtrado.groupby('Causa')[['Duracao','ConsumidoresAtingidos','CHI']].median().reset_index()
# Ordenando mediana_resp pelo valor da mediana da 'Duracao'
mediana_causa_duracao = mediana_causa.sort_values(by='Duracao', ascending=False).head(5)
# Ordenando mediana_resp pelo valor da mediana da 'ConsumidoresAtingidos'
mediana_causa_cons = mediana_causa.sort_values(by='ConsumidoresAtingidos', ascending=False).head(5)
# Ordenando mediana_resp pelo valor da mediana da 'CHI'
mediana_causa_chi = mediana_causa.sort_values(by='CHI', ascending=False).head(5)
limite_superior_y_mediana_causa_duracao = mediana_causa['Duracao'].max() * 1.3
limite_superior_y_mediana_causa_consu = mediana_causa['ConsumidoresAtingidos'].max() * 1.3
limite_superior_y_mediana_causa_chi = mediana_causa['CHI'].max() * 1.3

# Gráficos *************************************************************************************************

# grafico 1 numero de interrupções por mes 
fig_numero_interrupcoes_mes = px.line(numero_interrupcoes_mes,
                                    x = 'Mes',
                                    y = 'Quantidade',
                                    markers = True,
                                    color_discrete_sequence=['#1300A7'],
                                    title = 'Número de Interrupções por Mês')
fig_numero_interrupcoes_mes.update_yaxes(range=[0, limite_superior_y_numero_interrupcoes])
fig_numero_interrupcoes_mes.update_layout(yaxis_title = 'Interrupções')
rotulo_de_dados(fig_numero_interrupcoes_mes,numero_interrupcoes_mes,'Quantidade')

#grafico 2 estacao
fig_contagem_estacao = px.bar(contagem_estacao,
                              x = 'Estacao',
                              y = 'Quantidade',
                              text= 'Quantidade',
                              title = 'Número de Ocorrências por Estação',
                              color_discrete_sequence=['#1300A7'])
fig_contagem_estacao.update_layout(yaxis_title = 'Quantidade')
fig_contagem_estacao.update_yaxes(range=[0, limite_superior_y_contagem_estacao])
fig_contagem_estacao.update_traces(texttemplate='%{text:.2s}', textposition='inside')

# Grafico 3 mediana da duracao
fig_mediana_duracao = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'Duracao',
                                    markers = True,
                                    color_discrete_sequence=['#00BFF3'],
                                    title = 'Mediana da Duração em horas por Mês')
fig_mediana_duracao.update_yaxes(range=[0, limite_superior_y_mediana_duracao])
fig_mediana_duracao.update_layout(yaxis_title = 'Duração')
rotulo_de_dados(fig_mediana_duracao,mediana_das_variaveis,'Duracao')

# Grafico 4 mediana dos consumidores atingidos
fig_mediana_consu = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'ConsumidoresAtingidos',
                                    markers = True,
                                    color_discrete_sequence=['#156082'],
                                    title = 'Mediana de Consumidores Atingidos por Mês')
fig_mediana_consu.update_yaxes(range=[0, limite_superior_y_mediana_consu])
fig_mediana_consu.update_layout(yaxis_title = 'Unidades Consumidoras Atingidas')
rotulo_de_dados(fig_mediana_consu,mediana_das_variaveis,'ConsumidoresAtingidos')

# Grafico 5 mediana dos CHI
fig_mediana_chi = px.line(mediana_das_variaveis,
                                    x = 'Mes',
                                    y = 'CHI',
                                    markers = True,
                                    color_discrete_sequence=['#08003B'],
                                    title = 'Mediana do CHI  por Mês')
fig_mediana_chi.update_yaxes(range=[0, limite_superior_y_mediana_chi])
fig_mediana_chi.update_layout(yaxis_title = 'CHI')
rotulo_de_dados(fig_mediana_chi,mediana_das_variaveis,'CHI')

# Grafico 6 Contagem por Resposanbilidade
fig_contagem_resp = px.bar(contagem_resp,
                              x = 'Quantidade',
                              y = 'Responsabilidade',
                              text= 'Quantidade',
                              title = 'Ocorrências por Responsabilidade',
                              color_discrete_sequence=['#1300A7'])
fig_contagem_resp.update_layout(yaxis_title = 'Responsabilidade')
fig_contagem_resp.update_xaxes(range=[0, limite_superior_y_contagem_resp])
fig_contagem_resp.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 7 Contagem por Causa
fig_contagem_causa = px.bar(contagem_causa.tail(10),
                              x = 'Quantidade',
                              y = 'Causa',
                              text= 'Quantidade',
                              title = 'Ocorrências por Causa',
                              color_discrete_sequence=['#1300A7'])
fig_contagem_causa.update_layout(yaxis_title = 'Causa')
fig_contagem_causa.update_xaxes(range=[0, limite_superior_y_contagem_causa])
fig_contagem_causa.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 8 Mediana Duração Responsabilidade 
# Ordenando mediana_resp pelo valor da mediana da 'Duracao'
mediana_resp = mediana_resp.sort_values(by='Duracao', ascending=False)
fig_mediana_duracao_resp = px.bar(mediana_resp,
                              x = 'Responsabilidade',
                              y = 'Duracao',
                              text= 'Duracao',
                              title = 'Mediana Duração(h) - Responsabilidade',
                              color_discrete_sequence=['#00BFF3'])
fig_mediana_duracao_resp.update_layout(yaxis_title = 'Duração')
fig_mediana_duracao_resp.update_yaxes(range=[0, limite_superior_y_mediana_resp_duracao])
fig_mediana_duracao_resp.update_xaxes(tickangle=-45)
fig_mediana_duracao_resp.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 9 Mediana Consumidores Atingidos Responsabilidade 
# Ordenando mediana_resp pelo valor da mediana da consumidores atingidos
mediana_resp = mediana_resp.sort_values(by='ConsumidoresAtingidos', ascending=False)
fig_mediana_consu_resp = px.bar(mediana_resp,
                              x = 'Responsabilidade',
                              y = 'ConsumidoresAtingidos',
                              text= 'ConsumidoresAtingidos',
                              title = 'Mediana Consumidores - Responsabilidade',
                              color_discrete_sequence=['#156082'])
fig_mediana_consu_resp.update_layout(yaxis_title = 'Consumidores Atingidos')
fig_mediana_consu_resp.update_yaxes(range=[0, limite_superior_y_mediana_resp_consu])
fig_mediana_consu_resp.update_xaxes(tickangle=-45)
fig_mediana_consu_resp.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 10 Mediana CHI Responsabilidade 
# Ordenando mediana_resp pelo valor da mediana da CHI
mediana_resp = mediana_resp.sort_values(by='CHI', ascending=False)
fig_mediana_chi_resp = px.bar(mediana_resp,
                              x = 'Responsabilidade',
                              y = 'CHI',
                              text= 'CHI',
                              title = 'Mediana CHI - Responsabilidade',
                              color_discrete_sequence=['#08003B'])
fig_mediana_chi_resp.update_layout(yaxis_title = 'CHI')
fig_mediana_chi_resp.update_yaxes(range=[0, limite_superior_y_mediana_resp_chi])
fig_mediana_chi_resp.update_xaxes(tickangle=-45)
fig_mediana_chi_resp.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 11 Mediana Duração Causa
fig_mediana_duracao_causa = px.bar(mediana_causa_duracao,
                              x = 'Causa',
                              y = 'Duracao',
                              text= 'Duracao',
                              title = 'Mediana Duração(h) - Causa',
                              color_discrete_sequence=['#00BFF3'])
fig_mediana_duracao_causa.update_layout(yaxis_title = 'Duração')
fig_mediana_duracao_causa.update_yaxes(range=[0, limite_superior_y_mediana_causa_duracao])
fig_mediana_duracao_causa.update_xaxes(tickangle=-90)
fig_mediana_duracao_causa.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 12 Mediana Consumidores Atingidos Responsabilidade 
fig_mediana_consu_causa = px.bar(mediana_causa_cons,
                              x = 'Causa',
                              y = 'ConsumidoresAtingidos',
                              text= 'ConsumidoresAtingidos',
                              title = 'Mediana Consudimidores - Causa',
                              color_discrete_sequence=['#156082'])
fig_mediana_consu_causa.update_layout(yaxis_title = 'Consudimidores Atingidos')
fig_mediana_consu_causa.update_yaxes(range=[0, limite_superior_y_mediana_causa_consu])
fig_mediana_consu_causa.update_xaxes(tickangle=-90)
fig_mediana_consu_causa.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')

# Grafico 13 Mediana CHI Causa
fig_mediana_chi_causa = px.bar(mediana_causa_chi,
                              x = 'Causa',
                              y = 'CHI',
                              text= 'CHI',
                              title = 'Mediana de CHI - Causa',
                              color_discrete_sequence=['#08003B'])
fig_mediana_chi_causa.update_layout(yaxis_title = 'CHI')
fig_mediana_chi_causa.update_yaxes(range=[0, limite_superior_y_mediana_causa_chi])
fig_mediana_chi_causa.update_xaxes(tickangle=-90)
fig_mediana_chi_causa.update_traces(texttemplate='%{text:.2s}', textposition='outside',textfont_color='black')


aba1, aba2 = st.tabs(['Período','Fator Gerador'])


with aba1:
# primeiro bloco do Dashboard
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Número Total de Interrupções em 2023',df_filtrado.shape[0])
    with col2:
        st.metric('Mediana de Duração em horas',round(df_filtrado['Duracao'].median(),2))
    with col3:
        st.metric('Mediana de Consumidores Atingidos',int(df_filtrado['ConsumidoresAtingidos'].median()))
    with col4:
        st.metric('Mediana de CHI',round(df_filtrado['CHI'].median(),2))

    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_numero_interrupcoes_mes,use_container_width= True)
    with col2:
        st.plotly_chart(fig_contagem_estacao,use_container_width= True)

    col3, col4,col5 = st.columns(3)
    with col3:
        st.plotly_chart(fig_mediana_duracao,use_container_width= True)
    with col4:
        st.plotly_chart(fig_mediana_consu,use_container_width= True)
    with col5:
        st.plotly_chart(fig_mediana_chi,use_container_width= True)


with aba2:
# primeiro bloco do Dashboard
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Número Total de Interrupções em 2023',df_filtrado.shape[0])
    with col2:
        st.metric('Mediana de Duração em horas',round(df_filtrado['Duracao'].median(),2))
    with col3:
        st.metric('Mediana de Consumidores Atingidos',int(df_filtrado['ConsumidoresAtingidos'].median()))
    with col4:
        st.metric('Mediana de CHI',round(df_filtrado['CHI'].median(),2))

    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.plotly_chart(fig_contagem_resp,use_container_width= True)
    with col2:
        st.plotly_chart(fig_mediana_duracao_resp,use_container_width= True)
    with col3:
        st.plotly_chart(fig_mediana_consu_resp,use_container_width= True)
    with col4:
        st.plotly_chart(fig_mediana_chi_resp,use_container_width= True)
    
    col5, col6,col7,col8 = st.columns(4)
    with col5:
        st.plotly_chart(fig_contagem_causa,use_container_width= True)
    with col6:
        st.plotly_chart(fig_mediana_duracao_causa,use_container_width= True)
    with col7:
        st.plotly_chart(fig_mediana_consu_causa,use_container_width= True)
    with col8:
        st.plotly_chart(fig_mediana_chi_causa,use_container_width= True)



