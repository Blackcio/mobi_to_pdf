import os
import subprocess
import sys
from pathlib import Path

# Configurações
LOG_FILE = "conversion_log.txt"

def log_error(message):
    """Registra erros em um arquivo de log."""
    with open(LOG_FILE, "a") as log:
        log.write(f"Erro: {message}\n")
    print(f"Erro: {message} (consulte {LOG_FILE} para mais detalhes)")

def check_calibre_installed():
    """Verifica se o Calibre está instalado e disponível no PATH."""
    try:
        subprocess.run(["ebook-convert", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        log_error("Calibre não encontrado. Certifique-se de que o Calibre está instalado e no PATH.")
        return False
    except subprocess.CalledProcessError as e:
        log_error(f"Erro ao verificar o Calibre: {e}")
        return False

def convert_ebook(input_file, output_file):
    """Converte um arquivo de e-book para outro formato usando o Calibre."""
    if not os.path.exists(input_file):
        log_error(f"Arquivo de entrada '{input_file}' não encontrado.")
        return False

    command = ["ebook-convert", input_file, output_file]

    try:
        subprocess.run(command, check=True)
        print(f"Arquivo convertido com sucesso: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Erro ao converter o arquivo: {e}")
        return False

def convert_all_mobi_in_directory(directory, output_directory):
    """Converte todos os arquivos .mobi de um diretório para .pdf."""
    if not os.path.exists(directory):
        log_error(f"Diretório de entrada '{directory}' não encontrado.")
        return

    if not os.path.exists(output_directory):
        print(f"Criando diretório de saída: {output_directory}")
        os.makedirs(output_directory)

    # Percorre todos os arquivos no diretório
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mobi"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(output_directory, filename.replace(".mobi", ".pdf"))

            print(f"\nConvertendo: {filename}...")
            if convert_ebook(input_file, output_file):
                print(f"Concluído: {output_file}")
            else:
                print(f"Falha na conversão: {filename}")

def menu():
    """Exibe o menu interativo para o usuário."""
    print("\n=== Conversor de E-books ===")
    print("1. Converter um arquivo MOBI para PDF")
    print("2. Converter todos os arquivos MOBI de um diretório para PDF")
    print("3. Sair")

    while True:
        escolha = input("\nEscolha uma opção (1, 2 ou 3): ").strip()

        if escolha == "1":
            # Conversão de um único arquivo
            input_file = input("Digite o caminho completo do arquivo MOBI: ").strip()
            output_file = input("Digite o caminho completo do arquivo PDF de saída: ").strip()

            if not input_file.lower().endswith(".mobi"):
                log_error("O arquivo de entrada deve ter a extensão .mobi.")
                continue

            if not output_file.lower().endswith(".pdf"):
                log_error("O arquivo de saída deve ter a extensão .pdf.")
                continue

            if os.path.exists(output_file):
                sobrescrever = input(f"O arquivo '{output_file}' já existe. Deseja sobrescrevê-lo? (s/n): ").strip().lower()
                if sobrescrever != 's':
                    print("Conversão cancelada.")
                    continue

            if convert_ebook(input_file, output_file):
                print("Conversão concluída com sucesso!")
            break

        elif escolha == "2":
            # Conversão de todos os arquivos .mobi de um diretório
            input_directory = input("Digite o caminho completo do diretório com os arquivos MOBI: ").strip()
            output_directory = input("Digite o caminho completo do diretório de saída para os PDFs: ").strip()

            convert_all_mobi_in_directory(input_directory, output_directory)
            break

        elif escolha == "3":
            print("Saindo...")
            sys.exit(0)

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    # Verifica se o Calibre está instalado
    if not check_calibre_installed():
        sys.exit(1)

    # Exibe o menu principal
    while True:
        menu()
