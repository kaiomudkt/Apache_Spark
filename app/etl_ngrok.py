import os
import zipfile
import requests
import subprocess
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
dotenv_path = '.env'
load_dotenv(dotenv_path)

def download_and_extract_ngrok(url: str, destination: str) -> None:
    """
    Baixa e extrai o Ngrok a partir de uma URL fornecida.
    Args:
    - url (str): URL de onde o arquivo Ngrok deve ser baixado.
    - destination (str): Diretório de destino onde o Ngrok será extraído.
    """
    # Download Ngrok
    ngrok_zip = os.path.join(destination, 'ngrok-stable-linux-amd64.zip')
    download_command = f"wget -q {url} -O {ngrok_zip}"
    os.system(download_command)
    # Extrair Ngrok
    with zipfile.ZipFile(ngrok_zip, 'r') as zip_ref:
        zip_ref.extractall(destination)
    # Remover o arquivo zip após extração
    os.remove(ngrok_zip)

def set_ngrok_auth_token(auth_token: str) -> None:
    """
    Define o token de autenticação do Ngrok.
    Args:
    - auth_token (str): Token de autenticação do Ngrok.
    """
    auth_command = f"./ngrok authtoken {auth_token}"
    os.system(auth_command)

def start_ngrok_http(port: int) -> Optional[List[Dict[str, str]]]:
    """
    Inicia o Ngrok para expor um serviço HTTP localmente e retorna informações sobre os túneis criados.
    Args:
    - port (int): Porta local onde o serviço está sendo executado.
    Returns:
    - List[Dict[str, str]]: Lista de dicionários contendo informações sobre os túneis, incluindo URLs públicas.
      Retorna None em caso de falha na inicialização do Ngrok.
    """
    try:
        # Inicia o Ngrok em segundo plano
        ngrok_process = subprocess.Popen(['./ngrok', 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ngrok_process.stdout.flush()
        # Aguarda um momento para o Ngrok iniciar completamente
        subprocess.run(['sleep', '2'])
        # Obtém as informações de túnel do Ngrok API
        tunnels_info = requests.get('http://localhost:4040/api/tunnels').json()['tunnels']
        return tunnels_info
    except Exception as e:
        print(f"Erro ao iniciar o Ngrok: {e}")
        return None

def main():
    # Define a URL para baixar o Ngrok
    ngrok_url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
    # Diretório onde o Ngrok será extraído
    ngrok_destination = './'
    # Baixa e extrai o Ngrok
    download_and_extract_ngrok(ngrok_url, ngrok_destination)
    # Define o token de autenticação do Ngrok a partir das variáveis de ambiente
    auth_token = os.getenv('NGROK_AUTH_TOKEN')
    if not auth_token:
        raise ValueError("Variável NGROK_AUTH_TOKEN não encontrada no arquivo .env")
    set_ngrok_auth_token(auth_token)
    # Inicia o Ngrok e obtém informações sobre os túneis
    port_to_expose = 4050
    tunnels_info = start_ngrok_http(port_to_expose)
    if tunnels_info:
        print("Túneis Ngrok disponíveis:")
        for tunnel in tunnels_info:
            print(f"URL pública: {tunnel['public_url']}")
    else:
        print("Falha ao iniciar o Ngrok.")

if __name__ == "__main__":
    # main()
    
    from pyngrok import ngrok, conf
    # Defina o caminho do Ngrok explicitamente
    conf.get_default().ngrok_path = "/usr/local/bin/ngrok"
    auth_token = os.getenv('NGROK_AUTH_TOKEN')
    if not auth_token:
        raise ValueError("Variável NGROK_AUTH_TOKEN não encontrada no arquivo .env")
    # Autentique com o Ngrok
    ngrok.set_auth_token(auth_token)
    # Iniciar um túnel para o servidor web local na porta 8000
    public_url = ngrok.connect(addr="8000", proto="http")
    print("URL pública do Ngrok:", public_url)
    # Exemplo: iniciar um servidor Flask ou outro aplicativo web na porta 8000
    # Aqui, você iniciaria o seu servidor Python

