from bicho import Bicho
from agresivo import Agresivo
from perezoso import Perezoso
from ente import Personaje
from puerta import Puerta
from pared import Pared
from bomba import Bomba
from pared_bomba import ParedBomba
from habitacion import Habitacion
from laberinto import Laberinto
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from orientacion import Orientacion

import threading

class Juego:
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
        self.personaje = None
        self.bicho_threads = {}

    def agregar_personaje(self, nombre):
        self.personaje = Personaje(10, 1, None, self, nombre)
        self.laberinto.entrar(self.personaje)

    def agregar_bicho(self, bicho):
        bicho.juego = self
        self.bichos.append(bicho)

    def lanzarBicho(self, bicho):
        thread = threading.Thread(target=bicho.actua)
        if bicho not in self.bicho_threads:
            self.bicho_threads[bicho] = []
        self.bicho_threads[bicho].append(thread)
        thread.start()

    def terminarBicho(self, bicho):
        if bicho in self.bicho_threads:
            for thread in self.bicho_threads[bicho]:
                bicho.vidas = 0

    def abrir_puertas(self):
        def abrirPuertas(obj):
            if obj.esPuerta():
                obj.abrir()
        self.laberinto.recorrer(abrirPuertas)

    def cerrar_puertas(self):
        def cerrarPuertas(obj):
            if obj.esPuerta():
                obj.cerrar()
        self.laberinto.recorrer(cerrarPuertas)

    def iniciar_juego(self):
        pass  

    def obtenerHabitacion(self, num):
        return self.laberinto.obtenerHabitacion(num)

    def crearLaberinto2HabFM(self, creator):
        laberinto = creator.crear_laberinto()
        habitacion1 = creator.crear_habitacion(1)
        habitacion2 = creator.crear_habitacion(2)
        puerta = creator.crear_puerta(habitacion1, habitacion2)
        
        habitacion1.ponerElementoEnOrientacion(puerta, Norte())
        habitacion2.ponerElementoEnOrientacion(puerta, Sur())
        
        laberinto.agregar_habitacion(habitacion1)
        laberinto.agregar_habitacion(habitacion2)
        return laberinto

    def crearLaberinto2HabBomba(self, creator):
        laberinto = creator.crear_laberinto()
        habitacion1 = creator.crear_habitacion(1)
        habitacion2 = creator.crear_habitacion(2)
        puerta = creator.crear_puerta(habitacion1, habitacion2)

        habitacion1.ponerElementoEnOrientacion(puerta, Norte())
        habitacion2.ponerElementoEnOrientacion(puerta, Sur())

        bomba1 = creator.crear_bomba(creator.crear_pared())
        bomba2 = creator.crear_bomba(creator.crear_pared())
        habitacion1.ponerElementoEnOrientacion(bomba1, Este())
        habitacion2.ponerElementoEnOrientacion(bomba2, Oeste())

        laberinto.agregar_habitacion(habitacion1)
        laberinto.agregar_habitacion(habitacion2)
        return laberinto

    def crearLaberinto4Hab(self, creator):
        laberinto = creator.crear_laberinto()
        habs = [creator.crear_habitacion(i) for i in range(1, 5)]
        puertas = [
            creator.crear_puerta(habs[0], habs[1]),
            creator.crear_puerta(habs[0], habs[2]),
            creator.crear_puerta(habs[1], habs[3]),
            creator.crear_puerta(habs[2], habs[3])
        ]

        orientaciones = [Sur(), Este(), Oeste(), Sur(), Norte(), Este(), Norte(), Oeste()]
        habitaciones_orientaciones = [
            (habs[0], puertas[0]), (habs[0], puertas[1]),
            (habs[2], puertas[1]), (habs[2], puertas[3]),
            (habs[1], puertas[0]), (habs[1], puertas[2]),
            (habs[3], puertas[3]), (habs[3], puertas[2])
        ]
        
        for (hab, puerta), orientacion in zip(habitaciones_orientaciones, orientaciones):
            hab.ponerElementoEnOrientacion(puerta, orientacion)

        bichos = [
            creator.crear_bicho(5, 10, habs[0], creator.crear_modo_agresivo()),
            creator.crear_bicho(5, 1, habs[1], creator.crear_modo_perezoso()),
            creator.crear_bicho(5, 10, habs[2], creator.crear_modo_agresivo()),
            creator.crear_bicho(5, 1, habs[3], creator.crear_modo_perezoso())
        ]
        
        for bicho, hab in zip(bichos, habs):
            self.agregar_bicho(bicho)
            hab.bicho = bicho

        for hab in habs:
            laberinto.agregar_habitacion(hab)
        
        return laberinto