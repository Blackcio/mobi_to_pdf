import os
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

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
        messagebox.showinfo("Sucesso", f"Arquivo convertido com sucesso: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Erro ao converter o arquivo: {e}")
        messagebox.showerror("Erro", f"Erro ao converter o arquivo: {e}")
        return False

def select_input_file():
    """Abre uma janela para selecionar o arquivo MOBI de entrada."""
    input_file = filedialog.askopenfilename(
        title="Selecione o arquivo MOBI",
        filetypes=[("MOBI Files", "*.mobi")]
    )
    if input_file:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, input_file)

def select_output_file():
    """Abre uma janela para selecionar o arquivo PDF de saída."""
    output_file = filedialog.asksaveasfilename(
        title="Salvar PDF como",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if output_file:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, output_file)

def start_conversion():
    """Inicia o processo de conversão."""
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file.lower().endswith(".mobi"):
        messagebox.showerror("Erro", "O arquivo de entrada deve ter a extensão .mobi.")
        return

    if not output_file.lower().endswith(".pdf"):
        messagebox.showerror("Erro", "O arquivo de saída deve ter a extensão .pdf.")
        return

    if os.path.exists(output_file):
        overwrite = messagebox.askyesno("Sobrescrever", f"O arquivo '{output_file}' já existe. Deseja sobrescrevê-lo?")
        if not overwrite:
            return

    if convert_ebook(input_file, output_file):
        messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")

# Interface gráfica
root = tk.Tk()
root.title("Conversor de E-books")

# Frame principal
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

# Entrada do arquivo MOBI
tk.Label(main_frame, text="Arquivo MOBI:").grid(row=0, column=0, sticky="w")
input_file_entry = tk.Entry(main_frame, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(main_frame, text="Selecionar", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

# Saída do arquivo PDF
tk.Label(main_frame, text="Arquivo PDF:").grid(row=1, column=0, sticky="w")
output_file_entry = tk.Entry(main_frame, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(main_frame, text="Selecionar", command=select_output_file).grid(row=1, column=2, padx=5, pady=5)

# Botão de conversão
tk.Button(main_frame, text="Converter", command=start_conversion).grid(row=2, column=1, pady=10)

# Verifica se o Calibre está instalado
if not check_calibre_installed():
    messagebox.showerror("Erro", "Calibre não encontrado. Certifique-se de que o Calibre está instalado e no PATH.")
    sys.exit(1)

# Inicia a interface gráfica
root.mainloop()
