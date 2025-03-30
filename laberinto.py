from contenedor import Contenedor

class Laberinto(Contenedor):
    def __init__(self):
        super().__init__()
    
    def entrar(self):
        print("Entrando en el laberinto")
        hab1=self.obtenerHabitacion(1)
        hab1.entrar(alguien)

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)
    
    def obtenerHabitacion(self, num):
        for habitacion in self.habitaciones:
            if habitacion.num == num:
                return habitacion
        return None

    def __str__(self):
        return super().__str__()
    