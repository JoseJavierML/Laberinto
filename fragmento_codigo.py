from hoja import Hoja
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ente import Personaje 

class FragmentoCodigo(Hoja):
    def __init__(self, nombre: str, pista: str):

        super().__init__(nombre)
        self.pista: str = pista
        print(f"Fragmento de Código creado: '{self.nombre}' que contiene la pista.")

    def __str__(self) -> str:
        return f"{self.nombre} (Contiene una pista)"

    def usar(self, personaje: 'Personaje', **kwargs) -> bool:
        print(f"Al examinar '{self.nombre}', lees lo siguiente: '{self.pista}'")
        return True 