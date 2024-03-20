from datetime import datetime, timedelta
import requests
import json
import os

# formatando a data
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

# data inicial
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
# data final
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)
# buscar por 
query = "datascience"

# campos retornados
tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

# url para consulta
url_raw = f"https://labdados.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

# variavel de ambiente com a key 
bearer_token = os.environ.get("BEARER_TOKEN")
# headers para requisição
headers = {"Authorization": "Bearer {}".format(bearer_token)}
# armazenando o retorno
response = requests.request("GET", url_raw, headers=headers)


# imprimir json
json_response = response.json()
# transforma em um string para o print
print(json.dumps(json_response, indent=4, sort_keys=True))

# acessando todas as paginas de retorno
while "next_token" in json_response.get("meta",{}):
    # pegar o next_token se ele existir
    next_token = json_response['meta']['next_token']
    # montando a url para pegar o valor
    url = f"{url_raw}&next_token={next_token}"
    # pega o valor
    response = requests.request("GET", url, headers=headers)
    # convertendo para json e imprimindo no console
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))