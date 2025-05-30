from laberinto import Laberinto
from habitacion import Habitacion
from pared import Pared
from pared_bomba import ParedBomba
from puerta import Puerta
from bicho import Bicho
from bomba import Bomba
from agresivo import Agresivo
from perezoso import Perezoso
from este import Este
from oeste import Oeste
from norte import Norte
from sur import Sur
from orientacion import Orientacion

class Creator:
    def crear_habitacion(self, num):
        habitacion = Habitacion(num)
        habitacion.orientaciones.append(self.crear_norte())  
        habitacion.orientaciones.append(self.crear_sur())
        habitacion.orientaciones.append(self.crear_oeste())
        habitacion.orientaciones.append(self.crear_este())

        pared_norte = self.crear_pared
        habitacion.ponerElementoEnOrientacion(pared_norte)
        pared_oeste = self.crear_pared
        habitacion.ponerElementoEnOrientacion(pared_oeste)
        pared_este = self.crear_pared
        habitacion.ponerElementoEnOrientacion(pared_este)
        pared_sur = self.crear_pared
        habitacion.ponerElementoEnOrientacion(pared_sur)

        return habitacion
    
    def crear_laberinto(self):
        return Laberinto()

    def crear_pared(self):
        return Pared()

    def crear_puerta(self, lado1, lado2):
        return Puerta(lado1, lado2)

    def crear_bomba(self, em):
        return Bomba(em)

    def crear_bicho(self, vidas, poder, posicion, modo):
        return Bicho(vidas, poder, posicion, modo)

    def crear_modo_agresivo(self):
        return Agresivo()

    def crear_modo_perezoso(self):
        return Perezoso()
    
    def crear_norte(self):
        return Norte()
    def crear_oeste(self):
        return Oeste()
    def crear_sur(self):
        return Sur()
    def crear_este(self):
        return Este()
class CreatorB(Creator):
    def crear_pared(self):
        return ParedBomba()