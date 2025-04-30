class EstadoEnte:
    def __init__(self):
        pass

    def vivir(self, ente):
        pass

    def morir(self, ente):
        pass


class Vivo(EstadoEnte):
    def __init__(self):
        super().__init__()
        
    def morir(self, ente):
        print("El ente muere")
        ente.estadoEnte = Muerto()

    def vivir(self, ente):
        print("El ente está vivo")

class Muerto(EstadoEnte):
    def __init__(self):
        super().__init__()

    def morir(self, ente):
        print("El ente está muerto")
        ente.juego.terminarJuego()

    def vivir(self, ente):
        print("El ente revive")
        ente.estadoEnte = Vivo()

    