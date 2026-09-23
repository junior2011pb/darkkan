import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from supabase import create_client, Client

# --- CONFIGURAÇÃO DO SUPABASE ---
# Cole aqui os dados que você pegou no painel do Supabase
SUPABASE_URL = "https://lmfhjdutrzugmjcoxzti.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxtZmhqZHV0cnp1Z21qY294enRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAxNDM0NjMsImV4cCI6MjEwNTcxOTQ2M30.3u0q-v8zU_Mc3gmcLAUjnwBx10QJfLztDZAWrvwWmMI"

# Inicializa a conexão com o banco de dados
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Darkkan - Sistema de Proteção")
        self.geometry("400x450")
        self.resizable(False, False)

        # Inicia mostrando a tela de login
        self.mostrar_tela_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- TELA DE LOGIN ---
    def mostrar_tela_login(self):
        self.limpar_tela()

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

    # --- TELA DE CADASTRO ---
    def mostrar_tela_cadastro(self):
        self.limpar_tela()

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

    # --- LÓGICA DE CADASTRO NO SUPABASE ---
    def fazer_cadastro(self):
        email = self.entry_cad_email.get()
        senha = self.entry_cad_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if not supabase:
            messagebox.showerror("Erro", "Supabase não configurado corretamente no código!")
            return

        try:
            response = supabase.auth.sign_up({"email": email, "password": senha})
            messagebox.showinfo("Sucesso!", "Conta criada com sucesso! Faça login para continuar.")
            self.mostrar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e))

    # --- LÓGICA DE LOGIN NO SUPABASE ---
    def fazer_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha o e-mail e a senha!")
            return

        if not supabase:
            messagebox.showerror("Erro", "Supabase não configurado corretamente no código!")
            return

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": senha})
            self.mostrar_tela_principal(email)
        except Exception as e:
            messagebox.showerror("Erro de Login", "E-mail ou senha incorretos.")

    # --- TELA PRINCIPAL ---
    def mostrar_tela_principal(self, email_usuario):
        self.limpar_tela()
        self.geometry("600x500")

        lbl_boas_vindas = ctk.CTkLabel(self, text=f"Logado como: {email_usuario}", font=("Arial", 14))
        lbl_boas_vindas.pack(pady=15)

        titulo = ctk.CTkLabel(self, text="Área de Trabalho - Sistema Pronto", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        self.lbl_status = ctk.CTkLabel(self, text="Conexão com a nuvem e banco de dados ativas!", font=("Arial", 12), text_color="green")
        self.lbl_status.pack(pady=20)

        btn_sair = ctk.CTkButton(self, text="Sair da Conta", fg_color="red", hover_color="darkred", command=self.mostrar_tela_login, width=150, height=35)
        btn_sair.pack(side="bottom", pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()