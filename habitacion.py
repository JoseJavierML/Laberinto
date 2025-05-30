from contenedor import Contenedor

class Habitacion(Contenedor):
    def __init__(self, num, nombre="", descripcion=""): 
        super().__init__()
        self.num = num
        self.nombre = nombre 
        self.descripcion = descripcion 
        self.items_en_habitacion = [] 
    def entrar(self, alguien):
        print(f"Entrando en la habitación {self.num}")
        alguien.posicion=self

    def __str__(self):
        return f"Habitación {self.num} ({getattr(self, 'nombre', 'Sin Nombre')})"