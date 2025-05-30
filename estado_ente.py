from typing import TYPE_CHECKING 
if TYPE_CHECKING:
    from ente import Ente 

class EstadoEnte:
    def __init__(self):
        pass

    def vivir(self, ente: 'Ente'): 
        pass

    def morir(self, ente: 'Ente'):
        pass

class Vivo(EstadoEnte):
    def __init__(self):
        super().__init__()
        
    def morir(self, ente: 'Ente'): 
        nombre_ente = getattr(ente, 'nombre', 'El ente') 
        print(f"{nombre_ente} muere.")
        ente.estadoEnte = Muerto() 

    def vivir(self, ente: 'Ente'):
        nombre_ente = getattr(ente, 'nombre', 'El ente')
        print(f"{nombre_ente} está vivo.")

class Muerto(EstadoEnte):
    def __init__(self):
        super().__init__()

    def morir(self, ente: 'Ente'): 
        from ente import Personaje 

        nombre_ente = getattr(ente, 'nombre', 'El ente')
        
        if hasattr(ente, 'juego') and ente.juego:
            if isinstance(ente, Personaje): 
                print(f"{nombre_ente} (el personaje principal) está completamente derrotado.")
                ente.juego.perder_juego() 
            else: 
                print(f"{nombre_ente} ya estaba/ha sido derrotado (no es el jugador).")
        else:
            print(f"{nombre_ente} está muerto, pero no se pudo finalizar el juego (sin referencia a 'juego').")


    def vivir(self, ente: 'Ente'):
        from ente import Personaje 

        nombre_ente = getattr(ente, 'nombre', 'El ente')
        print(f"{nombre_ente} revive milagrosamente.") 
        ente.estadoEnte = Vivo()