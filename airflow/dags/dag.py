from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator

with DAG(
    'meu_dag',
    start_date=days_ago(1),
    schedule_interval='@daily' # executa a meia noite
) as dag:
    # task
    tarefa_01 = EmptyOperator(task_id='tarefa_01')
    tarefa_02 = EmptyOperator(task_id='tarefa_02')
    tarefa_03 = EmptyOperator(task_id='tarefa_03')
    tarefa_04 = BashOperator(
        task_id = 'criar_pasta',
        bash_command = 'mkdir -p "/home/rafael/Documentos/github/eng_dados/airflow/file"'
    )
    # Fluxo
    tarefa_01 >> [tarefa_02,tarefa_03] # tarefa 2 e 3 vão ser executadas depois que a tarefa 1 for executa
    tarefa_03 >> tarefa_04 # tarefa 4 vai ser executada depois da tarefa 3 ser executada
