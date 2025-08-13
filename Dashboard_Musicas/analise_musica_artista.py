import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title('Análise de Músicas/Artistas')

BASE_DIR = os.path.dirname(__file__)
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

numero_albuns = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_albuns.xlsx'))
numero_albuns['Ano'] = numero_albuns['Ano'].astype(int)

numero_musicas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_musicas.xlsx'))
numero_musicas['Ano'] = numero_musicas['Ano'].astype(int)

numero_generos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_generos.xlsx'))
numero_generos['Ano'] = numero_generos['Ano'].astype(int)

numero_musicas_skipadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_musicas_skipadas.xlsx'))
numero_musicas_skipadas['Ano'] = numero_musicas_skipadas['Ano'].astype(int)

musicas_mais_tocadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_mais_tocadas.xlsx'))
musicas_mais_tocadas['Ano'] = musicas_mais_tocadas['Ano'].astype(int)

musicas_por_genero = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_por_genero.xlsx'))
musicas_por_genero['Ano'] = musicas_por_genero['Ano'].astype(int)

artistas_mais_populares = pd.read_excel(os.path.join(PLANILHAS_DIR, 'artistas_mais_populares.xlsx')).head(10)

anos_Am = sorted(set(numero_albuns["Ano"].unique().tolist() + 
                        numero_generos["Ano"].unique().tolist() +
                        numero_musicas["Ano"].unique().tolist() +
                        numero_musicas_skipadas["Ano"].unique().tolist() + 
                        musicas_mais_tocadas["Ano"].unique().tolist() +
                        musicas_por_genero["Ano"].unique().tolist()))

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    filtro_anos_Am = st.selectbox('Anos', anos_Am)
    
numero_albuns_fitrado = numero_albuns[numero_albuns['Ano'] == filtro_anos_Am]
numero_generos_filtrado = numero_generos[numero_generos['Ano'] == filtro_anos_Am]
numero_musicas_filtrado = numero_musicas[numero_musicas['Ano'] == filtro_anos_Am]
numero_musicas_skipadas_filtrado = numero_musicas_skipadas[numero_musicas_skipadas['Ano'] == filtro_anos_Am]
musicas_mais_tocadas_filtrado = musicas_mais_tocadas[musicas_mais_tocadas['Ano'] == filtro_anos_Am].head(10)
musicas_por_genero_filtrado = musicas_por_genero[musicas_por_genero['Ano'] == filtro_anos_Am]
        
am1, am2, am3, am4 = st.columns(4)

with am1:
    st.metric('Número de álbuns', numero_albuns_fitrado["Número de Álbuns"].iloc[0], border=True)
with am2:
    st.metric('Número de músicas', numero_musicas_filtrado["Número de músicas"].iloc[0], border=True)
with am3:
    st.metric('Número de gêneros', numero_generos_filtrado["Gêneros"].iloc[0], border=True)
with am4:
    st.metric('Número de músicas skipadas', numero_musicas_skipadas_filtrado["Músicas skipadas"].iloc[0], border=True)

ama1, ama2 = st.columns(2)

with ama1:
    grafico_musica_mais_tocadas = px.bar(musicas_mais_tocadas_filtrado, x='Quantidade', y='Música',
                                            title='Top 10 músicas mais tocadas', color_discrete_sequence=["#7B44D3"])
    grafico_musica_mais_tocadas.update_layout(yaxis_title=None, yaxis=dict(autorange='reversed'),
                                                xaxis_title='Quantidade de vezes tocada')
    st.plotly_chart(grafico_musica_mais_tocadas)
with ama2:
    grafico_artistas_mais_populares = px.bar(artistas_mais_populares, x='Seguidores', y='Artista',
                                                color_discrete_sequence=["#7B44D3"], title='Top 10 artistas mais populares')
    grafico_artistas_mais_populares.update_layout(yaxis_title=None, yaxis=dict(autorange='reversed'))
    st.plotly_chart(grafico_artistas_mais_populares)
    
grafico_musicas_por_genero = px.bar(musicas_por_genero_filtrado, x='Gênero', y='Músicas',
                                    color_discrete_sequence=["#7B44D3"], title='Quantidade de músicas por gênero',
                                    text='Músicas')
grafico_musicas_por_genero.update_traces(textposition='outside')
grafico_musicas_por_genero.update_layout(yaxis_showgrid=False)
st.plotly_chart(grafico_musicas_por_genero)
