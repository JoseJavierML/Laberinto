from comando import Comando
from typing import TYPE_CHECKING, Optional, List
from hoja import Hoja
from puerta import Puerta, PuertaConLlaveGenerica, PuertaDeSalida 
from bicho import Bicho 
from estado_ente import Vivo 

try:
    from agresivo import Agresivo 
except ImportError:
    Agresivo = None
    print("ADVERTENCIA (comandos_concretos): No se pudo importar 'Agresivo' desde 'agresivo.py' para ComandoIr.")
try:
    from llave import Llave
except ImportError:
    Llave = None 
    print("ADVERTENCIA (comandos_concretos): No se pudo importar 'Llave' desde 'llave.py'")
try:
    from pocion import PocionCuracion
except ImportError:
    PocionCuracion = None
    print("ADVERTENCIA (comandos_concretos): No se pudo importar 'PocionCuracion' desde 'pocion.py'")
try:
    from fragmento_codigo import FragmentoCodigo
except ImportError:
    FragmentoCodigo = None
    print("ADVERTENCIA (comandos_concretos): No se pudo importar 'FragmentoCodigo' desde 'fragmento_codigo.py'")


if TYPE_CHECKING:
    from juego import Juego 

class ComandoIr(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."

        if not args:
            return "Debes especificar una dirección (ej: 'ir norte')."
        
        direccion = args[0].lower()
        habitacion_actual_antes_de_mover = juego.personaje.posicion 
        puerta_a_usar = None

        if hasattr(habitacion_actual_antes_de_mover, direccion): 
            elemento_en_direccion = getattr(habitacion_actual_antes_de_mover, direccion)
            if isinstance(elemento_en_direccion, (Puerta, PuertaConLlaveGenerica, PuertaDeSalida)):
                puerta_a_usar = elemento_en_direccion
        
        if puerta_a_usar:
            print(f"Intentando ir {direccion} a través de '{getattr(puerta_a_usar, 'nombre', 'una puerta')}'...")
            if puerta_a_usar.entrar(juego.personaje): 
                juego.mostrar_descripcion_habitacion_actual() 
                
                if Agresivo: 
                    habitacion_nueva = juego.personaje.posicion 
                    bichos_agresivos_en_sala = []
                    if hasattr(juego, 'bichos'):
                        for bicho_en_juego in juego.bichos:
                            if bicho_en_juego.estaVivo() and \
                               bicho_en_juego.posicion == habitacion_nueva and \
                               isinstance(bicho_en_juego.modo, Agresivo):
                                bichos_agresivos_en_sala.append(bicho_en_juego)
                    
                    if bichos_agresivos_en_sala:
                        for bicho_agresivo in bichos_agresivos_en_sala:
                            if not isinstance(juego.personaje.estadoEnte, Vivo): break 
                            print(f"¡Un {bicho_agresivo.nombre} te ve y se lanza al ataque!")
                            if hasattr(bicho_agresivo, 'intentar_contraataque'):
                                bicho_agresivo.intentar_contraataque(juego.personaje)
                                if not isinstance(juego.personaje.estadoEnte, Vivo):
                                    return "Has sido emboscado y derrotado al entrar..." 
                return None 
            else:
                return f"No pudiste ir hacia {direccion}." 
        else:
            return f"No hay una puerta en la dirección '{direccion}' desde aquí."

class ComandoInventario(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje:
            return "Error: El personaje no existe."
        if not hasattr(juego.personaje, 'inventario'):
            return "Error: El personaje no tiene inventario."
        return juego.personaje.inventario.listar_items()

class ComandoCoger(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."

        if not args:
            return "Debes especificar qué objeto quieres coger (ej: 'coger palo de madera')."
        
        nombre_objeto_a_coger = " ".join(args).lower()
        habitacion_actual = juego.personaje.posicion
        item_encontrado: Optional[Hoja] = None
        
        if hasattr(habitacion_actual, 'hijos'):
            for posible_item in list(habitacion_actual.hijos): 
                if isinstance(posible_item, Hoja) and hasattr(posible_item, 'nombre'):
                    if posible_item.nombre.lower() == nombre_objeto_a_coger:
                        item_encontrado = posible_item
                        break 
        
        if item_encontrado:
            if juego.personaje.inventario.agregar_item(item_encontrado):
                if hasattr(habitacion_actual, 'eliminar_hijo'):
                    habitacion_actual.eliminar_hijo(item_encontrado)
                    return f"Has recogido: {item_encontrado.nombre}."
                else:
                    juego.personaje.inventario.quitar_item_por_nombre(item_encontrado.nombre) 
                    return f"Error interno: No se pudo quitar {item_encontrado.nombre} de la habitación."
            else:
                return f"No puedes coger {item_encontrado.nombre} (quizás el inventario está lleno)."
        else:
            return f"No ves ningún objeto llamado '{nombre_objeto_a_coger}' aquí."
        
class ComandoUsar(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."

        if not args:
            return "Debes especificar qué objeto quieres usar (ej: 'usar pocion' o 'usar llave en norte')."

        nombre_item_args = []
        nombre_objetivo_args = []
        idx_preposicion = -1

        preposiciones_comunes = ["en", "con", "sobre", "a"]
        for prep in preposiciones_comunes:
            if prep in args:
                idx_preposicion = args.index(prep)
                break
        
        if idx_preposicion != -1: 
            nombre_item_args = args[:idx_preposicion]
            nombre_objetivo_args = args[idx_preposicion+1:]
            if not nombre_item_args or not nombre_objetivo_args:
                return "Formato incorrecto. Prueba: 'usar <item> en <objetivo>' o 'usar <item> con <objetivo>'."
        else: 
            nombre_item_args = args 

        nombre_item_str = " ".join(nombre_item_args).lower()
        item_a_usar = juego.personaje.inventario.buscar_item_por_nombre(nombre_item_str)
        
        if not item_a_usar:
            return f"No tienes un objeto llamado '{nombre_item_str}' en tu inventario."

        if not hasattr(item_a_usar, 'usar'):
            return f"El objeto '{nombre_item_str}' no parece ser usable de esta forma."


        if nombre_objetivo_args:
            direccion_objetivo_str = " ".join(nombre_objetivo_args).lower()
            habitacion_actual = juego.personaje.posicion
            puerta_objetivo = None

            if hasattr(habitacion_actual, direccion_objetivo_str):
                elemento_en_direccion = getattr(habitacion_actual, direccion_objetivo_str)
                if isinstance(elemento_en_direccion, (Puerta, PuertaConLlaveGenerica, PuertaDeSalida)):
                    puerta_objetivo = elemento_en_direccion
            
            if not puerta_objetivo:
                return f"No hay una puerta en la dirección '{direccion_objetivo_str}' para usar con '{nombre_item_str}'."

            print(f"Intentando usar '{item_a_usar.nombre}' en '{getattr(puerta_objetivo, 'nombre', direccion_objetivo_str)}'...")
            fue_exitoso = item_a_usar.usar(juego.personaje, puerta_objetivo=puerta_objetivo) 
            
            if fue_exitoso:
                mensaje_accion = f"Has usado '{item_a_usar.nombre}'."

                if Llave and isinstance(item_a_usar, Llave): 
                    juego.personaje.inventario.quitar_item_por_nombre(item_a_usar.nombre)
                    mensaje_accion += f" La '{item_a_usar.nombre}' ha desaparecido."
                    mensaje_accion += f" La '{getattr(puerta_objetivo, 'nombre', 'puerta')}' parece desbloqueada. Prueba a abrirla."
                return mensaje_accion
            else:
                return f"No pudiste usar '{item_a_usar.nombre}' con '{getattr(puerta_objetivo, 'nombre', direccion_objetivo_str)}'."
        

        else:
            print(f"Intentando usar '{item_a_usar.nombre}'...")

            fue_exitoso = item_a_usar.usar(juego.personaje) 
            
            if fue_exitoso:
                mensaje_retorno = f"Has usado '{item_a_usar.nombre}'."
                if PocionCuracion and isinstance(item_a_usar, PocionCuracion):
                    juego.personaje.inventario.quitar_item_por_nombre(item_a_usar.nombre)
                elif FragmentoCodigo and isinstance(item_a_usar, FragmentoCodigo):
                    pass 
                
                return mensaje_retorno
            else:
                if Llave and isinstance(item_a_usar, Llave): 
                    return f"Debes especificar en qué quieres usar la '{item_a_usar.nombre}' (ej: usar {item_a_usar.nombre} en norte)."
                return f"No has podido usar '{item_a_usar.nombre}' ahora o no tuvo efecto."

class ComandoAbrir(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."
        
        if not args:
            return "Debes especificar qué puerta quieres abrir (ej: 'abrir norte')."
            
        direccion = args[0].lower()
        habitacion_actual = juego.personaje.posicion
        puerta_a_abrir = None

        if hasattr(habitacion_actual, direccion):
            elemento_en_direccion = getattr(habitacion_actual, direccion)
            if isinstance(elemento_en_direccion, (Puerta, PuertaConLlaveGenerica, PuertaDeSalida)):
                puerta_a_abrir = elemento_en_direccion
        
        if puerta_a_abrir:
            if puerta_a_abrir.abrir(): 
                return f"Has abierto la '{getattr(puerta_a_abrir, 'nombre', 'puerta')}' en dirección {direccion}."
            else:
                return None 
        else:
            return f"No hay una puerta en la dirección '{direccion}' para abrir."
        
class ComandoMostrar(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje:
            return "Error: No hay un personaje en el juego."

        salud_str = f"Salud de {juego.personaje.nombre}: {juego.personaje.vidas}"
        if hasattr(juego.personaje, 'vidas_maximas') and juego.personaje.vidas_maximas is not None:
            salud_str += f" / {juego.personaje.vidas_maximas}"
        
        print(salud_str)
        print("--- Ubicación Actual ---")
        juego.mostrar_descripcion_habitacion_actual() 
        
        return None
    
class ComandoIntroducirCodigo(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."

        if len(args) < 3 or args[1].lower() != "en": 
            return "Formato incorrecto. Prueba: 'introducir_codigo <codigo> en <direccion_puerta>'."

        codigo_introducido = args[0]
    
        direccion_puerta_str = " ".join(args[2:]).lower() 
                                    

        habitacion_actual = juego.personaje.posicion
        puerta_final_obj = None

        if hasattr(habitacion_actual, direccion_puerta_str):
            elemento_en_direccion = getattr(habitacion_actual, direccion_puerta_str)
            if isinstance(elemento_en_direccion, PuertaDeSalida): 
                puerta_final_obj = elemento_en_direccion
        
        if not puerta_final_obj:
            return f"No hay una puerta que requiera código en la dirección '{direccion_puerta_str}'."

        print(f"Intentando introducir código '{codigo_introducido}' en '{puerta_final_obj.nombre}'...")
        
        if puerta_final_obj.intentar_abrir_con_codigo(codigo_introducido):
            
            juego.ganar_juego()
            return "¡Has abierto la puerta del destino!" 
        else:
            return None 
        
class ComandoSoltarItem(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion:
            return "Error: Personaje no inicializado o sin posición."
        if not hasattr(juego.personaje, 'inventario'):
            return "Error: El personaje no tiene inventario."

        if not args:
            return "Debes especificar qué objeto quieres soltar (ej: 'soltar palo de madera')."
        
        nombre_item_a_soltar = " ".join(args).lower()
        
        item_soltado = juego.personaje.inventario.quitar_item_por_nombre(nombre_item_a_soltar)
        
        if item_soltado:
            habitacion_actual = juego.personaje.posicion
            if hasattr(habitacion_actual, 'agregar_hijo'):
                habitacion_actual.agregar_hijo(item_soltado)
                if hasattr(item_soltado, 'equipada') and item_soltado.equipada:
                    if hasattr(item_soltado, 'usar'):
                         item_soltado.usar(juego.personaje) 
                return f"Has soltado: {item_soltado.nombre}."
            else:
                juego.personaje.inventario.agregar_item(item_soltado) 
                return f"Error: No puedes dejar objetos en este lugar."
        else:
            return f"No tienes un objeto llamado '{nombre_item_a_soltar}' en tu inventario."

class ComandoAyuda(Comando):
    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not hasattr(juego, 'procesador_comandos') or \
           not hasattr(juego.procesador_comandos, 'comandos_disponibles'):
            return "Error: El sistema de ayuda no está disponible."

       
        comandos_agrupados = {}
        
        temp_comandos = {} 
        
        for cmd_key, cmd_obj in juego.procesador_comandos.comandos_disponibles.items():
            obj_id = id(cmd_obj)
            
            if hasattr(cmd_obj, '_alias_direccion_original') and cmd_key in cmd_obj._alias_direccion_original:
                continue

            if obj_id not in temp_comandos:
                temp_comandos[obj_id] = {'principal': cmd_key, 'alias': set()}
            else:
                
                if len(cmd_key) < len(temp_comandos[obj_id]['principal']):
                    temp_comandos[obj_id]['alias'].add(temp_comandos[obj_id]['principal'])
                    temp_comandos[obj_id]['principal'] = cmd_key
                elif cmd_key != temp_comandos[obj_id]['principal']: 
                    temp_comandos[obj_id]['alias'].add(cmd_key)

        ayuda_texto = "Comandos disponibles:\n"
        
        comandos_ordenados = sorted(temp_comandos.values(), key=lambda x: x['principal'])
        
        for grupo in comandos_ordenados:
            ayuda_texto += f"  - {grupo['principal']}"
            if grupo['alias']:
                alias_ordenados = sorted(list(grupo['alias']))
                ayuda_texto += f" (alias: {', '.join(alias_ordenados)})"
            ayuda_texto += "\n"
            
        ayuda_texto += "\nTambién puedes usar direcciones como comandos directos (ej: 'norte', 'sur', 'este', 'oeste').\n"
        ayuda_texto += "Para la mayoría de los comandos: <comando> [argumentos...]\n"
        ayuda_texto += "Ejemplos:\n"
        ayuda_texto += "  ir norte\n"
        ayuda_texto += "  coger palo de madera\n"
        ayuda_texto += "  inventario (o inv)\n"
        ayuda_texto += "  mostrar (o estado, info, ver)\n"
        ayuda_texto += "  usar pocion de salud pequeña\n"
        ayuda_texto += "  usar llave comun en norte\n"
        ayuda_texto += "  atacar <nombre del bicho>\n" 
        ayuda_texto += "  atacar <nombre del bicho> con <nombre del arma>\n" 
        ayuda_texto += "  abrir norte\n"
        ayuda_texto += "  introducir_codigo 123 en norte\n"
        ayuda_texto += "  soltar palo de madera\n"
        ayuda_texto += "  ayuda (o ?)\n"
        ayuda_texto += "  salir (para terminar el juego)\n"
        
        return ayuda_texto.strip()
try:
    from arma import Arma
except ImportError:
    Arma = None
    print("ADVERTENCIA (comandos_concretos): No se pudo importar 'Arma' desde 'arma.py' para ComandoAtacar.")


class ComandoAtacar(Comando):
    def _encontrar_bicho_en_sala(self, juego: 'Juego', nombre_bicho_str: str) -> Optional[Bicho]:
        hab_actual = juego.personaje.posicion
        nombre_bicho_lower = nombre_bicho_str.lower()
        if hasattr(juego, 'bichos'): 
            for bicho_obj in juego.bichos:
                if hasattr(bicho_obj, 'estaVivo') and bicho_obj.estaVivo() and \
                   hasattr(bicho_obj, 'posicion') and bicho_obj.posicion == hab_actual and \
                   hasattr(bicho_obj, 'nombre') and bicho_obj.nombre.lower() == nombre_bicho_lower:
                    return bicho_obj
        return None

    def ejecutar(self, juego: 'Juego', args: List[str]) -> Optional[str]:
        if not juego.personaje or not juego.personaje.posicion or \
           not hasattr(juego.personaje, 'estadoEnte') or not isinstance(juego.personaje.estadoEnte, Vivo): 
            return "No puedes atacar ahora (personaje no disponible, sin posición o no está vivo)."

        if not args:
            return "Debes especificar a qué bicho atacar (ej: 'atacar guardián')."

        nombre_bicho_a_atacar_args = []
        nombre_arma_a_usar_args = []
        usando_arma_especifica = False

        if "con" in args:
            try:
                idx_con = args.index("con")
                nombre_bicho_a_atacar_args = args[:idx_con]
                nombre_arma_a_usar_args = args[idx_con+1:]
                if not nombre_bicho_a_atacar_args or not nombre_arma_a_usar_args:
                    return "Formato incorrecto. Prueba: 'atacar <bicho> con <arma>' o 'atacar <bicho>'."
                usando_arma_especifica = True
            except ValueError: 
                nombre_bicho_a_atacar_args = args 
        else:
            nombre_bicho_a_atacar_args = args

        nombre_bicho_str = " ".join(nombre_bicho_a_atacar_args).lower()
        bicho_objetivo = self._encontrar_bicho_en_sala(juego, nombre_bicho_str)

        if not bicho_objetivo:
            return f"No hay ningún bicho llamado '{nombre_bicho_str}' aquí o ya está derrotado."

        poder_ataque_jugador = juego.personaje.poder 
        arma_especifica_usada_msg = ""

        if usando_arma_especifica:
            if not Arma: 
                return "Error: La funcionalidad de armas no está disponible en este momento."

            nombre_arma_str = " ".join(nombre_arma_a_usar_args).lower()
            arma_obj = juego.personaje.inventario.buscar_item_por_nombre(nombre_arma_str)

            if not arma_obj:
                return f"No tienes un arma llamada '{nombre_arma_str}' en tu inventario."
            if not isinstance(arma_obj, Arma):
                return f"'{getattr(arma_obj, 'nombre', nombre_arma_str)}' no es un arma."
            
            if hasattr(arma_obj, 'usar'):
                print(f"Intentando equipar '{arma_obj.nombre}' para el ataque...")
                arma_obj.usar(juego.personaje) 
                poder_ataque_jugador = juego.personaje.poder 
                arma_especifica_usada_msg = f" (con {arma_obj.nombre})"
            else:
                return f"No se puede equipar/usar el arma '{arma_obj.nombre}' de esta forma."
        
       
        print(f"Atacas al {bicho_objetivo.nombre}{arma_especifica_usada_msg}...")
        bicho_objetivo.recibir_daño(poder_ataque_jugador) 

        if not bicho_objetivo.estaVivo():
            return None 
        
        # print(f"DEBUG: {bicho_objetivo.nombre} sigue vivo, intentando contraataque.")
        if hasattr(bicho_objetivo, 'intentar_contraataque'):
             bicho_objetivo.intentar_contraataque(juego.personaje) 
             
        if juego.esta_terminado():
            return None 
        
        if bicho_objetivo.estaVivo(): 
            return "El combate continúa..."
        else:
            return None 