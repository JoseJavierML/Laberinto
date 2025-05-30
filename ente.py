from typing import Optional, TYPE_CHECKING
from hoja import Hoja 
from inventario import Inventario
from estado_ente import EstadoEnte, Vivo, Muerto 

if TYPE_CHECKING:
    from juego import Juego 
    from habitacion import Habitacion 

class Ente:
    def __init__(self):
        self.nombre: str = "Ente Anónimo"
        self.vidas: Optional[int] = None
        self.vidas_maximas: Optional[int] = None 
        self.poder: Optional[int] = None
        self.posicion: Optional['Habitacion'] = None 
        self.juego: Optional['Juego'] = None         
        self.estadoEnte: Optional[EstadoEnte] = None 

    def estaVivo(self) -> bool:
        if self.vidas is None or self.estadoEnte is None:
            return False 
        return self.vidas > 0 and isinstance(self.estadoEnte, Vivo)

    def morir(self):
        if self.estadoEnte and isinstance(self.estadoEnte, Vivo): 
            print(f"¡{self.nombre} ha sido derrotado!")
            self.estadoEnte.morir(self) 
            if isinstance(self.estadoEnte, Muerto) and hasattr(self, 'juego') and self.juego:
                if not self.juego.esta_terminado(): 
                    self.juego.perder_juego()
        elif isinstance(self.estadoEnte, Muerto):
            # print(f"{self.nombre} ya estaba derrotado.")
            pass
        else:
            print(f"WARN: {self.nombre} intentó morir pero su estado es desconocido o ya no es Vivo.")


class Personaje(Ente):
    def __init__(self, nombre: str, vidas: int, poder: int, juego: 'Juego', capacidad_inventario: int = 5):
        super().__init__()
        self.nombre = nombre
        self.vidas_maximas = vidas  
        self.vidas = vidas         
        self.poder = poder
        self.juego = juego          
        self.inventario = Inventario(capacidad_inventario)
        self.estadoEnte = Vivo()    

    def __str__(self) -> str:
        salud_actual_str = f"{self.vidas}"
        if self.vidas_maximas is not None:
            salud_actual_str += f"/{self.vidas_maximas}"
        
        estado_str = ""
        if self.estadoEnte and hasattr(self.estadoEnte, '__class__'): 
            estado_str = f"(Estado: {self.estadoEnte.__class__.__name__})"

        return (f"--- {self.nombre} {estado_str} ---\n"
                f"  Salud: {salud_actual_str}\n"
                f"  Poder: {self.poder}\n"
                f"  {self.inventario.listar_items()}") 

    def recibir_daño(self, cantidad: int):
        if not self.estaVivo():
            # print(f"{self.nombre} ya está derrotado, no puede recibir más daño.") 
            return

        self.vidas -= cantidad
        
        vidas_mostradas = max(0, self.vidas) 
        
        print(f"¡{self.nombre} recibe {cantidad} puntos de daño! Vidas restantes: {vidas_mostradas}.")
        
        if self.vidas <= 0:
            self.vidas = 0 
            super().morir() 


    def recoger_hoja(self, hoja_a_recoger: Hoja, habitacion_actual: 'Habitacion'):
        if not hasattr(habitacion_actual, 'hijos'):
            print(f"Error: {getattr(habitacion_actual, 'nombre', 'Esta habitación')} no parece contener objetos (sin 'hijos').")
            return False

        item_encontrado_en_hijos = False
        for hijo in habitacion_actual.hijos: 
            if hijo == hoja_a_recoger: 
                item_encontrado_en_hijos = True
                break
        
        if item_encontrado_en_hijos: 
            if self.inventario.agregar_item(hoja_a_recoger):
                if hasattr(habitacion_actual, 'eliminar_hijo'):
                    habitacion_actual.eliminar_hijo(hoja_a_recoger) 
                    print(f"{self.nombre} recogió: {hoja_a_recoger.nombre}.")
                    return True
                else:
                    self.inventario.quitar_item_por_nombre(hoja_a_recoger.nombre)
                    print(f"Error interno: No se pudo quitar {hoja_a_recoger.nombre} de la habitación.")
                    return False
            else:
                return False
        else:
            print(f"'{hoja_a_recoger.nombre}' no se encuentra en {getattr(habitacion_actual, 'nombre', 'esta habitación')}.")
            return False

    def mostrar_inventario(self):
        print(self.inventario.listar_items())