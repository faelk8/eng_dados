from airflow.providers.http.hooks.http import HttpHook
import requests
from datetime import datetime, timedelta
import json


class TwitterHook(HttpHook):

    def __init__(self, end_time, start_time, query, conn_id=None):
        """
         Construtor da classe que herda do Httphook.
        
        Args:
            end_time (str): Data final.
            start_time (str): Data inicial.
            query (str): Query a ser executada.
            conn_id (str, optional): ID de conexão do Airflow default None.
        """
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        self.conn_id = conn_id or "twitter_default"
        super().__init__(http_conn_id=self.conn_id)

    def create_url(self):
        """
        Cria a URL para fazer a consulta na API do Twitter.

        Retorna:
            str: URL formatada para consulta.
        """
        # formata da data para o padrão do Twitter
        TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
        end_time = self.end_time
        start_time = self.start_time
        query = self.query
        # campos que vão ser retornados
        tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
        user_fields = "expansions=author_id&user.fields=id,name,username,created_at"
        # monstagem da url para a consulta (query) - pega a base da url
        url_raw = f"{self.base_url}/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"
        return url_raw

    def connect_to_endpoint(self, url, session):
        """
        Conecta-se ao endpoint da API do Twitter.

        Args:
            url (str): URL para o endpoint da API.
            session (requests.Session): Sessão para fazer a requisição HTTP.

        Returns:
            dict: Resposta da requisição.
        """
        request = requests.Request("GET", url)
        prep = session.prepare_request(request)
        # log para informação
        self.log.info(f"URL: {url}")
        return self.run_and_check(session, prep, {})

    def paginate(self, url_raw, session):
        """
        Pagina os resultados da consulta à API do Twitter.

        Args:
            url_raw (str): URL para o endpoint da API.
            session (requests.Session): Sessão para fazer a requisição HTTP.

        Returns:
            list: Lista contendo as respostas paginadas da API.
        """        
        # lista para armazenar os dados retornados
        lista_json_response = []
        # função connect_to_endpoint reponsavel pela conexão
        response = self.connect_to_endpoint(url_raw, session)
        json_response = response.json()
        # insere o retorno na lista
        lista_json_response.append(json_response)
        contador = 1

        # paginate
        # lendo todas as páginas do retorno
        while "next_token" in json_response.get("meta",{} and contador <100): # contador para limitar a quantida de requesição
            # próximo token, só entra se existir
            next_token = json_response['meta']['next_token']
            # montando uma nova url
            url = f"{url_raw}&next_token={next_token}"
            # requisitando a próxima página
            response =  self.connect_to_endpoint(url, session)
            # converte para json
            json_response = response.json()
            # insere na lista sobrescrevendo os valores
            lista_json_response.append(json_response)
            contador += 1
        return lista_json_response
    
    def run(self):
        """
        Executa a consulta à API do Twitter. Não recebe parâmetros, executa todas as funções.

        Returns:
            list: Lista contendo as respostas paginadas da API.
        """
        # realiza as conexões
        session = self.get_conn()
        # função cria para criar a url que executa a query
        url_raw = self.create_url()
        return self.paginate(url_raw, session)

if __name__ == "__main__":
    """
    Ponto de entrada do script.

    Formata a data atual e executa uma consulta à API do Twitter usando a classe TwitterHook.
    Imprime os resultados formatados em JSON.
    """
    # formatando a data
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)
    query = "datascience"
    # percorre as paginas de retorno e faz a impressão
    for pg in TwitterHook(end_time, start_time, query).run():
        print(json.dumps(pg, indent=4, sort_keys=True))
