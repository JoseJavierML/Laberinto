class EstadoPuerta:
    def __init__(self):
        pass

    def abrir(self, puerta):
        pass

    def cerrar(self, puerta):
        pass

    def entrar(self, puerta, alguien):
        pass
    
class Abierta(EstadoPuerta):
    def __init__(self):
        super().__init__()

    def cerrar(self, puerta):
        print("Cerrando puerta")
        puerta.estadoPuerta = Cerrada()

    def abrir(self, puerta):
        print("Puerta ya abierta")

    def entrar(self, puerta, alguien):
        puerta.puedeEntrar(alguien)


class Cerrada(EstadoPuerta):
    def __init__(self):
        super().__init__()

    def cerrar(self, puerta):
        print("Puerta ya cerrada")

    def abrir(self, puerta):
        print("Abriendo puerta")
        puerta.estadoPuerta = Abierta()

    def entrar(self, puerta, alguien):
        pass