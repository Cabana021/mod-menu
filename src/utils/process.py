import psutil
from typing import Optional, Tuple, Dict, Any

"""
Módulo de Utilitários de Processo

Fornece funções para interagir com os processos do sistema operacional,
como verificar se um processo está em execução e detectar qual dos
jogos suportados está ativo.
"""

def is_process_running(process_name: str) -> bool:
    """
    Verifica se um processo com o nome especificado está atualmente em execução.
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == process_name.lower():
            return True
    return False

def detect_running_game(game_configs: Dict[str, Any]) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Detecta qual dos jogos configurados está em execução.
    """
    for game_name, config in game_configs.items():
        if is_process_running(config["process_name"]):
            return game_name, config
    return None