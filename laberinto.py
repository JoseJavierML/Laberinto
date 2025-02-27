class ElementoMapa:
    def __init__(self):
        pass
    def entrar(self):
        pass

class Laberinto(ElementoMapa):
    def __init__(self):
        super().__init__()
        self.habitaciones = []
    
    def entrar(self):
        print("Entrando en el laberinto")
    
    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)
    
    def obtenerHabitacion(self, num):
        for habitacion in self.habitaciones:
            if habitacion.num == num:
                return habitacion
        return None


class Pared(ElementoMapa):
    def __init__(self):
        super().__init__()
    def entrar(self):
        print("Entrando en una pared")

class Habitacion(ElementoMapa):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
        self.paredes = []
        self.puertas = []

    def entrar(self):
        print(f"Entrando en la habitacion {self.num}")
    def agregar_pared(self, pared):
        self.paredes.append(pared)
    def agregar_puerta(self, puerta):
        self.puertas.append(puerta)

class Decorator(ElementoMapa):
    def __init__(self, em):
        super().__init__()
        self.em = em

class Bomba(Decorator):
    def __init__(self, em):
        super().__init__(em)
        self.activa = False
    def esBomba(self):
        return True
class Modo:
    def __init__(self):
        super().__init__()

class Perezoso(Modo):
    def __init__(self):
        super().__init__()

class Agresivo(Modo):
    def __init__(self):
            super().__init__()

class Bicho:
    def __init__(self,vidas,poder,posicion,modo):
        self.vidas = vidas
        self.poder = poder
        self.posicion = posicion
        self.modo = modo                        
class Juego:
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
    
    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)
    
    def iniciar_juego(self):
        pass
    
    def crearLaberinto2HabFM(self, creator):
        laberinto = creator.crear_laberinto()
        habitacion1 = creator.crear_habitacion(1)
        habitacion2 = creator.crear_habitacion(2)
        puerta = creator.crear_puerta(habitacion1, habitacion2)
        habitacion1.sur = puerta
        habitacion2.norte = puerta
        laberinto.agregar_habitacion(habitacion1)
        laberinto.agregar_habitacion(habitacion2)
        return laberinto
    
    def crearLaberinto4Hab(self, creator):
        laberinto = creator.crear_laberinto()

        habitacion1 = creator.crear_habitacion(1)
        habitacion2 = creator.crear_habitacion(2)
        habitacion3 = creator.crear_habitacion(3)
        habitacion4 = creator.crear_habitacion(4)

        puerta12 = creator.crear_puerta(habitacion1, habitacion2)
        puerta13 = creator.crear_puerta(habitacion1, habitacion3)
        puerta24 = creator.crear_puerta(habitacion2, habitacion4)
        puerta34 = creator.crear_puerta(habitacion3, habitacion4)

        habitacion1.sur = puerta12
        habitacion1.este = puerta13
        habitacion2.norte = puerta12
        habitacion2.este = puerta24
        habitacion3.oeste = puerta13
        habitacion3.sur = puerta34
        habitacion4.norte = puerta34
        habitacion4.oeste = puerta24

        bicho1 = creator.crear_bicho(5, 10, habitacion1, creator.crear_modo_agresivo())
        self.agregar_bicho(bicho1)
        bicho2 = creator.crear_bicho(5, 1, habitacion2, creator.crear_modo_perezoso())
        self.agregar_bicho(bicho2)
        bicho3 = creator.crear_bicho(5, 10, habitacion3, creator.crear_modo_agresivo())
        self.agregar_bicho(bicho3)
        bicho4 = creator.crear_bicho(5, 1, habitacion4, creator.crear_modo_perezoso())
        self.agregar_bicho(bicho4)

        habitacion1.bicho = bicho1
        habitacion2.bicho = bicho2
        habitacion3.bicho = bicho3
        habitacion4.bicho = bicho4

        laberinto.agregar_habitacion(habitacion1)
        laberinto.agregar_habitacion(habitacion2)
        laberinto.agregar_habitacion(habitacion3)
        laberinto.agregar_habitacion(habitacion4)

        return laberinto
