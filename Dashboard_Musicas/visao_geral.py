import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title('Visão Geral')

        
BASE_DIR = os.path.dirname(__file__)
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

# Carregando planilhas com conversão da coluna 'Ano'
total_usuarios = pd.read_excel(os.path.join(PLANILHAS_DIR, 'total_usuarios.xlsx'))
total_usuarios['Ano'] = total_usuarios['Ano'].astype(int)

receita_total = pd.read_excel(os.path.join(PLANILHAS_DIR, 'receita_total.xlsx'))
receita_total['Ano'] = receita_total['Ano'].astype(int)

musicas_ultimo_mes = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_ultimo_mes.xlsx'))
musicas_ultimo_mes['Ano'] = musicas_ultimo_mes['Ano'].astype(int)

taxa_cancelamento = pd.read_excel(os.path.join(PLANILHAS_DIR, 'taxa_cancelamento.xlsx'))
taxa_cancelamento['Ano'] = taxa_cancelamento['Ano'].astype(int)

total_usuarios_ativos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'total_usuarios_ativos.xlsx'))
total_usuarios_ativos['Ano'] = total_usuarios_ativos['Ano'].astype(int)

anos_vg = sorted(set(total_usuarios["Ano"].unique().tolist() + 
                receita_total["Ano"].unique().tolist() +
                musicas_ultimo_mes["Ano"].unique().tolist() +
                taxa_cancelamento["Ano"].unique().tolist() +
                total_usuarios_ativos["Ano"].unique().tolist()))

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    filtro_anos_Vg = st.selectbox("Anos", anos_vg)

total_usuarios_filtrado = total_usuarios[total_usuarios["Ano"] == filtro_anos_Vg]

musicas_ultimo_mes_filtrado = musicas_ultimo_mes[musicas_ultimo_mes["Ano"] == filtro_anos_Vg].sort_values(by='Mês', ascending=False).head(1)
print(musicas_ultimo_mes_filtrado)
taxa_cancelamento_filtrado = taxa_cancelamento[taxa_cancelamento["Ano"] == filtro_anos_Vg]

total_usuarios_ativos_filtrado = total_usuarios_ativos[total_usuarios_ativos["Ano"] == filtro_anos_Vg]


valor_receita_total = receita_total['Receita Total'].iloc[0]
valor_receita_total_formatado = f"R$ {valor_receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

valor_taxa_cancelamento = taxa_cancelamento['Taxa de cancelamento'].iloc[0]
valor_taxa_cancelamento_formatado = f"{valor_taxa_cancelamento}%"

vg1, vg2, vg3, vg4 = st.columns(4)

with vg1:
    st.metric('Total de Usuários', total_usuarios_filtrado['Total de Usuários'].iloc[0], border=True)
with vg2:
    st.metric('Receita Total', valor_receita_total_formatado, border=True)
with vg3:
    st.metric('Número de músicas tocadas no último mês', musicas_ultimo_mes_filtrado["Total de Músicas"].iloc[0], border=True)
with vg4:
    st.metric('Taxa de Cancelamento', valor_taxa_cancelamento_formatado, border=True)    

st.markdown('Obs: O filtro de Ano não se aplica à Taxa de Cancelamento. A Receita total está sendo contabilizada apenas no ano de 2025.')

grafico_vg = px.bar(total_usuarios_ativos_filtrado, x='Mês', y='Quantidade',
                    color_discrete_sequence=["#7B44D3"], text='Quantidade', title='Total de usuários ativos/mês')
grafico_vg.update_layout(yaxis_showgrid=False)
grafico_vg.update_traces(textposition='outside')

st.plotly_chart(grafico_vg)
