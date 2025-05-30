from perezoso import Perezoso 
from agresivo import Agresivo 
from ente import Ente,Personaje
from estado_ente import Vivo 
from typing import List, Optional
from hoja import Hoja

class Bicho(Ente):
    def __init__(self, vidas: int, poder: int, posicion, modo, 
                 nombre: str = "Bicho Anónimo", 
                 drop_items: Optional[List['Hoja']] = None): 
        super().__init__() 
        self.nombre: str = nombre
        self.vidas_maximas: int = vidas 
        self.vidas: int = vidas
        self.poder: int = poder
        self.posicion = posicion 
        self.modo = modo
        self.juego = None 
        

        if not self.estadoEnte: 
            self.estadoEnte = Vivo()

        self.drop_items_objs: List['Hoja'] = drop_items if drop_items is not None else []

        print(f"BICHO CREADO: {self.nombre} (V:{self.vidas}, P:{self.poder}, Modo:{self.modo}) en Hab: {getattr(self.posicion, 'num', '?')}")

    def estaVivo(self) -> bool:
        return self.vidas > 0

    def recibir_daño(self, cantidad: int):
        if not self.estaVivo():
            return

        self.vidas -= cantidad
        vidas_mostradas = max(0, self.vidas)
        print(f"¡El {self.nombre} recibe {cantidad} puntos de daño! Vidas restantes: {vidas_mostradas}.")
        
        if self.vidas <= 0:
            self.morir()

    def morir(self):
        if isinstance(self.estadoEnte, Vivo): 
            print(f"¡El {self.nombre} ha sido derrotado!")
            self.estadoEnte.morir(self) 
            self._soltar_drops()
            self._eliminar_del_juego()

    def _soltar_drops(self):
        if self.posicion and self.drop_items_objs:
            if hasattr(self.posicion, 'agregar_hijo'):
                print(f"El {self.nombre} ha soltado algo:")
                for item_obj in self.drop_items_objs:
                    self.posicion.agregar_hijo(item_obj)
                    print(f"  - {item_obj.nombre} aparece en el suelo.")
            else:
                print(f"BICHO WARN: La habitación {getattr(self.posicion, 'num', '?')} no puede recibir drops (no tiene 'agregar_hijo').")

    def _eliminar_del_juego(self):
        if self.juego and hasattr(self.juego, 'bichos') and self in self.juego.bichos:
            self.juego.bichos.remove(self)
            #print(f"BICHO INFO: {self.nombre} eliminado de la lista de bichos del juego.")
        
    def actua(self): 
        if self.estaVivo() and self.modo and hasattr(self.modo, 'actuar'):
            self.modo.actuar(self)
        elif not self.estaVivo():
            pass 
          

    def intentar_contraataque(self, personaje_objetivo: 'Personaje'):
        if self.estaVivo() and self.modo and hasattr(self.modo, 'atacar'):
            #print(f"DEBUG BICHO: {self.nombre} intentando contraataque...")
            self.modo.atacar(self, personaje_objetivo)
        elif not self.estaVivo():
            pass 
                


    def __str__(self):
        estado_vida = "Vivo" if self.estaVivo() else "Derrotado"
        return f"{self.nombre} [{getattr(self.modo, '__str__', lambda: 'Sin Modo')()}] (Vidas: {self.vidas}/{self.vidas_maximas}, Estado: {estado_vida})"