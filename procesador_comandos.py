from typing import TYPE_CHECKING, Optional, Dict
from comando import Comando
from comandos_concretos import ComandoIr,ComandoMostrar, ComandoInventario, ComandoCoger, ComandoUsar, ComandoAbrir, ComandoIntroducirCodigo,ComandoSoltarItem, ComandoAyuda ,ComandoAtacar

if TYPE_CHECKING:
    from juego import Juego

class ProcesadorComandos:
    def __init__(self, juego: 'Juego'):
        self.juego = juego
        self.comandos_disponibles: Dict[str, Comando] = {}
        self._registrar_comandos_iniciales()

    def _registrar_comandos_iniciales(self):
        self.registrar_comando("ir", ComandoIr())
        self.registrar_comando("i", ComandoIr()) 
        self.registrar_comando("norte", ComandoIr(), es_alias_direccion=True, direccion_alias="norte")
        self.registrar_comando("sur", ComandoIr(), es_alias_direccion=True, direccion_alias="sur")
        self.registrar_comando("este", ComandoIr(), es_alias_direccion=True, direccion_alias="este")
        self.registrar_comando("oeste", ComandoIr(), es_alias_direccion=True, direccion_alias="oeste")
        
        self.registrar_comando("inventario", ComandoInventario())
        self.registrar_comando("inv", ComandoInventario()) 

        self.registrar_comando("coger", ComandoCoger())
        self.registrar_comando("tomar", ComandoCoger())
        self.registrar_comando("recoger", ComandoCoger())
        self.registrar_comando("usar", ComandoUsar())

        self.registrar_comando("abrir", ComandoAbrir())
        self.registrar_comando("ab", ComandoAbrir()) 
        
        self.registrar_comando("mostrar", ComandoMostrar())
        self.registrar_comando("estado", ComandoMostrar()) 
        self.registrar_comando("info", ComandoMostrar())   
        self.registrar_comando("ver", ComandoMostrar())    

        self.registrar_comando("introducir_codigo", ComandoIntroducirCodigo())
        self.registrar_comando("codigo", ComandoIntroducirCodigo()) 
        self.registrar_comando("poner_codigo", ComandoIntroducirCodigo()) 

        self.registrar_comando("soltar", ComandoSoltarItem())
        self.registrar_comando("dejar", ComandoSoltarItem()) 

        self.registrar_comando("ayuda", ComandoAyuda())
        self.registrar_comando("help", ComandoAyuda()) 
        self.registrar_comando("?", ComandoAyuda())    

        self.registrar_comando("atacar", ComandoAtacar())
        self.registrar_comando("luchar", ComandoAtacar()) 
        
        print(f"DEBUG: Comandos registrados: {list(self.comandos_disponibles.keys())}") 

    def registrar_comando(self, palabra_clave: str, comando_obj: Comando, es_alias_direccion: bool = False, direccion_alias: str = ""):
        palabra_clave = palabra_clave.lower()
        if es_alias_direccion:
            self.comandos_disponibles[palabra_clave] = comando_obj 
            if not hasattr(comando_obj, '_alias_direccion_original'):
                 comando_obj._alias_direccion_original = {} 
            comando_obj._alias_direccion_original[palabra_clave] = direccion_alias
        else:
            self.comandos_disponibles[palabra_clave.lower()] = comando_obj


    def procesar(self, entrada_str: str) -> Optional[str]:
        partes = entrada_str.strip().lower().split()
        if not partes:
            return "No has introducido ningún comando."

        palabra_clave_cmd = partes[0]
        argumentos = partes[1:]

        comando_obj = self.comandos_disponibles.get(palabra_clave_cmd)

        if comando_obj:
            argumentos_para_comando = argumentos 
            if hasattr(comando_obj, '_alias_direccion_original') and palabra_clave_cmd in comando_obj._alias_direccion_original:
                direccion_fija = comando_obj._alias_direccion_original[palabra_clave_cmd]
                argumentos_para_comando = [direccion_fija] 
            
            try:
                return comando_obj.ejecutar(self.juego, argumentos_para_comando)
            except Exception as e:
                print(f"DEBUG: Error ejecutando el comando '{palabra_clave_cmd}' con args '{argumentos_para_comando}': {e}")
                import traceback
                traceback.print_exc() 
                return f"Hubo un error inesperado al procesar tu comando. ({type(e).__name__})"
        else:
            if palabra_clave_cmd == "ayuda":
                comandos_ayuda = "Comandos disponibles: " + ", ".join(sorted(self.comandos_disponibles.keys()))
                return comandos_ayuda
            return f"Comando desconocido: '{palabra_clave_cmd}'. Escribe 'ayuda' para ver los comandos."
  