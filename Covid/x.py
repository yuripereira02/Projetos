import pandas as pd

df = pd.read_parquet('dados_covid19_agregado.parquet')

df.to_excel('dados_covid19_agregado.xlsx')