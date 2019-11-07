import requests
import pandas as pd


class Repositorio:
    def __init__(self, nome, url, estrelas, dataCriacao):
        self.nome = nome
        self.nameWithOwner
        self.url = url
        self.estrelas = estrelas
        self.dataCriacao = dataCriacao
        self.releases


def run_query(json, headers):  # A simple function to use requests.post to make the API call.

    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}. {}"
                        .format(request.status_code, json['query'],
                                json['variables']))


def verificar_travis_ci(nameWithOwner):
    url = "https://raw.githubusercontent.com/" + nameWithOwner + "/master/.travis.yml"
    r = requests.get(url, allow_redirects=True)
    return r.status_code == 404


def get_json(query, *params):
    json = {
        "query": query, "variables": {'cursor': params[0]} if params else {}
    }
    return json


query = """
query example($cursor: String){
  search(query: "language:python", type: REPOSITORY, first: 100, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        name
        nameWithOwner
        url
        stargazers {
            totalCount
        }
        createdAt
        releases {
          totalCount
        }
      }
    }
  }
}
"""

token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # insert your personal token here
headers = {"Authorization": "Bearer " + token}

result = run_query(get_json(query), headers)

ans = result['data']['search']['nodes']

for i in range(0, 9):
    if result['data']['search']['pageInfo']['hasNextPage']:
        result = run_query(get_json(query, result['data']['search']['pageInfo']['endCursor']), headers)
        ans += result['data']['search']['nodes']

dadosFinais = []
contador = 0

for dado in ans:
    x = {
        "nome": dado['name'],
        "nameWithOwner": dado['nameWithOwner'],
        "url": dado['url'],
        "estrelas": dado['stargazers']['totalCount'],
        "dataCriacao": dado['createdAt'],
        "releases": dado['releases']['totalCount']
    }
    h = x['releases']
    if verificar_travis_ci(x['url']) and (200 >= int(x['releases']) > 0) and contador < 5:
        dadosFinais.append(x)
        contador += 1
    if contador >= 5:
        break

df = pd.DataFrame(dadosFinais, columns=['nome', 'nameWithOwner', 'url', 'estrelas', 'dataCriacao', 'releases'])

df.to_csv("repositorios.csv", sep="\t", line_terminator="\n", index=False)
