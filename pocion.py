from hoja import Hoja
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ente import Personaje 

class PocionCuracion(Hoja):
    def __init__(self, nombre: str, puntos_vida_recuperados: int):
        super().__init__(nombre)
        self.puntos_vida_recuperados: int = puntos_vida_recuperados

    def __str__(self):
        return f"{self.nombre} (Cura: +{self.puntos_vida_recuperados} PV)"

    def usar(self, personaje: 'Personaje', **kwargs) -> bool: 
        
        vidas_maximas = getattr(personaje, 'vidas_maximas', personaje.vidas + self.puntos_vida_recuperados + 1) 
                                                                      
        if personaje.vidas < vidas_maximas:
            vida_anterior = personaje.vidas
            personaje.vidas += self.puntos_vida_recuperados
            if personaje.vidas > vidas_maximas and hasattr(personaje, 'vidas_maximas'): 
                 personaje.vidas = vidas_maximas
            curacion_efectiva = personaje.vidas - vida_anterior
            print(f"{personaje.nombre} ha usado {self.nombre} y recuperado {curacion_efectiva} puntos de vida. Vidas actuales: {personaje.vidas}.")
            return True 
        else:
            print(f"{personaje.nombre} ya tiene la vida al máximo. No se usó {self.nombre}.")
            return False 