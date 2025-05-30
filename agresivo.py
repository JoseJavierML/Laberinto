import time
from modo import Modo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bicho import Bicho
    from ente import Personaje
    from estado_ente import Vivo

class Agresivo(Modo):
    def __init__(self):
        super().__init__()

    def dormir(self, bicho: 'Bicho'):
        nombre_bicho = getattr(bicho, 'nombre', 'Agresivo')
        # print(f"{nombre_bicho}: Durmiendo brevemente...")
        time.sleep(0.5)

    def caminar(self, bicho: 'Bicho'):
        nombre_bicho = getattr(bicho, 'nombre', 'Agresivo')
        # print(f"{nombre_bicho}: Se mueve amenazadoramente...")
        pass

    def atacar(self, bicho: 'Bicho', personaje_objetivo: 'Personaje'):
        from estado_ente import Vivo 

        nombre_bicho = getattr(bicho, 'nombre', 'Agresivo')
        nombre_personaje = getattr(personaje_objetivo, 'nombre', 'el objetivo')

        if personaje_objetivo and hasattr(personaje_objetivo, 'recibir_daño') and \
           hasattr(personaje_objetivo, 'estadoEnte') and isinstance(personaje_objetivo.estadoEnte, Vivo):
            print(f"¡El {nombre_bicho} ataca a {nombre_personaje} con furia!")
            if hasattr(bicho, 'poder'):
                personaje_objetivo.recibir_daño(bicho.poder)
            else:
                print(f"WARN: {nombre_bicho} no tiene atributo 'poder'.")

        else:
            print(f"El {nombre_bicho} intenta atacar, ¡pero no hay un objetivo válido o vivo!")

    def __str__(self):
        return "agresivo"