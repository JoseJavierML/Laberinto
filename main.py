from director import Director
from juego import Juego 
from typing import Optional 

def inicializar_juego_real(ruta_json: str) -> Optional[Juego]:

    print(f"MAIN: Creando instancia de Director...")
    director_juego = Director() 
    
    print(f"MAIN: Director procesando archivo JSON: {ruta_json}")
    
    juego_configurado = director_juego.procesar(ruta_json) 

    if not juego_configurado:
        print("ERROR CRÍTICO MAIN: El Director no pudo construir la instancia de Juego.")
        return None
    
    if not isinstance(juego_configurado, Juego):
        print(f"ERROR CRÍTICO MAIN: El Director no devolvió un objeto Juego válido (obtenido: {type(juego_configurado)}).")
        return None
    
    if not juego_configurado.personaje:
        print("ERROR CRÍTICO MAIN: Personaje no fue creado o asignado por el builder al objeto Juego.")
        return None 
        
    if not juego_configurado.personaje.posicion:
        print("ERROR CRÍTICO MAIN: Personaje no tiene una posición inicial asignada por el builder.")
        return None

    print("MAIN: Juego construido y configurado exitosamente por el sistema Builder-Director.")
    return juego_configurado


def bucle_de_juego_interactivo(juego_actual: Juego):
    if not juego_actual:
        print("MAIN ERROR: Se intentó iniciar el bucle con un juego no válido.")
        return

    print("\n" + juego_actual.configuracionGlobal.get("mensajeBienvenida", "¡Comienza la aventura interactiva!"))
    juego_actual.mostrar_descripcion_habitacion_actual()

    while not juego_actual.esta_terminado():
        entrada = input("> ").strip()
        if not entrada:
            continue 
        
        if entrada.lower() == "salir":
            juego_actual.terminar_juego("Has decidido salir del juego. ¡Hasta pronto!")
           
        else:
            resultado_procesamiento = juego_actual.procesador_comandos.procesar(entrada)
            if resultado_procesamiento: 
                print(resultado_procesamiento)
        
        
        if juego_actual.personaje and hasattr(juego_actual.personaje, 'vidas') and \
           juego_actual.personaje.vidas <= 0 and not juego_actual.esta_terminado():
            juego_actual.perder_juego()

    
    print("\n" + juego_actual.mensaje_final)
    print("Gracias por jugar.")


if __name__ == "__main__":
  
    ruta_json_personalizada = "C:\\Users\\jjmud\\Documentos_Locales\\Universidad\\3º AÑO\\2ºCautri\\Diseño software\\Laberinto Diseño de Software\\juego_inicial.json"
    
    print(f"MAIN: Iniciando el juego con el builder y el archivo: {ruta_json_personalizada}")
    mi_juego_instancia = inicializar_juego_real(ruta_json_personalizada)

    if mi_juego_instancia:
        print("MAIN: Juego inicializado por el builder. Iniciando bucle interactivo.")
        bucle_de_juego_interactivo(mi_juego_instancia)
    else:
        print("MAIN: No se pudo iniciar el juego. Revisa los errores anteriores.")