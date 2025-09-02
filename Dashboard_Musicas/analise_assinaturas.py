import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title('Análise de Assinaturas')

BASE_DIR = os.path.dirname(__file__)
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

assinaturas_pagas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_pagas.xlsx'))
assinaturas_falhas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_falhas.xlsx'))
assinaturas_reembolsadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_reembolsadas.xlsx'))
valor_total_assinaturas_pagas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'valor_total_assinaturas_pagas.xlsx'))
assinaturas_por_tipo_status = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_por_tipo_status.xlsx'))

col_index = valor_total_assinaturas_pagas.columns.get_loc("sum")
total_assinaturas_pagas = int(valor_total_assinaturas_pagas.iloc[0, col_index])
valor_total_assinaturas_pagas_formatado = f"R$ {total_assinaturas_pagas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

aa1, aa2, aa3, aa4 = st.columns(4)

with aa1:
    st.metric('Número de assinaturas pagas', int(assinaturas_pagas.loc[0, 'count']), border=True)
with aa2:
    st.metric('Número de assinaturas falhas', int(assinaturas_falhas.loc[0, 'count']), border=True)
with aa3:
    st.metric('Número de assinaturas reembolsadas', int(assinaturas_reembolsadas.loc[0, 'count']), border=True)
with aa4:
    st.metric('Valor total de assinaturas pagas', valor_total_assinaturas_pagas_formatado, border=True)
    
grafico_assinaturas_ts = px.bar(assinaturas_por_tipo_status, x='Tipo', y='Quantidade',
                                title='Assinaturas por tipo e status', color='Status',
                                barmode='group', color_discrete_sequence=["#751B99", '#7B44D3'],
                                text='Quantidade')
grafico_assinaturas_ts.update_layout(yaxis_showgrid=False)
grafico_assinaturas_ts.update_traces(textposition='outside')
st.plotly_chart(grafico_assinaturas_ts)
