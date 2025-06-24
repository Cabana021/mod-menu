from pymem import Pymem
from pymem.exception import ProcessNotFound
from typing import List, Optional

"""
Módulo de Interação com a Memória do Jogo

Este módulo contém a classe GameMemory, responsável por ler e escrever
na memória de um processo de jogo utilizando a biblioteca Pymem.
"""

class GameMemory:
    """
    Gerencia a leitura e escrita na memória de um processo de jogo.
    """

    def __init__(self, process_name: str):
        """
        Inicializa o gerenciador de memória, tentando se anexar ao processo do jogo.
        """
        self.pm: Optional[Pymem] = None
        self.base_address: Optional[int] = None
        try:
            self.pm = Pymem(process_name)
            self.base_address = self.pm.base_address
        except ProcessNotFound:
            # Lança a exceção para que a camada superior (UI) possa tratá-la.
            raise ProcessNotFound(f"Processo '{process_name}' não encontrado.")

    def _resolve_pointer_chain(self, offsets: List[int]) -> Optional[int]:
        """
        Resolve uma cadeia de ponteiros para encontrar um endereço de memória final.
        """
        if not self.pm or self.base_address is None:
            return None

        # Começa com o endereço base do processo + o primeiro offset
        try:
            addr = self.base_address + offsets[0]
            # Itera através dos offsets restantes para seguir a cadeia de ponteiros
            for offset in offsets[1:]:
                addr = self.pm.read_int(addr) + offset
            return addr
        except Exception:
            # Se qualquer leitura falhar (ex: endereço inválido), a cadeia é inválida.
            return None

    def read_int_from_chain(self, offsets: List[int]) -> Optional[int]:
        """
        Lê um valor inteiro a partir de uma cadeia de ponteiros.
        """
        address = self._resolve_pointer_chain(offsets)
        if address and self.pm:
            try:
                return self.pm.read_int(address)
            except Exception:
                return None
        return None

    def write_int_to_chain(self, offsets: List[int], value: int) -> bool:
        """
        Escreve um valor inteiro em um endereço obtido de uma cadeia de ponteiros.
        """
        address = self._resolve_pointer_chain(offsets)
        if address and self.pm:
            try:
                self.pm.write_int(address, value)
                return True
            except Exception:
                return False
        return False