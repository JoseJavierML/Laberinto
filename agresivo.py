import time
from modo import Modo

class Agresivo(Modo):
    def __init__(self):
        super().__init__()

    def dormir(self, bicho):
        print("Agresivo: Durmiendo...")
        time.sleep(1)

    def caminar(self, bicho):
        print("Agresivo: Caminando de manera imponente...")

    def atacar(self, bicho):
        print("Agresivo: Atacando al jugador")

    def __str__(self):
        return "agresivo"