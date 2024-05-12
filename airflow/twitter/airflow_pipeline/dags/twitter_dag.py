import sys
sys.path.append("airflow_pipeline")

from airflow.models import DAG
from datetime import datetime, timedelta
from operators.twitter_operator import TwitterOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from os.path import join
from airflow.utils.dates import days_ago
from pathlib import Path

with DAG(dag_id = "TwitterDAG", start_date=days_ago(2), schedule_interval="@daily") as dag:
    """
    Agenda a execução de cada tarefa (operador), executa buscando dados de 2 dias atrás.
    A data é ajusta pelo DAG e executa diariamente.
    Aqui chama a classe e passa os parâmentros coforme definido no operador.

    DAG:
        TwitterOperator: Coleta os dados
        SparkSubmitOperator: Realiza o processamento dos dados
    """
    # 
    BASE_FOLDER = join(
       str(Path("~/MEGA").expanduser()), # pega todo o caminho anterior 
       "github/eng_dados/airflow/twitter/datalake/{stage}/twitter_datascience/{partition}", # estage bronse, silver, golde - partitions - data da extração
    )
    # data da extração
    PARTITION_FOLDER_EXTRACT = "extract_date={{ data_interval_start.strftime('%Y-%m-%d') }}"
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
    query = "datascience"

    twitter_operator = TwitterOperator(file_path=join(BASE_FOLDER.format(stage="bronze",partition=PARTITION_FOLDER_EXTRACT),
                                        "datascience_{{ ds_nodash }}.json"),
                                        query=query,
                                        start_time="{{ data_interval_start.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        end_time="{{ data_interval_end.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        task_id="twitter_datascience")
    
    twitter_transform = SparkSubmitOperator(task_id="transform_twitter_datascience",
                                            application="/home/rafael/MEGA/github/eng_dados/airflow/twitter/airflow_pipeline/operators/transformation.py",
                                            name="twitter_transformation",
                                            application_args=["--src", BASE_FOLDER.format(stage="bronze", partition=PARTITION_FOLDER_EXTRACT),
                                             "--dest", BASE_FOLDER.format(stage="silver", partition=""),
                                             "--process-date", "{{ ds }}"])
    
    twitter_insight = SparkSubmitOperator(task_id="insight_twitter",
                                            application="/home/rafael/MEGA/github/eng_dados/airflow/twitter/airflow_pipeline/operators/insight_tweet.py",
                                            name="insight_twitter",
                                            application_args=["--src", BASE_FOLDER.format(stage="silver", partition=""),
                                             "--dest", BASE_FOLDER.format(stage="gold", partition=""),
                                             "--process-date", "{{ ds }}"])

twitter_operator >> twitter_transform >> twitter_insight
    