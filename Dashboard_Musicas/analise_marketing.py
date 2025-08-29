import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title('Análise de Marketing')

BASE_DIR = os.path.dirname(__file__)
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

orcamento_instagram = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_instagram.xlsx'))
orcamento_instagram['Ano'] = orcamento_instagram['Ano'].astype(int)

orcamento_facebook = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_facebook.xlsx'))
orcamento_facebook['Ano'] = orcamento_facebook['Ano'].astype(int)

orcamento_google_Ads = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_google_Ads.xlsx'))
orcamento_google_Ads['Ano'] = orcamento_google_Ads['Ano'].astype(int)

orcamento_tiktok = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_tiktok.xlsx'))
orcamento_tiktok['Ano'] = orcamento_tiktok['Ano'].astype(int)

orcamento_youtube = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_youtube.xlsx'))
orcamento_youtube['Ano'] = orcamento_youtube['Ano'].astype(int)

campanhas_por_canal = pd.read_excel(os.path.join(PLANILHAS_DIR, 'campanhas_por_canal.xlsx'))
campanhas_por_canal['Ano'] = campanhas_por_canal['Ano'].astype(int)

anos_analise_marketing = sorted(set(orcamento_instagram['Ano'].unique().tolist() +
                                    orcamento_facebook['Ano'].unique().tolist() +
                                    orcamento_google_Ads['Ano'].unique().tolist() +
                                    orcamento_tiktok['Ano'].unique().tolist() +
                                    orcamento_youtube['Ano'].unique().tolist() +
                                    campanhas_por_canal['Ano'].unique().tolist()))

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    filtro_anos_analise_marketing = st.selectbox('Anos', anos_analise_marketing)
    
a1, a2, a3, a4, a5 = st.columns(5)

orcamento_instagram_filtrado = orcamento_instagram[orcamento_instagram['Ano'] == filtro_anos_analise_marketing]
orcamento_facebook_filtrado = orcamento_facebook[orcamento_facebook['Ano'] == filtro_anos_analise_marketing]
orcamento_google_Ads_filtrado = orcamento_google_Ads[orcamento_google_Ads['Ano'] == filtro_anos_analise_marketing]
orcamento_tiktok_filtrado = orcamento_tiktok[orcamento_tiktok['Ano'] == filtro_anos_analise_marketing]
orcamento_youtube_filtrado = orcamento_youtube[orcamento_youtube['Ano'] == filtro_anos_analise_marketing]
campanhas_por_canal_filtrado = campanhas_por_canal[campanhas_por_canal['Ano'] == filtro_anos_analise_marketing]


valor_instagram = orcamento_instagram_filtrado['Orçamento'].iloc[0]
valor_instagram_formatado = f"R$ {valor_instagram:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

valor_facebook = orcamento_facebook_filtrado['Orçamento'].iloc[0]
valor_facebook_formatado = f"R$ {valor_facebook:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

valor_google_Ads = orcamento_google_Ads_filtrado['Orçamento'].iloc[0]
valor_google_Ads_formatado = f"R$ {valor_google_Ads:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

valor_tiktok = orcamento_tiktok_filtrado['Orçamento'].iloc[0]
valor_tiktok_formatado = f"R$ {valor_tiktok:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

valor_youtube = orcamento_youtube_filtrado['Orçamento'].iloc[0]
valor_youtube_formatado = f"R$ {valor_youtube:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
with a1:
    st.metric('Orçamento Instagram', valor_instagram_formatado, border=True)
with a2:
    st.metric('Orçamento Facebook', valor_facebook_formatado, border=True)
with a3:
    st.metric('Orçamento Google Ads', valor_google_Ads_formatado, border=True)
with a4:
    st.metric('Orçamento TikTok', valor_tiktok_formatado, border=True)
with a5:
    st.metric('Orçamento YouTube', valor_youtube_formatado, border=True)
    
grafico_campanhas_canal = px.bar(campanhas_por_canal_filtrado, x='Canal', y='Campanhas', title='Campanhas por Canal',
                                    color_discrete_sequence=["#7B44D3"], text='Campanhas')
grafico_campanhas_canal.update_layout(yaxis_showgrid=False, yaxis=dict(dtick=1))
grafico_campanhas_canal.update_traces(textposition='outside')
st.plotly_chart(grafico_campanhas_canal)
