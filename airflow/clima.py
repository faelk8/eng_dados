import os 
from os.path import join
import pandas as pd 
from datetime import datetime, timedelta

import os 
from dotenv import load_dotenv
load_dotenv('/home/rafael/Documentos/utilitarios/credenciais/clima-boston.env')
key = os.getenv("key")

# intervalo de datas
data_inicio = datetime.today()
data_fim = data_inicio + timedelta(days=7)

# formatando as datas
data_inicio = data_inicio.strftime('%Y-%m-%d')
data_fim = data_fim.strftime('%Y-%m-%d')

city = 'Boston'

# unitGroup - sistema de unidade grau celsius
# include=days - para que os dados vem em dias
# contentType=csv - formato dos dados
url = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',f'{city}/{data_inicio}/{data_fim}?unitGroup=metric&include=days&key={key}&contentType=csv')

df = pd.read_csv(url)
# print(df.head())

caminho = f"/home/rafael/Documentos/github/eng_dados/dados/clima/semana-{data_inicio}/"
os.mkdir(caminho)


df.to_csv(caminho + 'dados_brutos.csv')
df[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(caminho + 'temperaturas.csv')
df[['datetime', 'description', 'icon']].to_csv(caminho + 'condicoes.csv')
