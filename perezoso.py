import time
from modo import Modo

class Perezoso(Modo):
    def __init__(self):
        super().__init__()

    def dormir(self, bicho):
        print("Perezoso: Durmiendo...")
        time.sleep(3)

    def caminar(self, bicho):
        print("Perezoso: Caminando pasivamente...")

    def atacar(self, bicho):
        print("Perezoso: Atacando un poco...")

    def __str__(self):
        return "perezoso"