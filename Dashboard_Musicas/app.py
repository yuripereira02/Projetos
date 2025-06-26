import streamlit as st
import pandas as pd
from consultas import *
import plotly.express as px
from streamlit_option_menu import option_menu


st.set_page_config(page_title='Dashboard Musicas', layout='wide')


with st.sidebar:
    st.title('**Geral App**')
    
    selected = option_menu(
        menu_title="Menu",
        options=["Visão Geral", "Análise de Usuários", "Análise de Músicas/Artistas",
                 "Análise de Assinaturas", "Análise de Marketing"],
        default_index=0,
    )

if selected == "Visão Geral":
    
    st.title('Visão Geral')

        
    total_usuarios = pd.read_sql_query(total_usuarios, con=engine)
    total_usuarios['Ano'] = total_usuarios['Ano'].astype(int)

    receita_total = pd.read_sql_query(receita_total, con=engine)
    receita_total['Ano'] = receita_total['Ano'].astype(int)

    musicas_ultimo_mes = pd.read_sql_query(musicas_ultimo_mes, con=engine)
    musicas_ultimo_mes['Ano'] = musicas_ultimo_mes['Ano'].astype(int)

    taxa_cancelamento = pd.read_sql_query(taxa_cancelamento, con=engine)
    taxa_cancelamento['Ano'] = taxa_cancelamento['Ano'].astype(int)

    total_usuarios_ativos = pd.read_sql_query(total_usuarios_ativos, con=engine)
    total_usuarios['Ano'] = total_usuarios['Ano'].astype(int)

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
    taxa_cancelamento_filtrado = taxa_cancelamento[taxa_cancelamento["Ano"] == filtro_anos_Vg]
    total_usuarios_ativos_filtrado = total_usuarios_ativos[total_usuarios_ativos["Ano"] == filtro_anos_Vg]

    valor_receita_total = receita_total.iloc[0]
    valor_receita_total_formatado = f"R$ {valor_receita_total.iloc[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    valor_taxa_cancelamento = taxa_cancelamento.iloc[0,0]
    valor_taxa_cancelamento_formatado = f"{valor_taxa_cancelamento}%"

    vg1, vg2, vg3, vg4 = st.columns(4)

    with vg1:
        st.metric('Total de Usuários', total_usuarios_filtrado.iloc[0,0], border=True)
    with vg2:
        st.metric('Receita Total', valor_receita_total_formatado, border=True)
    with vg3:
        st.metric('Número de músicas tocadas no último mês', musicas_ultimo_mes_filtrado.iloc[0,0], border=True)
    with vg4:
        st.metric('Taxa de Cancelamento', valor_taxa_cancelamento_formatado, border=True)    

    st.markdown('Obs: O filtro de Ano não se aplica à Taxa de Cancelamento. A Receita total está sendo contabilizada apenas no ano de 2025.')

    grafico_vg = px.bar(total_usuarios_ativos_filtrado, x='Mês', y='Quantidade',
                        color_discrete_sequence=['#00BFFF'], text='Quantidade', title='Total de usuários ativos/mês')
    grafico_vg.update_layout(yaxis_showgrid=False)
    grafico_vg.update_traces(textposition='outside')

    st.plotly_chart(grafico_vg)
    
elif selected == 'Análise de Usuários':
    
    st.title('Análise de Usuários')
    
    crescimento_usuarios = pd.read_sql_query(crescimento_usuarios, con=engine)
    
    crescimento_usuarios['Ano'] = crescimento_usuarios['Ano'].astype(int)
    ordem_mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    crescimento_usuarios['Mês'] = pd.Categorical(
        crescimento_usuarios['Mês'],
        categories=ordem_mes,
        ordered=True
    )
   
    print(crescimento_usuarios)
    usuarios_por_genero = pd.read_sql_query(usuarios_por_genero, con=engine)
    usuarios_por_genero['Ano'] = usuarios_por_genero['Ano'].astype(int)
    
    usuarios_mais_ativos = pd.read_sql_query(usuarios_mais_ativos, con=engine)
    usuarios_mais_ativos['Ano'] = usuarios_mais_ativos['Ano'].astype(int)
    
    distribuicao_por_pais = pd.read_sql_query(distribuicao_por_pais, con=engine)
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
                         markers=True, text='Usuários', color_discrete_sequence=['#00BFFF'], title='Crescimento de usuários ao longo do tempo')
    grafico_crescimento.update_layout(yaxis_showgrid=False)
    grafico_crescimento.update_traces(textposition='top center')
    st.plotly_chart(grafico_crescimento)
    
    au1, au2 = st.columns(2)
    
    with au1:
        grafico_usuarios_genero = px.bar(usuarios_por_genero_filtrado, x='Gênero', y='Quantidade',
                                         color_discrete_sequence=['#00BFFF'], text='Quantidade', title='Número de usuários por gênero')
        grafico_usuarios_genero.update_layout(yaxis_showgrid=False)
        grafico_usuarios_genero.update_traces(textposition='outside')
        st.plotly_chart(grafico_usuarios_genero)
    with au2:
        usuarios_mais_ativos_filtrado = usuarios_mais_ativos_filtrado.sort_values(by='Atividade', ascending=False).head(10)
        grafico_usuarios_mais_ativos = px.bar(usuarios_mais_ativos_filtrado, x='Atividade', y='Usuários',
                                                    title='Top 10 usuários mais ativos', color_discrete_sequence=['#00BFFF'])
        grafico_usuarios_mais_ativos.update_layout(xaxis_title='Atividade em segundos', yaxis_title='',
                                                   yaxis=dict(autorange='reversed'))
        st.plotly_chart(grafico_usuarios_mais_ativos)
    

    grafico_distribuicao_por_pais = px.bar(distribuicao_por_pais_filtrado, x='País', y='Quantidade',
                                           title='Distribuição de usuários por país', text='Quantidade',
                                           color_discrete_sequence=['#00BFFF'])
    grafico_distribuicao_por_pais.update_layout(yaxis_showgrid=False)
    grafico_distribuicao_por_pais.update_traces(textposition='outside')
    st.plotly_chart(grafico_distribuicao_por_pais)
    
elif selected == 'Análise de Músicas/Artistas':
    
    st.title('Análise de Músicas/Artistas')
    
    numero_albuns = pd.read_sql_query(numero_albuns, con=engine)
    numero_albuns['Ano'] = numero_albuns['Ano'].astype(int)
    
    numero_musicas = pd.read_sql_query(numero_musicas, con=engine)
    numero_musicas['Ano'] = numero_musicas['Ano'].astype(int)
    
    numero_generos = pd.read_sql_query(numero_generos, con=engine)
    numero_generos['Ano'] = numero_generos['Ano'].astype(int)
    
    numero_musicas_skipadas = pd.read_sql_query(numero_musicas_skipadas, con=engine)
    numero_musicas_skipadas['Ano'] = numero_musicas_skipadas['Ano'].astype(int)
    
    musicas_mais_tocadas = pd.read_sql_query(musicas_mais_tocadas, con=engine)
    musicas_mais_tocadas['Ano'] = musicas_mais_tocadas['Ano'].astype(int)
    
    musicas_por_genero = pd.read_sql_query(musicas_por_genero, con=engine)
    musicas_por_genero['Ano'] = musicas_por_genero['Ano'].astype(int)
    
    artistas_mais_populares = pd.read_sql_query(artistas_mais_populares, con=engine).head(10)
        
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
        st.metric('Número de álbuns', numero_albuns_fitrado.iloc[0,0], border=True)
    with am2:
        st.metric('Número de músicas', numero_musicas_filtrado.iloc[0,0], border=True)
    with am3:
        st.metric('Número de gêneros', numero_generos_filtrado.iloc[0,0], border=True)
    with am4:
        st.metric('Número de músicas skipadas', numero_musicas_skipadas_filtrado.iloc[0,0], border=True)
    
    ama1, ama2 = st.columns(2)
    
    with ama1:
        grafico_musica_mais_tocadas = px.bar(musicas_mais_tocadas_filtrado, x='Quantidade', y='Música',
                                             title='Top 10 músicas mais tocadas', color_discrete_sequence=['#00BFFF'])
        grafico_musica_mais_tocadas.update_layout(yaxis_title=None, yaxis=dict(autorange='reversed'),
                                                  xaxis_title='Quantidade de vezes tocada')
        st.plotly_chart(grafico_musica_mais_tocadas)
    with ama2:
        grafico_artistas_mais_populares = px.bar(artistas_mais_populares, x='Seguidores', y='Artista',
                                                 color_discrete_sequence=['#00BFFF'], title='Top 10 artistas mais populares')
        grafico_artistas_mais_populares.update_layout(yaxis_title=None, yaxis=dict(autorange='reversed'))
        st.plotly_chart(grafico_artistas_mais_populares)
        
    grafico_musicas_por_genero = px.bar(musicas_por_genero_filtrado, x='Gênero', y='Músicas',
                                        color_discrete_sequence=['#00BFFF'], title='Quantidade de músicas por gênero',
                                        text='Músicas')
    grafico_musicas_por_genero.update_traces(textposition='outside')
    grafico_musicas_por_genero.update_layout(yaxis_showgrid=False)
    st.plotly_chart(grafico_musicas_por_genero)
    
elif selected == 'Análise de Assinaturas':
    
    st.title('Análise de Assinaturas')
    
    assinaturas_pagas = pd.read_sql_query(assinaturas_pagas, con=engine)
    assinaturas_falhas = pd.read_sql_query(assinaturas_falhas, con=engine)
    assinaturas_reembolsadas = pd.read_sql_query(assinaturas_reembolsadas, con=engine)
    valor_total_assinaturas_pagas = pd.read_sql_query(valor_total_assinaturas_pagas, con=engine)
    assinaturas_por_tipo_status = pd.read_sql_query(assinaturas_por_tipo_status, con=engine)
    
    total_assinaturas_pagas = valor_total_assinaturas_pagas.iloc[0]
    valor_total_assinaturas_pagas_formatado = f"R$ {total_assinaturas_pagas.iloc[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    aa1, aa2, aa3, aa4 = st.columns(4)
    
    with aa1:
        st.metric('Número de assinaturas pagas', assinaturas_pagas.loc[0], border=True)
    with aa2:
        st.metric('Número de assinaturas falhas', assinaturas_falhas.loc[0], border=True)
    with aa3:
        st.metric('Número de assinaturas reembolsadas', assinaturas_reembolsadas.loc[0], border=True)
    with aa4:
        st.metric('Valor total de assinaturas pagas', valor_total_assinaturas_pagas_formatado, border=True)
        
    grafico_assinaturas_ts = px.bar(assinaturas_por_tipo_status, x='Tipo', y='Quantidade',
                                    title='Assinaturas por tipo e status', color='Status',
                                    barmode='group', color_discrete_sequence=["#093CA8", '#00BFFF'],
                                    text='Quantidade')
    grafico_assinaturas_ts.update_layout(yaxis_showgrid=False)
    grafico_assinaturas_ts.update_traces(textposition='outside')
    st.plotly_chart(grafico_assinaturas_ts)
    
elif selected == 'Análise de Marketing':
    st.title('Análise de Marketing')
    
    orcamento_instagram = pd.read_sql_query(orcamento_instagram, con=engine)
    orcamento_instagram['Ano'] = orcamento_instagram['Ano'].astype(int)
    
    orcamento_facebook = pd.read_sql_query(orcamento_facebook, con=engine)
    orcamento_facebook['Ano'] = orcamento_facebook['Ano'].astype(int)
    
    orcamento_google_Ads = pd.read_sql_query(orcamento_google_Ads, con=engine)
    orcamento_google_Ads['Ano'] = orcamento_google_Ads['Ano'].astype(int)
    
    orcamento_tiktok = pd.read_sql_query(orcamento_tiktok, con=engine)
    orcamento_tiktok['Ano'] = orcamento_tiktok['Ano'].astype(int)
    
    orcamento_youtube = pd.read_sql_query(orcamento_youtube, con=engine)
    orcamento_youtube['Ano'] = orcamento_youtube['Ano'].astype(int)
    
    campanhas_por_canal = pd.read_sql_query(campanhas_por_canal, con=engine)
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
    
    valor_instagram = orcamento_instagram_filtrado.iloc[0, 0] 
    valor_instagram_formatado = f"R$ {valor_instagram:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    valor_facebook = orcamento_facebook_filtrado.iloc[0,0]
    valor_facebook_formatado = f"R$ {valor_facebook:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    valor_google_Ads = orcamento_google_Ads_filtrado.iloc[0,0]
    valor_google_Ads_formatado = f"R$ {valor_google_Ads:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    valor_tiktok = orcamento_tiktok_filtrado.iloc[0,0]
    valor_tiktok_formatado = f"R$ {valor_tiktok:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    valor_youtube = orcamento_youtube_filtrado.iloc[0,0]
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
                                     color_discrete_sequence=['#00BFFF'], text='Campanhas')
    grafico_campanhas_canal.update_layout(yaxis_showgrid=False, yaxis=dict(dtick=1))
    grafico_campanhas_canal.update_traces(textposition='outside')
    st.plotly_chart(grafico_campanhas_canal)