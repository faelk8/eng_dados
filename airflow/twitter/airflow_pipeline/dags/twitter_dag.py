import sys
sys.path.append("airflow_pipeline")

from airflow.models import DAG
from operators.twitter_operator import TwitterOperator
from os.path import join
from airflow.utils.dates import days_ago

with DAG(dag_id = "TwitterDAG", start_date=days_ago(2), schedule_interval="@daily") as dag:
    """
    Agenda a execução de cada tarefa (operador), executa buscando dados de 2 dias atrás.
    A data é ajusta pelo DAG, executa diariamente.
    Aqui chama a classe e passa os parâmentros coforme definido no operador.
    """
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
    query = "datascience"

    to = TwitterOperator(file_path=join("datalake/twitter_datascience",
                                        "extract_date={{ ds }}",
                                        "datascience_{{ ds_nodash }}.json"),
                                        query=query,
                                        start_time="{{ data_interval_start.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        end_time="{{ data_interval_end.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        task_id="twitter_datascience")