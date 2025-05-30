from hoja import Hoja
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ente import Personaje

class Arma(Hoja):
    def __init__(self, nombre: str, poder_adicional: int):
        super().__init__(nombre)
        self.poder_adicional: int = poder_adicional
        self.equipada: bool = False

    def __str__(self):
        estado = "(equipada)" if self.equipada else ""
        return f"{self.nombre} (Poder: +{self.poder_adicional}) {estado}"

    def usar(self, personaje: 'Personaje', **kwargs) -> bool:

        if 'puerta_objetivo' in kwargs:
            print(f"El item '{self.nombre}' es un arma y no se usa directamente con puertas de esta manera.")
            return False 
 
        if self.equipada:
            if personaje.poder is not None: 
                personaje.poder -= self.poder_adicional
            self.equipada = False
            print(f"{personaje.nombre} ha desequipado {self.nombre}.")
        else:
            if personaje.poder is not None:
                personaje.poder += self.poder_adicional
            self.equipada = True
            print(f"{personaje.nombre} ha equipado {self.nombre}. Su poder ahora es {personaje.poder}.")
        return True 