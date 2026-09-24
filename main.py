import hashlib
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from supabase import create_client, Client

# Configurações do Supabase (mesmas chaves validadas)
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_KEY = "sua-chave-anon-aqui"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class DarkkanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Darkkan - Sistema de Proteção")
        self.geometry("750x550")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- TELA DE LOGIN ---
    def show_login_screen(self):
        self.clear_container()

        title = ctk.CTkLabel(self.container, text="Darkkan - Login", font=("Arial", 22, "bold"))
        title.pack(pady=30)

        self.email_entry = ctk.CTkEntry(self.container, placeholder_text="E-mail", width=300, height=40)
        self.email_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self.container, placeholder_text="Senha", show="*", width=300, height=40)
        self.pass_entry.pack(pady=10)

        btn_login = ctk.CTkButton(self.container, text="Entrar", fg_color="#1f538d", width=300, height=40, command=self.fazer_login)
        btn_login.pack(pady=15)

        btn_ir_cadastro = ctk.CTkButton(self.container, text="Criar Conta Nova", fg_color="transparent", text_color="#1f538d", hover=False, command=self.show_signup_screen)
        btn_ir_cadastro.pack(pady=5)

    # --- TELA DE CADASTRO ---
    def show_signup_screen(self):
        self.clear_container()

        title = ctk.CTkLabel(self.container, text="Criar Conta no Darkkan", font=("Arial", 22, "bold"))
        title.pack(pady=30)

        self.reg_email = ctk.CTkEntry(self.container, placeholder_text="Seu E-mail", width=300, height=40)
        self.reg_email.pack(pady=10)

        self.reg_pass = ctk.CTkEntry(self.container, placeholder_text="Sua Senha", show="*", width=300, height=40)
        self.reg_pass.pack(pady=10)

        btn_cadastrar = ctk.CTkButton(self.container, text="Cadastrar Conta", fg_color="green", width=300, height=40, command=self.fazer_cadastro)
        btn_cadastrar.pack(pady=15)

        btn_voltar = ctk.CTkButton(self.container, text="Voltar para o Login", fg_color="transparent", text_color="gray", hover=False, command=self.show_login_screen)
        btn_voltar.pack(pady=5)

    def fazer_login(self):
        email = self.email_entry.get().strip()
        senha = self.pass_entry.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": senha})
            if response.user:
                self.usuario_atual = email
                self.show_workspace_screen()
        except Exception as e:
            messagebox.showerror("Erro ao Entrar", str(e))

    def fazer_cadastro(self):
        email = self.reg_email.get().strip()
        senha = self.reg_pass.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            response = supabase.auth.sign_up({"email": email, "password": senha})
            messagebox.SUCCESS = messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça o login.")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e))

    # --- ÁREA DE TRABALHO & MÓDULO DE VÍDEO (FASE 2) ---
    def show_workspace_screen(self):
        self.clear_container()

        lbl_user = ctk.CTkLabel(self.container, text=f"Logado como: {self.usuario_atual}", font=("Arial", 12))
        lbl_user.pack(pady=10)

        title = ctk.CTkLabel(self.container, text="Área de Proteção de Vídeos", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Botão para selecionar o vídeo
        btn_selecionar = ctk.CTkButton(self.container, text="Selecionar Vídeo do Canal (.mp4 / .mkv)", fg_color="#2b2b2b", hover_color="#3b3b3b", width=350, height=45, command=self.selecionar_video)
        btn_selecionar.pack(pady=15)

        # Caixa de informações do vídeo
        self.info_box = ctk.CTkTextbox(self.container, width=650, height=200)
        self.info_box.pack(pady=10)
        self.info_box.insert("0.0", "Nenhum vídeo selecionado.\nClique no botão acima para carregar o arquivo e gerar a assinatura digital de proteção.")
        self.info_box.configure(state="disabled")

        btn_sair = ctk.CTkButton(self.container, text="Sair da Conta", fg_color="red", width=200, height=35, command=self.show_login_screen)
        btn_sair.pack(pady=15)

    def selecionar_video(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o vídeo para proteção",
            filetypes=[("Arquivos de Vídeo", "*.mp4 *.mkv *.avi *.mov"), ("Todos os arquivos", "*.*")]
        )

        if caminho_arquivo:
            nome_arquivo = os.path.basename(caminho_arquivo)
            tamanho_bytes = os.path.getsize(caminho_arquivo)
            tamanho_mb = tamanho_bytes / (1024 * 1024)

            # Calculando o Hash SHA-256 do arquivo para assinatura digital
            self.info_box.configure(state="normal")
            self.info_box.delete("0.0", "end")
            self.info_box.insert("0.0", f"Analisando arquivo: {nome_arquivo}...\nCalculando impressões digitais de segurança...")
            self.update()

            hash_sha256 = hashlib.sha256()
            with open(caminho_arquivo, "rb") as f:
                for chunk in iter(lambda: f.read(4096 * 1024), b""):
                    hash_sha256.update(chunk)
            
            file_hash = hash_sha256.hexdigest()

            # Exibindo os dados processados
            resultado = (
                f"[ARQUIVO CARREGADO COM SUCESSO]\n"
                f"• Nome: {nome_arquivo}\n"
                f"• Caminho: {caminho_arquivo}\n"
                f"• Tamanho: {tamanho_mb:.2f} MB\n"
                f"• Hash SHA-256 (Impressão Digital): {file_hash}\n\n"
                f"Status: Pronto para aplicação de blindagem de metadados contra Content ID!"
            )

            self.info_box.delete("0.0", "end")
            self.info_box.insert("0.0", resultado)
            self.info_box.configure(state="disabled")

if __name__ == "__main__":
    app = DarkkanApp()
    app.mainloop()