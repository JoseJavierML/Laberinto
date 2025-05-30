from laberinto import Laberinto
from habitacion import Habitacion
from puerta import Puerta, PuertaConLlaveGenerica, PuertaDeSalida
from pared import Pared
from norte import Norte
from sur import Sur
from este import Este
from oeste import Oeste
from cuadrado import Cuadrado 
# from forma import Forma 
from juego import Juego
from ente import Personaje 
from inventario import Inventario 
from bicho import Bicho
from agresivo import Agresivo 
from perezoso import Perezoso
from tunel import Tunel
from hoja import Hoja   
try: from arma import Arma
except ImportError: Arma = None; print("ADVERTENCIA (LaberintoBuilder): No se pudo importar 'Arma' desde 'arma.py'")
try: from pocion import PocionCuracion
except ImportError: PocionCuracion = None; print("ADVERTENCIA (LaberintoBuilder): No se pudo importar 'PocionCuracion' desde 'pocion.py'")
try: from llave import Llave
except ImportError: Llave = None; print("ADVERTENCIA (LaberintoBuilder): No se pudo importar 'Llave' desde 'llave.py'")
try: from fragmento_codigo import FragmentoCodigo
except ImportError: FragmentoCodigo = None; print("ADVERTENCIA (LaberintoBuilder): No se pudo importar 'FragmentoCodigo' desde 'fragmento_codigo.py'")

from typing import Optional, Dict, Any, List 

class LaberintoBuilder:
    def __init__(self):
        self.laberinto: Optional[Laberinto] = None
        self.juego: Optional[Juego] = None

    def fabricarJuego(self):
        self.juego = Juego()
        if self.laberinto:
            self.juego.laberinto = self.laberinto 
            print("BUILDER: Instancia de Laberinto asignada al Juego.")
        else:
            print("BUILDER WARN: fabricarJuego llamado pero self.laberinto es None. Creando un laberinto vacío para el juego.")
            self.fabricarLaberinto() 
            self.juego.laberinto = self.laberinto

    def fabricarLaberinto(self, descripcion_lab: str = "Un laberinto enigmático"): 
        print(f"BUILDER: Fabricando instancia de Laberinto (Descripción: '{descripcion_lab}').")
        self.laberinto = Laberinto(descripcion=descripcion_lab)

    def fabricarHabitacion(self, num: int, id_str: Optional[str] = None, nombre: str = "", descripcion: str = "", forma_str: str = "cuadrado"):
        # print(f"BUILDER: Fabricando Habitación num: {num}, id: {id_str}, nombre: {nombre}, forma: {forma_str}")
        hab = Habitacion(num, nombre=nombre, descripcion=descripcion) 
        if id_str:
            hab.id_str = id_str 
        
        hab.forma = self.fabricarFormaEspecifica(forma_str) 
        
        if hasattr(hab.forma, 'orientaciones') and hab.forma.orientaciones: 
            for orientacion_obj in hab.forma.orientaciones:
                if hasattr(hab, 'ponerElementoEnOrientacion'):
                    hab.ponerElementoEnOrientacion(self.fabricarPared(), orientacion_obj)
                else:
                    print(f"BUILDER ERROR: Habitación {num} no tiene método 'ponerElementoEnOrientacion'.")
        else:
            print(f"BUILDER WARN: La forma de Habitación {num} no tiene orientaciones definidas para poner paredes por defecto.")
        
        if self.laberinto:
            self.laberinto.agregar_habitacion(hab) 
        else:
            print("BUILDER ERROR: self.laberinto es None, no se puede agregar habitación.")
        return hab
    
    def fabricarNorte(self):
        return Norte()
    
    def fabricarSur(self):
        return Sur()
    
    def fabricarOeste(self):
        return Oeste()
    
    def fabricarEste(self):
        return Este()

    def fabricarPared(self):
        return Pared()

    def fabricarFormaEspecifica(self, forma_str: str):
        forma_str_lower = forma_str.lower().strip()
        forma_obj = None

        if forma_str_lower == "cuadrado":
            print(f"BUILDER: Fabricando forma Cuadrado (especificada como '{forma_str}').")
            forma_obj = Cuadrado()
        else:
            print(f"BUILDER WARN: Forma '{forma_str}' desconocida o no implementada. Usando Cuadrado por defecto.")
            forma_obj = Cuadrado() 
        if forma_obj and hasattr(forma_obj, 'agregarOrientacion'):
            forma_obj.agregarOrientacion(self.fabricarNorte())
            forma_obj.agregarOrientacion(self.fabricarSur())
            forma_obj.agregarOrientacion(self.fabricarEste())
            forma_obj.agregarOrientacion(self.fabricarOeste())
        elif forma_obj:
            print(f"BUILDER ERROR: La forma '{type(forma_obj).__name__}' creada no tiene método 'agregarOrientacion'.")
        else:
            print(f"BUILDER ERROR CRÍTICO: No se pudo crear un objeto forma. Creando Cuadrado vacío.")
            return Cuadrado() 

        return forma_obj

    def fabricarPuerta(self, num_lado1: int, str_o1: str, num_lado2: int, str_o2: str, 
                       tipo_puerta_str: Optional[str] = "PuertaNormal", **kwargs_puerta) -> Optional[Puerta]:
        if not self.laberinto:
            print("BUILDER ERROR: Laberinto no fabricado, no se puede crear puerta.")
            return None

        hab1 = self.laberinto.obtenerHabitacion(num_lado1)
        hab2 = self.laberinto.obtenerHabitacion(num_lado2) 

        if not hab1:
            print(f"BUILDER ERROR: No se encontró habitación {num_lado1} para la puerta (lado1).")
            return None
        if not hab2 and tipo_puerta_str not in ["PuertaDeSalida"]:
            print(f"BUILDER ERROR: No se encontró habitación {num_lado2} (lado2) para una puerta tipo '{tipo_puerta_str}' que requiere dos habitaciones.")
            return None
        elif not hab2 and tipo_puerta_str == "PuertaDeSalida":
            print(f"BUILDER INFO: Habitación destino {num_lado2} (lado2) para PuertaDeSalida no encontrada, asumiendo conexión al exterior.")

        puerta_obj = None
        nombre_puerta_defecto = f"Puerta entre Hab.{num_lado1} y Hab.{num_lado2 if hab2 else 'Exterior'}"
        nombre_puerta_json = kwargs_puerta.get("nombre", nombre_puerta_defecto)

        if tipo_puerta_str == "PuertaConLlaveGenerica":
            puerta_obj = PuertaConLlaveGenerica(hab1, hab2, nombre=nombre_puerta_json)
        elif tipo_puerta_str == "PuertaDeSalida":
            codigo = kwargs_puerta.get("codigo_secreto", "000") 
            puerta_obj = PuertaDeSalida(hab1, hab2, codigo_secreto=codigo, nombre=nombre_puerta_json)
        elif tipo_puerta_str == "PuertaNormal" or tipo_puerta_str is None: 
            if not hab2:
                 print(f"BUILDER ERROR: PuertaNormal entre Hab {num_lado1} y Hab {num_lado2} (no encontrada) no puede tener un lado None.")
                 return None
            puerta_obj = Puerta(hab1, hab2) 
            puerta_obj.nombre = nombre_puerta_json
        else:
            print(f"BUILDER WARN: Tipo de puerta '{tipo_puerta_str}' desconocido. No se creará la puerta.")
            return None
        
        orientacion1_obj = self.obtenerObjeto(str_o1)
        if not orientacion1_obj:
            print(f"BUILDER ERROR: Orientación desconocida '{str_o1}' para puerta en Hab {num_lado1}.")
            return None

        # print(f"BUILDER: Poniendo '{getattr(puerta_obj, 'nombre', 'puerta')}' en Hab {hab1.num} ({str_o1})")
        hab1.ponerElementoEnOrientacion(puerta_obj, orientacion1_obj)

        if hab2: 
            orientacion2_obj = self.obtenerObjeto(str_o2)
            if not orientacion2_obj:
                print(f"BUILDER ERROR: Orientación desconocida '{str_o2}' para puerta en Hab {hab2.num}.")
            else:
                # print(f"BUILDER: Poniendo '{getattr(puerta_obj, 'nombre', 'puerta')}' en Hab {hab2.num} ({str_o2})")
                hab2.ponerElementoEnOrientacion(puerta_obj, orientacion2_obj)
        
        return puerta_obj
    
    def obtenerObjeto(self, cadena_orientacion: str): 
        obj = None
        cadena_lower = cadena_orientacion.lower().strip()
        if cadena_lower == 'norte': obj = self.fabricarNorte()
        elif cadena_lower == 'sur': obj = self.fabricarSur()
        elif cadena_lower == 'este': obj = self.fabricarEste()
        elif cadena_lower == 'oeste': obj = self.fabricarOeste()
        else: print(f"BUILDER WARN: Orientación '{cadena_orientacion}' desconocida en obtenerObjeto.")
        return obj
     
    def fabricarPersonaje(self, datos_personaje_json: Dict, juego_obj_ref: Juego) -> Optional[Personaje]:
        nombre = datos_personaje_json.get('nombre', "Aventurero Anónimo")
        vidas = datos_personaje_json.get('vidas', 20)
        poder = datos_personaje_json.get('poder', 5)
        
        datos_inventario_json = datos_personaje_json.get('inventario', {})
        capacidad_inv = datos_inventario_json.get('capacidad', 5)
        items_iniciales_json = datos_inventario_json.get('itemsIniciales', [])

        personaje_obj = Personaje(nombre=nombre, vidas=vidas, poder=poder, juego=juego_obj_ref, capacidad_inventario=capacidad_inv)
        print(f"BUILDER: Personaje '{nombre}' fabricado (V:{vidas}, P:{poder}, InvCap:{capacidad_inv}).")

        for item_data in items_iniciales_json:
            nombre_item = item_data.get('nombre')
            tipo_item = item_data.get('tipo')
            props_item = {k:v for k,v in item_data.items() if k not in ['nombre', 'tipo']}
            if nombre_item and tipo_item:
                item_creado = self.fabricarHoja(nombre_item, tipo_item, **props_item)
                if item_creado:
                    if personaje_obj.inventario.agregar_item(item_creado):
                        print(f"BUILDER: Item inicial '{nombre_item}' agregado al inventario de {nombre}.")
                    # else: agregar_item ya imprime si está lleno
        return personaje_obj

    def fabricarBichoConcreto(self, vidas: int, poder: int, posicion_obj: Habitacion, 
                              modo_obj, tipo_str: str, nombre_bicho: str, 
                              lista_drop_item_objs: List[Hoja]):
        # print(f"BUILDER: Fabricando Bicho {tipo_str} llamado '{nombre_bicho}' (V:{vidas}, P:{poder}, Pos:{getattr(posicion_obj, 'num', '?')}) con {len(lista_drop_item_objs)} drops.")
        bicho = Bicho(vidas=vidas, poder=poder, posicion=posicion_obj, modo=modo_obj, 
                      nombre=nombre_bicho, drop_items=lista_drop_item_objs)
        return bicho

    def fabricarBicho(self, modo_str: str, posicion_num: int, 
                      vidas_b: int = 10, poder_b: int = 3, 
                      nombre_b_json: Optional[str] = None, 
                      drops_json_defs: Optional[List[Dict]] = None):
        if not self.laberinto: print("BUILDER ERROR: Laberinto no fabricado, no se puede crear bicho."); return None
        if not self.juego: print("BUILDER ERROR: Instancia de Juego no fabricada por el builder, no se puede agregar bicho."); return None

        hab_posicion = self.laberinto.obtenerHabitacion(posicion_num)
        if not hab_posicion: print(f"BUILDER ERROR: No se encontró habitación {posicion_num} para el bicho."); return None

        nombre_bicho_final = nombre_b_json if nombre_b_json else f"Bicho {modo_str} Salvaje"
        
        items_fabricados_para_drop: List[Hoja] = []
        if drops_json_defs:
            # print(f"BUILDER: Fabricando {len(drops_json_defs)} drops para {nombre_bicho_final}...")
            for item_def in drops_json_defs:
                nombre_drop = item_def.get('nombre')
                tipo_drop = item_def.get('tipo')
                props_drop = {k: v for k, v in item_def.items() if k not in ['nombre', 'tipo']}
                if nombre_drop and tipo_drop:
                    item_obj_drop = self.fabricarHoja(nombre_drop, tipo_drop, **props_drop)
                    if item_obj_drop: items_fabricados_para_drop.append(item_obj_drop)
                else: print(f"BUILDER WARN: Definición de drop para '{nombre_bicho_final}' incompleta: {item_def}")

        bicho_obj = None
        modo_lower = modo_str.lower(); modo_concreto_obj = None
        if modo_lower == 'agresivo': modo_concreto_obj = Agresivo()
        elif modo_lower == 'perezoso': modo_concreto_obj = Perezoso()
        
        if modo_concreto_obj:
            bicho_obj = self.fabricarBichoConcreto(vidas_b, poder_b, hab_posicion, 
                                                   modo_concreto_obj, modo_str.capitalize(), 
                                                   nombre_bicho_final, items_fabricados_para_drop)
        else: print(f"BUILDER WARN: Modo de bicho '{modo_str}' desconocido para '{nombre_bicho_final}'."); return None

        if bicho_obj:
            if hasattr(self.juego, 'agregar_bicho'): self.juego.agregar_bicho(bicho_obj)
            else: print("BUILDER WARN: La clase Juego no tiene el método 'agregar_bicho'.")
        return bicho_obj

    def obtenerJuego(self) -> Optional[Juego]:
        return self.juego
    
    def fabricarTunelEn(self, unContenedorPadre):
        tunel = Tunel() 
        if hasattr(unContenedorPadre, 'agregar_hijo'):
            unContenedorPadre.agregar_hijo(tunel)
            print(f"BUILDER: Túnel fabricado y agregado a '{type(unContenedorPadre).__name__}'.")
        else:
            print(f"BUILDER ERROR: El contenedor padre '{type(unContenedorPadre).__name__}' no tiene método 'agregar_hijo'.")
        return tunel

    def fabricarHoja(self, nombre_item: str, tipo_item_str: str, **props_item_dict):
        item_obj = None; tipo_item_lower = tipo_item_str.lower().strip()

        if tipo_item_lower == "arma" and Arma: 
            item_obj = Arma(nombre=nombre_item, poder_adicional=props_item_dict.get("poder_adicional", 1))
        elif tipo_item_lower == "pocioncuracion" and PocionCuracion: 
            item_obj = PocionCuracion(nombre=nombre_item, puntos_vida_recuperados=props_item_dict.get("puntos_vida_recuperados", 0))
        elif tipo_item_lower == "llave" and Llave: 
            item_obj = Llave(nombre=nombre_item)
        elif tipo_item_lower == "fragmentocodigo" and FragmentoCodigo: 
            item_obj = FragmentoCodigo(nombre=nombre_item, pista=props_item_dict.get("pista", "Una pista olvidada."))
        elif tipo_item_lower == "hojagenerica":
            item_obj = Hoja(nombre=nombre_item) 
            if "descripcion" in props_item_dict: setattr(item_obj, 'descripcion', props_item_dict["descripcion"])
        else:
            print(f"BUILDER WARN: Tipo de ítem '{tipo_item_str}' desconocido o su clase no pudo ser importada para '{nombre_item}'. Creando Hoja genérica.")
            item_obj = Hoja(nombre=nombre_item) 

        if item_obj: print(f"BUILDER: Fabricado ítem '{nombre_item}' de tipo '{tipo_item_str}'.")
        return item_obj