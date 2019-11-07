import os
import shutil
from datetime import time

import pandas as pd
import requests
from func_timeout import func_timeout, FunctionTimedOut
import git


#Remove arquivos com permissão apenas para leitura
def remove_readonly(func, path, _):
    os.chmod(path, os.stat.S_IWRITE)
    func(path)


def clonar_repositorios(repositorios, directory='Repo\\'):
    i = 0
    while i < 5:
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
            if os.path.exists(directory):
                shutil.rmtree(directory, onerror=remove_readonly)
        os.makedirs('Repo\\')
        repo = repositorios[i].values[0]  # pegando o nome do repositório
        url = repositorios[i].values[1]  # pegando a url do repositório
        print('Clonando repositório', repo)

        try:
            data = func_timeout(600, git.Repo.clone_from, args=(url, 'Repo\\'))
        except FunctionTimedOut:
            print('Tempo limite excedido ao tentar clonar repositório')
            os.system('taskkill /f /im git.exe')
            time.sleep(5)
            continue
        except Exception:
            print('Ocorreu um erro ao clonar o repositório')


if __name__ == '__main__':
    repositorios = pd.read_csv('repositorios.csv', sep='\t', lineterminator='\n')
    clonar_repositorios(repositorios)
