"""
Módulo de Configuração

Centraliza todas as configurações do mod menu, como nomes de processos e
endereços de memória (offsets) para diferentes jogos. A estrutura foi
projetada para ser facilmente extensível.
"""

# Dicionário principal que agrupa as configurações por jogo.
# Facilita a seleção do jogo alvo no menu principal e a adição de novos jogos no futuro.

GAME_CONFIGS = {
    "FlatOut 2": {
        "process_name": "FlatOut2.exe",
        "features": {
            "money": "Adicionar Dinheiro" 
        },
        
        "offsets": {
            "money": [0x4E8418, 0x1C, 0x64, 0x14, 0x30, 0x14, 0x58, 0xE58] 
        },
        "values_to_add": {
            "money": 1500000
        }
    },
    
    # Espaço reservado para futuros jogos
    "": {
        "process_name": "(game).exe",
        "features": {
            "money": "Adicionar Dinheiro",
            "xp": "Adicionar XP",
        },
        "offsets": {
            "money": [],
            "xp":    []
        },
        "values_to_add": {
            "money": 1,
            "xp": 1,
        }
    }
}