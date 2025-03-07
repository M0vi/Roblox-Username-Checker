import requests
from colorama import Fore, Style
import os

def remover_acentos(texto):
    """Remove acentos e normaliza a string."""
    import unicodedata
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')

def obter_palavras_portugues():
    """Obtém uma lista de palavras em português de um arquivo local ou URL."""
    url = "https://raw.githubusercontent.com/OpenTaal/opentaal-wordlist/master/wordlist.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para status codes ruins (4xx ou 5xx)
        palavras = [remover_acentos(palavra.strip()) for palavra in response.text.splitlines()]
        return [palavra for palavra in palavras if palavra.isalpha()]  # Filtra apenas palavras válidas
    except Exception as e:
        print(f"{Fore.RED}Erro ao obter a lista de palavras: {e}{Style.RESET_ALL}")
        return []

def validate_username(username):
    """Valida um nome de usuário no Roblox usando a API."""
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            print(f"{Fore.GREEN}O nome de usuário '{username}' é válido e disponível{Style.RESET_ALL}")
            with open('valid.txt', 'a') as file:
                file.write(username + '\n')
        elif data['code'] == 1:
            print(f"{Fore.RED}O nome de usuário '{username}' já está em uso{Style.RESET_ALL}")
        elif data['code'] == 2:
            print(f"{Fore.RED}O nome de usuário '{username}' não é apropriado para Roblox{Style.RESET_ALL}")
        elif data['code'] == 10:
            print(f"{Fore.YELLOW}O nome de usuário '{username}' pode conter informações privadas{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Não foi possível acessar a API do Roblox: {e}{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Falha ao decodificar a resposta JSON da API do Roblox{Style.RESET_ALL}")

def validate_usernames_from_list(usernames):
    """Valida uma lista de nomes de usuário."""
    for username in usernames:
        validate_username(username)

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Exibe o menu principal."""
    print()
    clear_screen()
    print(f"{Fore.BLUE}██   ██  ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██████  ")
    print(f" ██ ██  ██      ██   ██ ██      ██      ██  ██  ██      ██   ██ ")
    print(f"  ███   ██      ███████ █████   ██      █████   █████   ██████  ")
    print(f" ██ ██  ██      ██   ██ ██      ██      ██  ██  ██      ██   ██ ")
    print(f"██   ██  ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██   ██ {Style.RESET_ALL}")
    print()
    print(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Escolha uma opção:")
    print(f"{Fore.MAGENTA}[{Fore.RESET}1{Fore.MAGENTA}]{Fore.RESET} Inserir um nome de usuário manualmente")
    print(f"{Fore.MAGENTA}[{Fore.RESET}2{Fore.MAGENTA}]{Fore.RESET} Verificar uma lista de nomes de usuários em português")
    print(f"{Fore.MAGENTA}[{Fore.RESET}0{Fore.MAGENTA}]{Fore.RESET} Sair")

# Main loop
if __name__ == "__main__":
    palavras_portuguesas = obter_palavras_portugues()  # Obtém a lista de palavras em português

    while True:
        display_menu()
        choice = input(f"{Fore.MAGENTA}[{Fore.RESET}>{Fore.MAGENTA}]{Fore.RESET} ")

        if choice == '1':
            username = input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Digite um nome de usuário: ")
            validate_username(username)
        elif choice == '2':
            validate_usernames_from_list(palavras_portuguesas)  # Valida as palavras em português
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}Escolha inválida{Style.RESET_ALL}")
            
