from airflow import DAG 
import pendulum # para definir um data especifica
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.macros import ds_add
from os.path import join
import pandas as pd 

import os 
from dotenv import load_dotenv
load_dotenv('/home/rafael/Documentos/utilitarios/credenciais/clima-boston.env')
key = os.getenv("key")


with DAG(
    "dados-climaticos-1",
    start_date=pendulum.datetime(2024,2,1,tz="UTC"),
    # minuto, hora, dia do mes, mes, dia da semana
    schedule_interval='0 0 * * 1', # executa toda segunda feira
) as dag:
    tarefa_1 = BashOperator(
        task_id = 'criar_pasta',
        bash_command = 'mkdir -p "/home/rafael/Documentos/github/eng_dados/airflow/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
        )
    
    def extrair_dado(data_interval_end):
        city = 'Boston'
        # unitGroup - sistema de unidade grau celsius
        # include=days - para que os dados vem em dias
        # contentType=csv - formato dos dados
        url = join(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        df = pd.read_csv(url)

        caminho = f"/home/rafael/Documentos/github/eng_dados/airflow/semana={data_interval_end}/"

        df.to_csv(caminho + 'dados_brutos.csv')
        df[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(caminho + 'temperaturas.csv')
        df[['datetime', 'description', 'icon']].to_csv(caminho + 'condicoes.csv')

    tarefa_2 = PythonOperator(
        task_id = 'extrair_dados',
        python_callable = extrair_dado,
        # argumento 
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    tarefa_1 >> tarefa_2
