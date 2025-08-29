import streamlit as st
import pandas as pd
import plotly.express as px
#
@st.cache_resource
def carregar_dados():
    df = pd.read_parquet('Covid/dados_covid19_agregado.parquet')
    return df

df = carregar_dados()

a1,a2,a3,a4,a5,a6,a7,a8 = st.columns(8)

with a1:
    anos = sorted(set(df['ano'].unique().tolist()))
    filtro_anos = st.selectbox('Anos', anos)

df_filtrado = df[df['ano'] == filtro_anos]

casos = df_filtrado['casosNovos'].sum()

obitos = df_filtrado['obitosNovos'].sum()

taxaMortalidade = obitos / casos * 100    


def formatar_pontos(num):
    return f"{num:,}".replace(",", ".")

col1, col2, col3= st.columns(3)

with col1:
    st.metric('Casos', value=formatar_pontos(casos), border=True)

with col2:
    st.metric('Óbitos', value=formatar_pontos(obitos), border=True)

with col3:
    st.metric('Taxa de mortalidade', value=f"{taxaMortalidade:.{1}f}%", border=True)
    
st.markdown('')

col4, col5 = st.columns(2)    

with col4:
    
    st.subheader('Casos')

    df_casos_mes = df_filtrado.groupby('ano_mes', as_index=False)['casosNovos'].sum()

    casos_mes = px.line(df_casos_mes, x='ano_mes', y='casosNovos', title='Evolução dos casos ao longo dos meses',
                        height=500, color_discrete_sequence=["#7B44D3"])
    casos_mes.update_layout(
                            xaxis_title='Mês', xaxis_title_font=dict(size=22, color="black"), xaxis_tickfont=dict(size=15, color='black'),
                            yaxis_title='Casos', yaxis_title_font=dict(size=22, color="black"), yaxis_tickfont=dict(size=15, color='black'))
    st.plotly_chart(casos_mes)
    
    st.divider()

    df_casos_estado = df_filtrado.groupby('estado', as_index=False)['casosNovos'].sum()
    casos_estado = px.bar(df_casos_estado, y='casosNovos', x='estado', title='Quantidade de casos por estado', height=500,
                          color_discrete_sequence=["#7B44D3"])
    casos_estado.update_layout(
                            xaxis_title='Estado', xaxis_title_font=dict(size=22, color='black'), xaxis_tickfont=dict(size=15, color="black"),
                            yaxis_title='Casos', yaxis_title_font=dict(size=22, color="black"), yaxis_tickfont=dict(size=15, color="black")
                               )
    st.plotly_chart(casos_estado)

    st.divider()

    casosTotal = df_filtrado['casosNovos'].sum()
    perc_casos_estado = df_filtrado.groupby(['ano','estado'], as_index=False)['casosNovos'].sum()
    perc_casos_estado['casosEstado'] = perc_casos_estado['casosNovos'] / casosTotal * 100

    fig1 = px.choropleth(
        perc_casos_estado,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="estado",
        featureidkey="properties.sigla",
        color="casosEstado",
        color_continuous_scale="Purples",
        title='Percentual de óbitos por estado',
        height=700
    )
    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_traces(
        hovertemplate="<b>%{location}</b><br>Percentual: %{z:.1f}%<extra></extra>",
        hoverlabel=dict(font_size=15))  

    fig1.update_layout(
        coloraxis_colorbar=dict(
            title="Percentual de casos"
        ))

    st.plotly_chart(fig1)
 #a
with col5:
    st.subheader('Óbitos')

    df_obitos_mes = df_filtrado.groupby('ano_mes', as_index=False)['obitosNovos'].sum()

    obitos_mes = px.line(df_obitos_mes, x='ano_mes', y='obitosNovos', title='Evolução dos óbitos ao longo dos meses',
                         height=500, color_discrete_sequence=["#7B44D3"])
    obitos_mes.update_layout(
                            xaxis_title='Mês', xaxis_title_font=dict(size=22, color='black'), xaxis_tickfont=dict(size=15, color="black"),
                            yaxis_title='Óbitos', yaxis_title_font=dict(size=22, color="black"), yaxis_tickfont=dict(size=15, color="black"))
    st.plotly_chart(obitos_mes)

    st.divider()
    
    df_obitos_estado = df_filtrado.groupby('estado', as_index=False)['obitosNovos'].sum()
    obitos_estado = px.bar(df_obitos_estado, y='obitosNovos', x='estado', title='Quantidade de óbitos por estado',
                           height=500, color_discrete_sequence=["#7B44D3"])
    obitos_estado.update_layout(
            xaxis_title='Estado', xaxis_title_font=dict(size=22, color="black"), xaxis_tickfont=dict(size=15, color="black"),
            yaxis_title='Óbitos', yaxis_title_font=dict(size=22, color="black"), yaxis_tickfont=dict(size=15, color="black"))
    st.plotly_chart(obitos_estado)

    st.divider()
    
    obitosTotal = df_filtrado['obitosNovos'].sum()
    perc_obitos_estado = df_filtrado.groupby(['ano', 'estado'], as_index=False)['obitosNovos'].sum()
    perc_obitos_estado['obitosEstado'] = perc_obitos_estado['obitosNovos'] / obitosTotal * 100

    fig2 = px.choropleth(
        perc_obitos_estado,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="estado",
        featureidkey="properties.sigla",
        color="obitosEstado",
        color_continuous_scale="Purples",
        title='Percentual de óbitos por estado',
        height=700

    )
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(
        coloraxis_colorbar=dict(
            title="Percentual de óbitos"
        ))
    fig2.update_traces(
    hovertemplate="<b>%{location}</b><br>Percentual: %{z:.1f}%<extra></extra>",
    hoverlabel=dict(font_size=15)
)

    st.plotly_chart(fig2)