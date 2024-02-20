

* Faz leitura linha a linha do arquivo;
* Trata cada linha individualmente e passando para a próxima etapa;
* Paralelização dos processos em múltiplos processos simultâneos;

pcollection
* Estado da etapa em trabalho com a aplicação de processos definidos na SDK;
* A variável dengue contém o resultado dos processos das pipelines que ela recebe;
* Leitura de arquivos



# Airflow
Agendamento de pipeline 
Orquestrador de fluxos
Cria, agenda e monitora datapipelines

O Apache Airflow é uma ferramenta open source que foi criada pelo Airbnb em 2014 e atualmente faz parte da Apache Software Foundation. Trata-se de um orquestrador de fluxos, ou seja, nos permite decidir em qual momento e em quais condições nosso programa irá rodar. É utilizada principalmente para criação, monitoramento e agendamento de pipeline de dados de forma programática.

Entre as características do Apache Airflow, podemos citar que é dinâmico, porque todos os seus pipelines de dados são definidos em Python, então tudo o que conseguimos realizar nesta linguagem, também pode ser feito no Airflow; é extensível porque nos permite conectar a várias outras ferramentas do ecosistema de dados; é escalável, então uma vez que temos poder computacional suficiente, conseguimos orquestrar inúmeras quantidades de pipeline de dados independentemente da complexidade desses pipelines; é elegante, porque conseguimos desenvolver datas pipelines de forma enxuta e direta; e, por fim, possui uma interface web útil e fácil de utilizar.

O fato de ser uma ferramenta open source configura uma vantagem porque conseguimos compartilhar melhorias e interagir com a comunidade. Além disso, é muito utilizado para desenvolvimento de pipelines ETL e ELT, treinamento de modelos de Machine Learning, geração de relatórios automatizada e backups automáticos.

* Dinâmino
* Extendível
* Escalável
* Elegante
* Interface Web

Caso de Uso
* Pipelines ETL/ELT
* Treinamento de modelos de Machine Learning
* Geração de relatório automatizada
* Backups automáticos

Agendamento de execução automática
DAG: Fluxo de trabalho
Task: Tarefas para serem executadas
DAG Run: Execução do DAG 
Task Instance
Operator: Bloco de execução

DAG: fluxo de trabalho definido em Python.
Task: unidade mais básica de um DAG.
Operator: encapsula a lógica para fazer uma unidade de trabalho (task).


A instalação do Airflow geralmente consiste nos seguintes componentes principais:

Webserver: apresenta uma interface de usuário que nos permite inspecionar, acionar e acompanhar o comportamento dos DAGs e suas tarefas;
Pasta de arquivos DAG: armazena os arquivos DAGs criados. Ela é lida pelo agendador e executor;
Scheduler (agendador): lida com o acionamento dos fluxos de trabalho (DAGs) agendados e o envio de tarefas para o executor;
Banco de dados: usado pelo agendador, executor e webserver para armazenar os metadados e status do DAG e suas tarefas;
Executor: lida com as tarefas em execução. O Airflow possui vários executores, mas apenas um é utilizado por vez.

# Instalação 

```
pip install "apache-airflow[celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt"
```

Iniciando o serviço
```
airflow standalone
```

admin 
HUhHD28rERfyzbvA