import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title='Dashboard Musicas', page_icon='bar_chart', layout='wide')

def load_llm(id_model, temperature):
    return ChatGroq(
        model = id_model,
        temperature = temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )


def build_prompt(artistas_mais_populares, assinaturas_falhas, assinaturas_pagas, assinaturas_por_tipo_status,
                assinaturas_reembolsadas, campanhas_por_canal, crescimento_usuarios, distribuicao_por_pais,
                musicas_mais_tocadas, musicas_por_genero, musicas_ultimo_mes, numero_albuns, numero_generos,
                numero_musicas_skipadas, numero_musicas, orcamento_facebook, orcamento_google_Ads, orcamento_instagram,
                orcamento_tiktok, orcamento_youtube, receita_total, taxa_cancelamento, total_usuarios_ativos,
                total_usuarios, usuarios_mais_ativos, usuarios_por_genero, valor_total_assinaturas_pagas, input):

    prompt = f'''
        Você é especializado nos dados destas bases de dados:
        Artistas mais populares:
        {artistas_mais_populares},
        
        Assinaturas falhas:
        {assinaturas_falhas},
        
        Assinaturas pagas:
        {assinaturas_pagas},
        
        Assinaturas por tipo e status:
        {assinaturas_por_tipo_status},
        
        Assinaturas reembolsadas:
        {assinaturas_reembolsadas},
        
        Campanhas por canal:
        {campanhas_por_canal},
        
        Crescimento usuários:
        {crescimento_usuarios},
        
        Distribuição por país:
        {distribuicao_por_pais},
        
        Músicas mais tocadas:
        {musicas_mais_tocadas},
        
        Músicas por gênero:
        {musicas_por_genero},
        
        Músicas no último mês:
        {musicas_ultimo_mes},
        
        Número de álbuns:
        {numero_albuns},
        
        Número por gênero:
        {numero_generos},
        
        Número de músicas skipadas:
        {numero_musicas_skipadas},
        
        Número de músicas:
        {numero_musicas},
        
        Orçamento facebook:
        {orcamento_facebook},
        
        Orçamento Google Ads:
        {orcamento_google_Ads},
        
        Orçamento Instagram:
        {orcamento_instagram},
        
        Orçamento Tiktok:
        {orcamento_tiktok},
        
        Orçamento YouTube:
        {orcamento_youtube},

        Receita Total:
        {receita_total},
        
        Taxa de cancelamento:
        {taxa_cancelamento},
        
        Total de usuários ativos:
        {total_usuarios_ativos},
        
        Total de usuários:
        {total_usuarios},
        
        Usuários mais ativos:
        {usuarios_mais_ativos},

        Usuários por gênero:
        {usuarios_por_genero},
        
        Valor total de assinaturas pagas:
        {valor_total_assinaturas_pagas}

        Com base nessas informações responda isto: {input}
    '''
    return prompt

def format_res(res, return_thinking=False):
    res = res.strip()
    if return_thinking:
        res = res.replace("<think>", "[pensando...] ")
        res = res.replace("</think>", "\n---\n")
    else:
        if "</think>" in res:
            res = res.split("</think>")[-1].strip()
    return res

st.navigation(pages=[st.Page('visao_geral.py', title='Visão Geral'),
                    st.Page('analise_users.py', title='Análise de Usuários'),
                    st.Page('analise_musica_artista.py', title='Análise de Músicas/Artistas'),
                    st.Page('analise_assinaturas.py', title='Análise de Assinaturas'),
                    st.Page('analise_marketing.py', title='Análise de Marketing')],
                    position='sidebar').run()



id_model = "deepseek-r1-distill-llama-70b"
temperature = 0.7

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANILHAS_DIR = os.path.join(BASE_DIR, 'planilhas')

artistas_mais_populares = pd.read_excel(os.path.join(PLANILHAS_DIR, 'artistas_mais_populares.xlsx')).head(10)
assinaturas_falhas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_falhas.xlsx'))
assinaturas_pagas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_pagas.xlsx'))
assinaturas_por_tipo_status = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_por_tipo_status.xlsx'))
assinaturas_reembolsadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'assinaturas_reembolsadas.xlsx'))
campanhas_por_canal = pd.read_excel(os.path.join(PLANILHAS_DIR, 'campanhas_por_canal.xlsx'))
crescimento_usuarios = pd.read_excel(os.path.join(PLANILHAS_DIR, 'crescimento_usuarios.xlsx'))
distribuicao_por_pais = pd.read_excel(os.path.join(PLANILHAS_DIR, 'distribuicao_por_pais.xlsx'))
musicas_mais_tocadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_mais_tocadas.xlsx'))
musicas_por_genero = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_por_genero.xlsx'))
musicas_ultimo_mes = pd.read_excel(os.path.join(PLANILHAS_DIR, 'musicas_ultimo_mes.xlsx'))
numero_albuns = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_albuns.xlsx'))
numero_generos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_generos.xlsx'))
numero_musicas_skipadas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_musicas_skipadas.xlsx'))
numero_musicas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'numero_musicas.xlsx'))
orcamento_facebook = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_facebook.xlsx'))
orcamento_google_Ads = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_google_Ads.xlsx'))
orcamento_instagram = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_instagram.xlsx'))
orcamento_tiktok = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_tiktok.xlsx'))
orcamento_youtube = pd.read_excel(os.path.join(PLANILHAS_DIR, 'orcamento_youtube.xlsx'))
receita_total = pd.read_excel(os.path.join(PLANILHAS_DIR, 'receita_total.xlsx'))
taxa_cancelamento = pd.read_excel(os.path.join(PLANILHAS_DIR, 'taxa_cancelamento.xlsx'))
total_usuarios_ativos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'total_usuarios_ativos.xlsx'))
total_usuarios = pd.read_excel(os.path.join(PLANILHAS_DIR, 'total_usuarios.xlsx'))
usuarios_mais_ativos = pd.read_excel(os.path.join(PLANILHAS_DIR, 'usuarios_mais_ativos.xlsx'))
usuarios_por_genero = pd.read_excel(os.path.join(PLANILHAS_DIR, 'usuarios_por_genero.xlsx'))
valor_total_assinaturas_pagas = pd.read_excel(os.path.join(PLANILHAS_DIR, 'valor_total_assinaturas_pagas.xlsx'))

st.sidebar.header('📌 Faça suas perguntas aqui:')
input = st.sidebar.chat_input(placeholder='Pergunte alguma coisa')

if input:
    llm = load_llm(id_model, temperature)
    prompt = build_prompt(artistas_mais_populares, assinaturas_falhas, assinaturas_pagas, assinaturas_por_tipo_status,
                    assinaturas_reembolsadas, campanhas_por_canal, crescimento_usuarios, distribuicao_por_pais,
                    musicas_mais_tocadas, musicas_por_genero, musicas_ultimo_mes, numero_albuns, numero_generos,
                    numero_musicas_skipadas, numero_musicas, orcamento_facebook, orcamento_google_Ads, orcamento_instagram,
                    orcamento_tiktok, orcamento_youtube, receita_total, taxa_cancelamento, total_usuarios_ativos,
                    total_usuarios, usuarios_mais_ativos, usuarios_por_genero, valor_total_assinaturas_pagas, input)
    res = llm.invoke(prompt)
    res_formatado = format_res(res.content, return_thinking=False)
    st.sidebar.markdown(res_formatado)
