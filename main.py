import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from supabase import create_client, Client
import hashlib
import os

SUPABASE_URL = "https://lmfhjdutrzugmjcoxzti.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxtZmhqZHV0cnp1Z21qY294enRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAxNDM0NjMsImV4cCI6MjEwNTcxOTQ2M30.3u0q-v8zU_Mc3gmcLAUjnwBx10QJfLztDZAWrvwWmMI"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Darkkan - Sistema de Proteção")
        self.geometry("400x450")
        self.resizable(False, False)
        self.usuario_atual = ""
        self.mostrar_tela_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela_login(self):
        self.limpar_tela()
        self.geometry("400x450")
        titulo = ctk.CTkLabel(self, text="Entrar no Sistema", font=("Arial", 20, "bold"))
        titulo.pack(pady=30)
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Seu e-mail", width=300, height=40)
        self.entry_email.pack(pady=10)
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Sua senha", show="*", width=300, height=40)
        self.entry_senha.pack(pady=10)
        btn_entrar = ctk.CTkButton(self, text="Entrar", command=self.fazer_login, width=300, height=40)
        btn_entrar.pack(pady=20)
        btn_ir_cadastro = ctk.CTkButton(self, text="Não tem conta? Cadastre-se", fg_color="transparent", text_color=("gray10", "gray90"), command=self.mostrar_tela_cadastro)
        btn_ir_cadastro.pack(pady=5)

    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        self.geometry("400x450")
        titulo = ctk.CTkLabel(self, text="Criar Nova Conta", font=("Arial", 20, "bold"))
        titulo.pack(pady=30)
        self.entry_cad_email = ctk.CTkEntry(self, placeholder_text="Seu melhor e-mail", width=300, height=40)
        self.entry_cad_email.pack(pady=10)
        self.entry_cad_senha = ctk.CTkEntry(self, placeholder_text="Crie uma senha", show="*", width=300, height=40)
        self.entry_cad_senha.pack(pady=10)
        btn_cadastrar = ctk.CTkButton(self, text="Cadastrar Conta", fg_color="green", hover_color="darkgreen", command=self.fazer_cadastro, width=300, height=40)
        btn_cadastrar.pack(pady=20)
        btn_voltar = ctk.CTkButton(self, text="Voltar para o Login", fg_color="transparent", text_color=("gray10", "gray90"), command=self.mostrar_tela_login)
        btn_voltar.pack(pady=5)

    def fazer_cadastro(self):
        email = self.entry_cad_email.get()
        senha = self.entry_cad_senha.get()
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        try:
            supabase.auth.sign_up({"email": email, "password": senha})
            messagebox.showinfo("Sucesso!", "Conta criada com sucesso! Faça login.")
            self.mostrar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e))

    def fazer_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha o e-mail e a senha!")
            return
        try:
            supabase.auth.sign_in_with_password({"email": email, "password": senha})
            self.usuario_atual = email
            self.mostrar_workspace_screen()
        except Exception:
            messagebox.showerror("Erro de Login", "E-mail ou senha incorretos.")

    def mostrar_workspace_screen(self):
        self.limpar_tela()
        self.geometry("740x520")
        lbl_user = ctk.CTkLabel(self, text=f"Logado como: {self.usuario_atual}", font=("Arial", 12, "bold"))
        lbl_user.pack(pady=(15, 5))
        title = ctk.CTkLabel(self, text="Área de Proteção de Vídeos - Fase 2", font=("Arial", 20, "bold"))
        title.pack(pady=5)
        btn_selecionar = ctk.CTkButton(self, text="Selecionar Vídeo do Canal (.mp4 / .mkv)", fg_color="#1f538d", hover_color="#143d6a", width=350, height=45, command=self.selecionar_video)
        btn_selecionar.pack(pady=10)
        self.info_box = ctk.CTkTextbox(self, width=680, height=240)
        self.info_box.pack(pady=10)
        self.info_box.insert("0.0", "Nenhum vídeo selecionado.\nClique no botão acima para carregar o arquivo e gerar a impressão digital (hash).")
        self.info_box.configure(state="disabled")
        btn_sair = ctk.CTkButton(self, text="Sair da Conta", fg_color="red", hover_color="darkred", width=200, height=35, command=self.mostrar_tela_login)
        btn_sair.pack(pady=10)

    def selecionar_video(self):
        caminho_arquivo = filedialog.askopenfilename(title="Selecione o vídeo", filetypes=[("Vídeos", "*.mp4 *.mkv *.avi *.mov"), ("Todos", "*.*")])
        if not caminho_arquivo:
            return
        nome_arquivo = os.path.basename(caminho_arquivo)
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        sha256_hash = hashlib.sha256()
        with open(caminho_arquivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
        resultado = f"[VÍDEO CARREGADO]\n• Nome: {nome_arquivo}\n• Tamanho: {tamanho_mb:.2f} MB\n• Hash SHA-256: {file_hash}\n\nPronto para blindagem!"
        self.info_box.configure(state="normal")
        self.info_box.delete("0.0", "end")
        self.info_box.insert("0.0", resultado)
        self.info_box.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()