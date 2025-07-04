import datetime
from typing import Optional, Dict, Any
from src.core.memory import GameMemory
from src.config import GAME_CONFIGS
from src.utils.process import detect_running_game
from src.ui import ModMenuUI
from pymem.exception import ProcessNotFound

class ModMenuController:
    """
    Classe controladora (Controller). Gerencia o estado da aplicação,
    a lógica (memória) e comanda a UI.
    """
    def __init__(self):
        # --- Estado da Aplicação ---
        self.game_name: Optional[str] = None
        self.game_config: Optional[Dict[str, Any]] = None
        self.memory: Optional[GameMemory] = None

        # --- Conexão com a UI ---
        # Fornece os métodos desta classe como callbacks para a UI
        callbacks = {
            'on_feature_click': self._feature_callback
        }
        self.ui = ModMenuUI(callbacks=callbacks)

    def run(self):
        """Inicia o loop de verificação de status e a UI."""
        self.update_status_loop()
        self.ui.start()

    def log(self, message: str):
        """Formata a mensagem e a envia para a UI."""
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.ui.add_log_message(f"[{now}] {message}")

    def update_status_loop(self):
        """Loop principal que verifica o status do jogo periodicamente."""
        detected_game = detect_running_game(GAME_CONFIGS)
        if detected_game and detected_game[0] != self.game_name:
            self.connect_to_game(*detected_game)
        elif not detected_game and self.memory:
            self.disconnect_from_game()
        self.ui.after(3000, self.update_status_loop)

    def connect_to_game(self, game_name: str, config: Dict[str, Any]):
        self.log(f"Jogo detectado: {game_name}. Tentando conectar...")
        try:
            self.memory = GameMemory(config["process_name"])
            self.game_name = game_name
            self.game_config = config
            
            # Comanda a UI para se atualizar
            self.ui.set_title(f"Mod Menu - {game_name}")
            self.ui.create_feature_buttons(config.get("features", {}))
            self.log(f"Conectado com sucesso a '{config['process_name']}'!")
            
        except ProcessNotFound:
            self.log("Falha ao conectar. O processo pode ter fechado.")
            self.reset_state()

    def disconnect_from_game(self):
        self.log(f"Jogo '{self.game_name}' não está mais rodando.")
        self.reset_state()

    def reset_state(self):
        self.ui.destroy_feature_buttons()
        self.game_name = None
        self.game_config = None
        self.memory = None
        self.ui.set_title("Aguardando Jogo...")

    def _feature_callback(self, feature_key: str):
        """Callback para os botões. Contém a lógica de escrita na memória."""
        if not self.memory or not self.game_config:
            self.log("Erro: Não conectado ao jogo.")
            return

        offsets = self.game_config["offsets"].get(feature_key)
        if not offsets:
            self.log(f"Erro: Offsets para '{feature_key}' não encontrados.")
            return
            
        value_to_add = self.game_config.get("values_to_add", {}).get(feature_key, 10000)
        current_value = self.memory.read_int_from_chain(offsets)

        if current_value is None:
            self.log(f"Erro ao ler o valor de '{feature_key}'.")
            return

        new_value = current_value + value_to_add
        if self.memory.write_int_to_chain(offsets, new_value):
            self.log(f"{feature_key.capitalize()} adicionado! Novo valor: {new_value:,}")
        else:
            self.log(f"Erro ao escrever o novo valor de '{feature_key}'.")