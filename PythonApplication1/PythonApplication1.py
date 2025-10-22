import tkinter as tk
from tkinter import messagebox, ttk
import ipaddress

def calcular():
    cidr = entrada.get().strip()
    if not cidr:
        messagebox.showwarning("Aviso", "Introduz uma rede em formato CIDR (ex.: 192.168.1.0/24)")
        return

    try:
        rede = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        messagebox.showerror("Erro", "Endereço inválido! Usa formato CIDR, ex.: 192.168.1.0/24")
        return

    num_hosts = rede.num_addresses - 2 if rede.prefixlen <= 30 else 0
    primeiro = list(rede.hosts())[0] if num_hosts > 0 else "N/A"
    ultimo = list(rede.hosts())[-1] if num_hosts > 0 else "N/A"
    wildcard = ipaddress.IPv4Address(0xFFFFFFFF ^ int(rede.netmask))

    resultado = f"""
📡 Resultados da Sub-rede

➡ Endereço de Rede   : {rede.network_address}
➡ Máscara de Sub-rede: {rede.netmask}
➡ Wildcard (ACL)     : {wildcard}
➡ Broadcast          : {rede.broadcast_address}
➡ Número de Hosts    : {num_hosts}
➡ Primeiro Host      : {primeiro}
➡ Último Host        : {ultimo}
➡ Prefixo CIDR       : /{rede.prefixlen}
➡ Privada            : {"Sim" if rede.is_private else "Não"}
"""
    texto_resultado.config(state="normal")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, resultado.strip())
    texto_resultado.config(state="disabled")

def limpar():
    entrada.delete(0, tk.END)
    texto_resultado.config(state="normal")
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.config(state="disabled")

# ===== Interface Tkinter =====
janela = tk.Tk()
janela.title("Calculadora de Sub-redes")
janela.geometry("550x500")
janela.resizable(False, False)
janela.configure(bg="#101419")

# Título
titulo = tk.Label(
    janela,
    text="📶 Calculadora de Sub-redes",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#101419"
)
titulo.pack(pady=15)

# Entrada
frame_input = tk.Frame(janela, bg="#101419")
frame_input.pack(pady=5)

lbl = tk.Label(frame_input, text="Rede (CIDR):", font=("Segoe UI", 12), bg="#101419", fg="white")
lbl.grid(row=0, column=0, padx=5)

entrada = ttk.Entry(frame_input, font=("Consolas", 12), width=25)
entrada.grid(row=0, column=1, padx=5)
entrada.insert(0, "192.168.1.0/24")

# Botões
frame_botoes = tk.Frame(janela, bg="#101419")
frame_botoes.pack(pady=10)

btn_calcular = ttk.Button(frame_botoes, text="Calcular", command=calcular)
btn_calcular.grid(row=0, column=0, padx=10)

btn_limpar = ttk.Button(frame_botoes, text="Limpar", command=limpar)
btn_limpar.grid(row=0, column=1, padx=10)

# Caixa de resultados
texto_resultado = tk.Text(
    janela,
    height=15,
    width=60,
    font=("Consolas", 11),
    bg="#1C1F26",
    fg="#E8E8E8",
    relief="flat",
    wrap="word",
)
texto_resultado.pack(pady=10)
texto_resultado.config(state="disabled")

# Rodapé
rodape = tk.Label(
    janela,
    text="Feito em Python + Tkinter • Offline ✔️",
    font=("Segoe UI", 9),
    fg="#888",
    bg="#101419"
)
rodape.pack(side="bottom", pady=5)

janela.mainloop()