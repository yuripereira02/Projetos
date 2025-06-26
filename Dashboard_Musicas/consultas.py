import sqlalchemy

DB_CONFIG = {
    "usuario": "postgres",
    "senha": "postgres",
    "host": "localhost",
    "porta": "5432",
    "nome_do_banco": "metabase",
}

engine = sqlalchemy.create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['usuario']}:{DB_CONFIG['senha']}@{DB_CONFIG['host']}:{DB_CONFIG['porta']}/{DB_CONFIG['nome_do_banco']}",
    connect_args={"client_encoding": "utf8"},
)

# Visão Geral

total_usuarios = '''
SELECT
	COUNT(id) as "Total de Usuários",
	EXTRACT(YEAR FROM data_cadastro) as "Ano"
FROM
	usuarios
GROUP BY
	"Ano"
'''

receita_total = '''
SELECT
	COALESCE(SUM(trn.valor), 0) + COALESCE(SUM(cmp.orcamento), 0) AS "Receita Total",
	EXTRACT(YEAR FROM trn.data) as "Ano"
FROM
	transacoes trn
LEFT JOIN
	assinaturas ass on trn.assinatura_id = ass.id
LEFT JOIN
	usuarios usr on ass.user_id = usr.id
LEFT JOIN
	user_campanha usc on usr.id = usc.user_id
LEFT JOIN
	campanhas cmp on usc.campanha_id = cmp.id
GROUP BY
	"Ano"
'''

musicas_ultimo_mes = '''
SELECT
	COUNT(musica_id) as "Total de Músicas",
	EXTRACT(YEAR FROM data_hora) as "Ano",
	EXTRACT(MONTH FROM data_hora) as "Mês"
FROM
	interacoes
GROUP BY
	"Ano", "Mês"
'''

taxa_cancelamento = '''
SELECT
	(select count(id) from assinaturas where status = 'cancelada') * 100 / count(id) as "Taxa de cancelamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	assinaturas
GROUP BY
	"Ano"
'''

total_usuarios_ativos = '''
select
	count(itr.id) as "Quantidade",
	case(extract(month from data_hora))
		when 01 then 'Janeiro'
		when 02 then 'Fevereiro'
		when 03 then 'Março'
		when 04 then 'Abril'
		when 05 then 'Maio'
		when 06 then 'Junho'
		when 07 then 'Julho'
		when 08 then 'Agosto'
		when 09 then 'Setembro'
		when 10 then 'Outubro'
		when 11 then 'Novembro'
		when 12 then 'Dezembro'
	end as "Mês",
	EXTRACT(YEAR FROM itr.data_hora) as "Ano"
FROM
	interacoes itr
left JOIN
	usuarios usr on itr.user_id = usr.id
LEFT JOIN
	assinaturas ass on usr.id = ass.user_id
WHERE
	ass.status = 'ativa'
group by
	EXTRACT(MONTH FROM data_hora), "Ano"
order by
	extract(month from data_hora)
'''

# Análise de Usuários

crescimento_usuarios = '''
SELECT
	COUNT(id) as "Usuários",
	CASE(EXTRACT(MONTH FROM data_cadastro))
		WHEN 01 THEN 'Janeiro'
		WHEN 02 THEN 'Fevereiro'
		WHEN 03 THEN 'Março'
		WHEN 04 THEN 'Abril'
		WHEN 05 THEN 'Maio'
		WHEN 06 THEN 'Junho'
		WHEN 07 THEN 'Julho'
		WHEN 08 THEN 'Agosto'
		WHEN 09 THEN 'Setembro'
		WHEN 10 THEN 'Outubro'
		WHEN 11 THEN 'Novembro'
		WHEN 12 THEN 'Dezembro'
	END AS "Mês",
	EXTRACT(YEAR FROM data_cadastro) AS "Ano"
FROM
	usuarios
GROUP BY
	"Mês", "Ano"
ORDER BY
	"Mês"
'''

usuarios_por_genero = '''
SELECT
	genero as "Gênero",
	COUNT(id) as "Quantidade",
	EXTRACT(YEAR FROM data_cadastro) as "Ano"
FROM
	usuarios
GROUP BY
	genero, "Ano"
'''

usuarios_mais_ativos = '''
SELECT
	usr.nome as "Usuários",
	sum(itr.duracao) as "Atividade",
	EXTRACT(YEAR FROM data_cadastro) as "Ano"
FROM
	usuarios usr
LEFT JOIN
	interacoes itr on usr.id = itr.user_id
GROUP BY
	usr.id, "Ano"
'''

distribuicao_por_pais = '''
SELECT
	pais as "País",
	COUNT(id) as "Quantidade",
	EXTRACT(YEAR FROM data_cadastro) as "Ano"
FROM
	usuarios
GROUP BY
	pais, "Ano"
'''

# Análise de Músicas/Artistas

numero_albuns = '''
SELECT
	count(id) as "Número de Álbuns",
	EXTRACT(YEAR FROM data_lancamento) as "Ano"
FROM
	albuns
GROUP BY
	"Ano"
'''

numero_musicas = '''
SELECT
	count(musicas.id) as "Número de músicas",
	EXTRACT(YEAR FROM albuns.data_lancamento) as "Ano"
FROM
	musicas
LEFT JOIN
	albuns on musicas.album_id = albuns.id
GROUP BY
	"Ano"
'''

numero_generos = '''
SELECT
	count(distinct(genero)) as "Gêneros",
	EXTRACT(YEAR FROM data_cadastro) as "Ano"
FROM
	usuarios
GROUP BY
	"Ano"
'''

numero_musicas_skipadas = '''
SELECT
	COUNT(id) as "Músicas skipadas",
	EXTRACT(YEAR FROM data_hora) as "Ano"
FROM
	interacoes
WHERE
	tipo = 'skip'
GROUP BY
	"Ano"
'''

musicas_mais_tocadas = '''
SELECT
	msc.titulo as "Música",
	count(itr.id) as "Quantidade",
	EXTRACT(YEAR FROM itr.data_hora) as "Ano"
FROM
	interacoes itr
LEFT JOIN
	musicas msc on itr.musica_id = msc.id
GROUP BY 
	msc.titulo, "Ano"
ORDER BY
	"Quantidade" DESC
'''

artistas_mais_populares = '''
SELECT
	nome as "Artista",
	seguidores as "Seguidores"
FROM
	artistas
ORDER BY
	seguidores DESC
'''

musicas_por_genero = '''
SELECT
	musicas.genero as "Gênero",
	count(musicas.id) as "Músicas",
	EXTRACT(YEAR FROM alb.data_lancamento) as "Ano"
FROM
	musicas
LEFT JOIN
	albuns alb on musicas.album_id = alb.id
GROUP BY
	musicas.genero, "Ano"
'''

# Análise de assinaturas

assinaturas_pagas = '''
SELECT
	COUNT(id)
FROM
	transacoes
WHERE
	status = 'pago'
'''

assinaturas_falhas = '''
SELECT
	COUNT(id)
FROM
	transacoes
WHERE
	status = 'falha'
'''

assinaturas_reembolsadas = '''
SELECT
	COUNT(id)
FROM
	transacoes
WHERE
	status = 'reembolsado'
'''

valor_total_assinaturas_pagas = '''
SELECT
	SUM(valor)
FROM
	transacoes
WHERE
	status = 'pago'
'''

assinaturas_por_tipo_status = '''
SELECT
	tipo as "Tipo",
	count(id) as "Quantidade",
	status as "Status"
FROM
	assinaturas
GROUP BY
	tipo, status
'''

# Análise marketing
orcamento_instagram = '''
SELECT
	sum(orcamento) as "Orçamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
WHERE
	canal = 'Instagram'
GROUP BY
	"Ano"
'''
orcamento_facebook = '''
SELECT
	sum(orcamento) as "Orçamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
WHERE
	canal = 'Facebook'
GROUP BY
	"Ano"
'''

orcamento_google_Ads = '''
SELECT
	sum(orcamento) as "Orçamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
WHERE
	canal = 'Google Ads'
GROUP BY
	"Ano"
'''

orcamento_tiktok = '''
SELECT
	sum(orcamento) as "Orçamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
WHERE
	canal = 'TikTok'
GROUP BY
	"Ano"
'''

orcamento_youtube = '''
SELECT
	sum(orcamento) as "Orçamento",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
WHERE
	canal = 'YouTube'
GROUP BY
	"Ano"
'''

campanhas_por_canal = '''
SELECT
	canal as "Canal",
	COUNT(id) as "Campanhas",
	EXTRACT(YEAR FROM data_inicio) as "Ano"
FROM
	campanhas
GROUP BY
	canal, "Ano"
'''