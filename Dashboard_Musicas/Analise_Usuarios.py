import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title('Análise de Usuários')

BASE_DIR = os.path.dirname(__file__)
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

crescimento_usuarios = pd.read_excel(os.path.join(PLANILHAS_DIR, 'crescimento_usuarios.xlsx'))
crescimento_usuarios['Ano'] = crescimento_usuarios['Ano'].astype(int)

ordem_mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
             'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
crescimento_usuarios['Mês'] = pd.Categorical(
    crescimento_usuarios['Mês'],
    categories=ordem_mes,
    ordered=True
)

usuarios_por_genero = pd.read_excel(os.path.join(PLANILHAS_DIR, 'usuarios_por_genero.xlsx'))
usuarios_por_genero['Ano'] = usuarios_por_genero['Ano'].astype(int)

usuarios_mais_ativos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'usuarios_mais_ativos.xlsx'))
usuarios_mais_ativos['Ano'] = usuarios_mais_ativos['Ano'].astype(int)

distribuicao_por_pais = pd.read_excel(os.path.join(PLANILHAS_DIR, 'distribuicao_por_pais.xlsx'))
distribuicao_por_pais['Ano'] = distribuicao_por_pais['Ano'].astype(int)

anos_Au = sorted(set(crescimento_usuarios["Ano"].unique().tolist() + 
                        usuarios_por_genero["Ano"].unique().tolist() +
                        usuarios_mais_ativos["Ano"].unique().tolist() +
                        distribuicao_por_pais["Ano"].unique().tolist()))

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    filtro_anos_Au = st.selectbox('Anos', anos_Au)

crescimento_usuarios_filtrado = crescimento_usuarios[crescimento_usuarios["Ano"] == filtro_anos_Au]
crescimento_usuarios_filtrado = crescimento_usuarios_filtrado.sort_values(by='Mês')

usuarios_por_genero_filtrado = usuarios_por_genero[usuarios_por_genero["Ano"] == filtro_anos_Au]
usuarios_mais_ativos_filtrado = usuarios_mais_ativos[usuarios_mais_ativos["Ano"] == filtro_anos_Au]
distribuicao_por_pais_filtrado = distribuicao_por_pais[distribuicao_por_pais["Ano"] == filtro_anos_Au] 

grafico_crescimento = px.line(crescimento_usuarios_filtrado, x='Mês' , y='Usuários', category_orders={'Mês' : ordem_mes},
                        markers=True, text='Usuários', color_discrete_sequence=["#7B44D3"], title='Crescimento de usuários ao longo do tempo')
grafico_crescimento.update_layout(yaxis_showgrid=False)
grafico_crescimento.update_traces(textposition='top center')
st.plotly_chart(grafico_crescimento)

au1, au2 = st.columns(2)

with au1:
    grafico_usuarios_genero = px.bar(usuarios_por_genero_filtrado, x='Gênero', y='Quantidade',
                                        color_discrete_sequence=["#7B44D3"], text='Quantidade', title='Número de usuários por gênero')
    grafico_usuarios_genero.update_layout(yaxis_showgrid=False)
    grafico_usuarios_genero.update_traces(textposition='outside')
    st.plotly_chart(grafico_usuarios_genero)
with au2:
    usuarios_mais_ativos_filtrado = usuarios_mais_ativos_filtrado.sort_values(by='Atividade', ascending=False).head(10)
    grafico_usuarios_mais_ativos = px.bar(usuarios_mais_ativos_filtrado, x='Atividade', y='Usuários',
                                                title='Top 10 usuários mais ativos', color_discrete_sequence=["#7B44D3"])
    grafico_usuarios_mais_ativos.update_layout(xaxis_title='Atividade em segundos', yaxis_title='',
                                                yaxis=dict(autorange='reversed'))
    st.plotly_chart(grafico_usuarios_mais_ativos)


grafico_distribuicao_por_pais = px.bar(distribuicao_por_pais_filtrado, x='País', y='Quantidade',
                                        title='Distribuição de usuários por país', text='Quantidade',
                                        color_discrete_sequence=["#7B44D3"])
grafico_distribuicao_por_pais.update_layout(yaxis_showgrid=False)
grafico_distribuicao_por_pais.update_traces(textposition='outside')
st.plotly_chart(grafico_distribuicao_por_pais)