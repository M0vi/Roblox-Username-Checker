import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import unicodedata
import os
import time

def remover_acentos(texto):
    """Remove acentos e normaliza a string."""
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')

def extrair_palavras_dicio(url, selector):
    """Faz scraping de palavras do Dicio.com.br com tratamento de erros."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        elementos = soup.select(selector)
        
        palavras = []
        for el in elementos:
            texto = el.get_text(strip=True).lower()
            if texto and texto not in ['·', '–', '-']:  # Filtra caracteres especiais
                palavras.extend(texto.split())
        
        # Filtra e processa palavras
        palavras_filtradas = []
        for p in palavras:
            palavra_sem_acento = remover_acentos(p)
            if palavra_sem_acento.isalpha() and len(palavra_sem_acento) >= 3:
                palavras_filtradas.append(palavra_sem_acento)
        
        return list(set(palavras_filtradas))  # Remove duplicatas

    except Exception as e:
        print(f"{Fore.RED}Erro no scraping: {e}{Style.RESET_ALL}")
        return []

def obter_palavras_mais_buscadas():
    """Obtém as 100 palavras mais buscadas no Dicio."""
    url = 'https://www.dicio.com.br/palavras-mais-buscadas/'
    selector = 'div.entry-content ul li, div.entry-content p strong'
    return extrair_palavras_dicio(url, selector)[:100]  # Limita a 100 palavras

def obter_palavras_mais_usadas():
    """Obtém as palavras mais usadas do artigo do Dicio."""
    url = 'https://www.dicio.com.br/as-palavras-mais-usadas-na-lingua-portuguesa/'
    selector = 'div.entry-content h3 + ul li, div.entry-content p strong'
    return extrair_palavras_dicio(url, selector)

def validate_username(username):
    """Valida um nome de usuário na API do Roblox."""
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            print(f"{Fore.GREEN}[DISPONÍVEL] {username}{Style.RESET_ALL}")
            with open('validos.txt', 'a') as f:
                f.write(username + '\n')
        else:
            print(f"{Fore.YELLOW}[INDISPONÍVEL] {username} (Código: {data['code']}){Style.RESET_ALL}")
        
        time.sleep(1)  # Respeita o rate limit da API

    except Exception as e:
        print(f"{Fore.RED}[ERRO] {username}: {e}{Style.RESET_ALL}")

def exibir_menu():
    """Exibe o menu principal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}┌────────────────────────────────────────────┐")
    print(f"│{Fore.YELLOW} ROBLOX USERNAME CHECKER - WEB SCRAPING {Fore.CYAN}│")
    print(f"└────────────────────────────────────────────┘{Style.RESET_ALL}")
    print(f"\n{Fore.MAGENTA}[1]{Fore.RESET} Verificar palavras mais buscadas (Dicio)")
    print(f"{Fore.MAGENTA}[2]{Fore.RESET} Verificar palavras mais usadas (Dicio)")
    print(f"{Fore.MAGENTA}[3]{Fore.RESET} Verificar nome manual")
    print(f"{Fore.MAGENTA}[0]{Fore.RESET} Sair\n")

# Execução principal
if __name__ == "__main__":
    while True:
        exibir_menu()
        opcao = input(f"{Fore.MAGENTA}»{Fore.RESET} Escolha: ")

        if opcao == '1':
            print(f"\n{Fore.BLUE}Obtendo palavras mais buscadas...{Style.RESET_ALL}")
            palavras = obter_palavras_mais_buscadas()
            if palavras:
                print(f"{Fore.GREEN}Encontradas {len(palavras)} palavras!{Style.RESET_ALL}")
                for p in palavras:
                    validate_username(p)
            else:
                print(f"{Fore.RED}Falha ao obter palavras{Style.RESET_ALL}")

        elif opcao == '2':
            print(f"\n{Fore.BLUE}Obtendo palavras mais usadas...{Style.RESET_ALL}")
            palavras = obter_palavras_mais_usadas()
            if palavras:
                print(f"{Fore.GREEN}Encontradas {len(palavras)} palavras!{Style.RESET_ALL}")
                for p in palavras:
                    validate_username(p)
            else:
                print(f"{Fore.RED}Falha ao obter palavras{Style.RESET_ALL}")

        elif opcao == '3':
            username = input(f"\n{Fore.BLUE}Digite o nome de usuário: {Style.RESET_ALL}")
            validate_username(username.strip())

        elif opcao == '0':
            break

        input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
        
