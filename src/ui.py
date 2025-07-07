import customtkinter as ctk
import os
from typing import Dict, Callable
from PIL import Image

class ModMenuUI(ctk.CTk):
    """
    Classe responsável exclusivamente pela interface gráfica (View).
    Ela cria os widgets e expõe métodos para serem controlados externamente.
    """
    def __init__(self, callbacks: Dict[str, Callable]):
        super().__init__()
        self.callbacks = callbacks
        self.feature_buttons: list[ctk.CTkButton] = []

        # --- Carregamento de Ícones ---
        self._load_icons()

        self._setup_window()
        self._create_widgets()

    def _load_icons(self):
        """Carrega as imagens que serão usadas como ícones na UI."""
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        
        # Ícone do Gamepad 
        self.gamepad_icon = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "gamepad_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "gamepad_icon.png")),
            size=(28, 28)
        )
        # Ícone de Dinheiro 
        self.money_icon = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "money_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "money_icon.png")),
            size=(20, 20)
        )
        # Ícone de XP 
        self.xp_icon = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "xp_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "xp_icon.png")),
            size=(20, 20)
        )

    def _setup_window(self):
        """Configura a janela principal."""
        self.title("Mod Menu do Cabana")
        self.geometry("450x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green") 

    def _create_widgets(self):
        """Cria e posiciona os widgets na janela usando o sistema de grid."""
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(1, weight=1)

        self.title_icon_label = ctk.CTkLabel(title_frame, text="", image=self.gamepad_icon)
        self.title_icon_label.grid(row=0, column=0, padx=(0, 10))

        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Aguardando Jogo...",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=1, sticky="w")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        log_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        log_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_title_label = ctk.CTkLabel(
            log_frame, text="Log de Atividades",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#AAB7C4"
        )
        log_title_label.grid(row=0, column=0, padx=10, pady=(5, 2), sticky="w")

        self.log_box = ctk.CTkTextbox(
            log_frame,
            border_width=0,
            fg_color="transparent",
            state="disabled"
        )
        self.log_box.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")


    def set_title(self, text: str):
        """Atualiza o texto do título principal."""
        self.title_label.configure(text=text)

    def add_log_message(self, message: str):
        """Adiciona uma mensagem à caixa de log."""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def create_feature_buttons(self, features: Dict[str, str]):
        """Cria dinamicamente os botões de funcionalidade com ícones."""
        self.destroy_feature_buttons()
        
        on_feature_click = self.callbacks.get('on_feature_click')
        if not on_feature_click:
            return

        for key, text in features.items():
            icon = None  # Começa sem ícone por padrão
            text_lower = text.lower()  # Converte o texto para minúsculas uma vez para eficiência
            
            # 1. Verifica se é 'dinheiro'
            if 'dinheiro' in text_lower:
                icon = self.money_icon
            # 2. Se não for dinheiro, verifica se é 'xp'
            elif 'xp' in text_lower:
                icon = self.xp_icon
            
            # Se nenhuma condição for atendida, 'icon' permanece 'None' e o botão não terá ícone.
            
            button = ctk.CTkButton(
                self.button_frame,
                text=text,
                image=icon,
                compound="left",
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=40,
                command=lambda k=key: on_feature_click(k)
            )
            button.grid(row=len(self.feature_buttons), column=0, pady=5, sticky="ew")
            self.feature_buttons.append(button)

    def destroy_feature_buttons(self):
        """Destroi todos os botões de funcionalidade existentes."""
        for button in self.feature_buttons:
            button.destroy()
        self.feature_buttons.clear()
        
    def start(self):
        """Inicia o loop principal da UI."""
        self.mainloop()