import time
from modo import Modo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bicho import Bicho      
    from ente import Personaje
    from estado_ente import Vivo  

class Perezoso(Modo):
    def __init__(self):
        super().__init__()

    def dormir(self, bicho: 'Bicho'):
        nombre_bicho = getattr(bicho, 'nombre', 'Perezoso')
        print(f"{nombre_bicho}: Durmiendo profundamente...")
        time.sleep(1) 
        
    def caminar(self, bicho: 'Bicho'):
        nombre_bicho = getattr(bicho, 'nombre', 'Perezoso')
        # print(f"{nombre_bicho}: Deambulando sin prisa...")
        pass 

    def atacar(self, bicho: 'Bicho', personaje_objetivo: 'Personaje'):
        from estado_ente import Vivo 

        nombre_bicho = getattr(bicho, 'nombre', 'Perezoso')
        nombre_personaje = getattr(personaje_objetivo, 'nombre', 'el objetivo')

        if personaje_objetivo and hasattr(personaje_objetivo, 'recibir_daño') and \
           hasattr(personaje_objetivo, 'estadoEnte') and isinstance(personaje_objetivo.estadoEnte, Vivo):
            print(f"El {nombre_bicho} ataca a {nombre_personaje} con desgana.")
            if hasattr(bicho, 'poder'):
                personaje_objetivo.recibir_daño(bicho.poder)
            else:
                print(f"WARN: {nombre_bicho} no tiene atributo 'poder'.")
        else:
            print(f"El {nombre_bicho} ni se molesta en atacar (objetivo no válido o no vivo).")

    def __str__(self):
        return "perezoso"