from typing import Optional, Dict, List, TYPE_CHECKING
from ente import Personaje
from habitacion import Habitacion
from inventario import Inventario 
from hoja import Hoja 
from puerta import Puerta, PuertaConLlaveGenerica, PuertaDeSalida
from bicho import Bicho
from procesador_comandos import ProcesadorComandos

if TYPE_CHECKING:
    from laberinto import Laberinto 

class Juego:
    def __init__(self):
        self.personaje: Optional[Personaje] = None
        self.laberinto: Optional['Laberinto'] = None 

        self.bichos: List = [] 
        self.configuracionGlobal: Dict = {}
        
        self._juego_terminado: bool = False
        self.mensaje_final: str = ""
        

        self.procesador_comandos = ProcesadorComandos(self)

        print("JUEGO: Nueva instancia de Juego creada (esperando ser poblada por el Builder).")

    def agregar_personaje(self, personaje_obj: Personaje):
        self.personaje = personaje_obj
        if self.personaje:
            self.personaje.juego = self 
            print(f"JUEGO: Personaje '{self.personaje.nombre}' asignado al juego.")
        else:
            print("JUEGO WARN: Se intentó agregar un personaje None.")


    def agregar_bicho(self, bicho_obj):
        if bicho_obj:
            self.bichos.append(bicho_obj)
            if hasattr(bicho_obj, 'juego'): 
                bicho_obj.juego = self
            print(f"JUEGO: Bicho '{getattr(bicho_obj, 'modo', type(bicho_obj).__name__)}' agregado al juego.")

    def esta_terminado(self) -> bool:
        return self._juego_terminado

    def terminar_juego(self, mensaje: str):
        self.mensaje_final = mensaje
        self._juego_terminado = True

    def ganar_juego(self):
        mensaje_victoria = (
            "\n...y así, el último mecanismo cede, la gran puerta se abre, no hacia un nuevo pasaje, sino hacia la comprensión.\n"
            "Miras hacia atrás, al laberinto de pasillos, pruebas y ecos de tus propios pasos.\n"
            "¿Fue el laberinto una prisión física, o un reflejo de los muros internos que construimos?\n"
            "Cada llave encontrada, cada código descifrado... meros símbolos de una búsqueda más profunda.\n"
            "Quizás, solo quizás, la única salida era entender que nunca estuviste verdaderamente atrapado,\n"
            "sino aprendiendo a ver más allá de las paredes que tú mismo habías aceptado.\n"
            "Ahora, con la mente clara y el espíritu sereno, avanzas. El 'exterior' no es un lugar, sino una nueva perspectiva.\n\n"
            "FIN"
        )
        self.terminar_juego(mensaje_victoria)

    def perder_juego(self):
        self.terminar_juego("La oscuridad te envuelve... Has sido derrotado, pero cada final es un nuevo comienzo para la reflexión.")

    def mostrar_descripcion_habitacion_actual(self):
        if not self.personaje or not self.personaje.posicion:
            print("JUEGO ERROR: No se puede mostrar descripción, personaje sin posición o no existe.")
            return
        
        hab_actual = self.personaje.posicion 
        
        print("-" * 30)

        nombre_hab = getattr(hab_actual, 'nombre', f"Habitación {getattr(hab_actual, 'num', 'Desconocida')}")
        desc_hab = getattr(hab_actual, 'descripcion', "Un lugar misterioso sin descripción aparente.")
        print(f"Estás en: {nombre_hab}")
        print(desc_hab)
        
        items_visibles = [hijo for hijo in getattr(hab_actual, 'hijos', []) if isinstance(hijo, Hoja)]
        if items_visibles:
            print("Ves aquí:")
            for item_obj in items_visibles:
                print(f"  - {item_obj.nombre}")
        else:
            print("No ves ningún objeto de interés inmediato.")


        bichos_en_sala = []
        if hasattr(self, 'bichos') and self.bichos:
            for bicho_en_juego in self.bichos:
                if hasattr(bicho_en_juego, 'estaVivo') and bicho_en_juego.estaVivo() and \
                   hasattr(bicho_en_juego, 'posicion') and bicho_en_juego.posicion == hab_actual:
                    bichos_en_sala.append(bicho_en_juego)
        
        if bichos_en_sala:
            print("Criaturas presentes:")
            for bicho_obj in bichos_en_sala:
                print(f"  - {str(bicho_obj)}") 
        

        posibles_nombres_orientaciones = ["norte", "sur", "este", "oeste"] 
        salidas_encontradas_info = []

        for orient_str in posibles_nombres_orientaciones:
            if hasattr(hab_actual, orient_str): 
                elemento_en_orient = getattr(hab_actual, orient_str)
                if isinstance(elemento_en_orient, (Puerta, PuertaConLlaveGenerica, PuertaDeSalida)):
                    puerta_obj = elemento_en_orient
                    
                    nombre_puerta_especifico = getattr(puerta_obj, 'nombre', 'una puerta')
                    hab_destino_obj = None
                    
                    try: 
                        if hasattr(puerta_obj, 'lado1') and hasattr(puerta_obj, 'lado2'): 
                            if puerta_obj.lado1 == hab_actual: 
                                hab_destino_obj = puerta_obj.lado2
                            elif puerta_obj.lado2 == hab_actual: 
                                hab_destino_obj = puerta_obj.lado1
                    except AttributeError:               
                        print(f"JUEGO WARN: Puerta '{nombre_puerta_especifico}' en {orient_str} parece no tener lados bien definidos.")
                    nombre_destino = "un lugar desconocido"
                    if hab_destino_obj: 
                        nombre_destino = getattr(hab_destino_obj, 'nombre', f"la habitación {getattr(hab_destino_obj, 'num', '?')}")
                    elif isinstance(puerta_obj, PuertaDeSalida):
                        nombre_destino = "la salida del laberinto"  
                    salidas_encontradas_info.append(f"  - {orient_str.capitalize()}: Hacia {nombre_destino} ({nombre_puerta_especifico})")

        if salidas_encontradas_info:
            print("Salidas visibles:")
            for info_salida in salidas_encontradas_info:
                print(info_salida)
        else:
            print("No ves salidas obvias desde aquí.")
        print("-" * 30)