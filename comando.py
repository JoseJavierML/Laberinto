from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, List 

if TYPE_CHECKING:
    from juego import Juego  

class Comando(ABC):
    @abstractmethod
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        pass