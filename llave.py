from hoja import Hoja
from ente import Personaje
from puerta import Puerta, PuertaConLlaveGenerica

class Llave(Hoja):
    def __init__(self, nombre: str = "Llave Común"):
        super().__init__(nombre)

    def __str__(self):
        return f"{self.nombre} (Un solo uso)"

    def usar(self, personaje: 'Personaje', **kwargs) -> bool:
        
        puerta_objetivo = kwargs.get('puerta_objetivo')

        if not isinstance(puerta_objetivo, PuertaConLlaveGenerica):
            print(f"{self.nombre} no se puede usar en un {type(puerta_objetivo).__name__}. Se esperaba una puerta con cerradura.")
            return False

        if puerta_objetivo.esta_bloqueada: 
            if puerta_objetivo.desbloquear_con_llave(): 
                print(f"{personaje.nombre} ha usado {self.nombre} para desbloquear {getattr(puerta_objetivo, 'nombre', 'la puerta')}.")
                return True 
            else:
                print(f"{self.nombre} no pudo desbloquear {getattr(puerta_objetivo, 'nombre', 'la puerta')}.")
                return False
        else: 
            print(f"{getattr(puerta_objetivo, 'nombre', 'La puerta')} ya está desbloqueada. No se usó {self.nombre}.")
            return False