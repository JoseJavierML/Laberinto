import json
 

class Director:
    def __init__(self):
        self.builder = None        
        self.dict_json = None     
    def obtenerJuego(self):
        if self.builder and hasattr(self.builder, 'obtenerJuego'):
            return self.builder.obtenerJuego()
        print("DIRECTOR ERROR: Builder no disponible o no tiene el método obtenerJuego.")
        return None
    
    def procesar(self, unArchivoJson: str):

        self.leerArchivo(unArchivoJson)
        
        if not self.dict_json:
            print("DIRECTOR ERROR: Fallo al leer o parsear el archivo JSON. No se puede procesar.")
            return None 

        self.iniBuilder() 

        if self.builder is None:
            print("DIRECTOR ERROR: El builder no se pudo inicializar (verifique la clave 'forma' en JSON).")
            return None 
            
        print("DIRECTOR: Iniciando fabricación de componentes del juego...")
        
        self.fabricarLaberintoEItems() 

        self.fabricarPuertasGlobales() 

        self.builder.fabricarJuego() 
        juego_obj_construido = self.builder.obtenerJuego()

        if juego_obj_construido and 'configuracionGlobal' in self.dict_json:
            juego_obj_construido.configuracionGlobal = self.dict_json['configuracionGlobal']
            print("DIRECTOR: Configuracion Global asignada al Juego.")
        if not juego_obj_construido:
            print("DIRECTOR ERROR: El builder no pudo crear/obtener la instancia de Juego.")
            return None

        self.fabricarPersonajePrincipal(juego_obj_construido)

        self.fabricarBichos(juego_obj_construido)

        print("DIRECTOR: Proceso de construcción del juego completado.")
        return juego_obj_construido

    def fabricarJuego(self): 
        pass


    def iniBuilder(self):
        from laberinto_builder import LaberintoBuilder 
        
        if (self.dict_json and 'forma' in self.dict_json and 
                self.dict_json['forma'].lower() == 'cuadrado'): 
            self.builder = LaberintoBuilder()
            print("DIRECTOR: LaberintoBuilder (para forma cuadrada) inicializado.")
        else:
            forma_val = self.dict_json.get('forma', 'NO DEFINIDA') if self.dict_json else 'JSON NO CARGADO'
            print(f"DIRECTOR: Condición para iniBuilder no cumplida (forma: '{forma_val}'). Builder NO inicializado.")
            self.builder = None

    def fabricarLaberintoEItems(self): 
        if not self.builder:
            print("DIRECTOR ERROR: No hay builder para fabricarLaberintoEItems.")
            return

        self.builder.fabricarLaberinto() 
            
        if (self.dict_json and 'laberinto' in self.dict_json and
                isinstance(self.dict_json['laberinto'], dict) and
                'habitaciones' in self.dict_json['laberinto'] and
                isinstance(self.dict_json['laberinto']['habitaciones'], list)):
            
            num_defs_hab = len(self.dict_json['laberinto']['habitaciones'])
            print(f"DIRECTOR: Encontradas {num_defs_hab} definiciones de habitaciones para procesar.")
            for habitacion_data_json in self.dict_json['laberinto']['habitaciones']:
                self._fabricarHabitacionConItems(habitacion_data_json)
        else:
            print("DIRECTOR ERROR: 'laberinto.habitaciones' no se encontró o no es una lista en el JSON.")

    def _fabricarHabitacionConItems(self, habitacion_data_json: dict):
        if not self.builder: return

        num_habitacion = habitacion_data_json.get('num')
        id_habitacion_str = habitacion_data_json.get('id')
        nombre_habitacion = habitacion_data_json.get('nombre', f"Sala N.{num_habitacion}")
        desc_habitacion = habitacion_data_json.get('descripcion', "Un lugar enigmático.")
        forma_habitacion_str = habitacion_data_json.get('forma', "cuadrado") 

        hab_creada_obj = None
        if num_habitacion is not None:
            hab_creada_obj = self.builder.fabricarHabitacion(
                num_habitacion, 
                id_str=id_habitacion_str,
                nombre=nombre_habitacion,
                descripcion=desc_habitacion,
                forma_str=forma_habitacion_str
            )
            
            if hab_creada_obj and 'itemsEnHabitacion' in habitacion_data_json and \
               isinstance(habitacion_data_json['itemsEnHabitacion'], list):
                # print(f"DIRECTOR: Procesando ítems para Habitación {num_habitacion}...")
                for item_json in habitacion_data_json['itemsEnHabitacion']:
                    nombre = item_json.get('nombre')
                    tipo = item_json.get('tipo')
                    props = {k: v for k, v in item_json.items() if k not in ['nombre', 'tipo']}
                    
                    if nombre and tipo:
                        item_obj = self.builder.fabricarHoja(nombre, tipo, **props)
                        if item_obj and hasattr(hab_creada_obj, 'agregar_hijo'):
                            hab_creada_obj.agregar_hijo(item_obj) 
                        elif not item_obj:
                            print(f"DIRECTOR WARN: Builder no pudo fabricar el item '{nombre}' ({tipo}) para hab {num_habitacion}.")
                        else:
                            print(f"DIRECTOR WARN: Habitación {num_habitacion} no tiene método 'agregar_hijo'.")
                    else:
                        print(f"DIRECTOR WARN: Item en JSON para hab {num_habitacion} sin nombre o tipo: {item_json}")
        else:
            print(f"DIRECTOR WARN: Datos de habitación sin 'num', no se procesará: {id_habitacion_str or habitacion_data_json}")

        
    def fabricarPuertasGlobales(self):
        if not self.builder:
            print("DIRECTOR ERROR: No hay builder para fabricarPuertasGlobales.")
            return

        puertas_data_list = None
        if (self.dict_json and 'laberinto' in self.dict_json and 
            isinstance(self.dict_json['laberinto'], dict) and 
            'puertasGlobales' in self.dict_json['laberinto'] and 
            isinstance(self.dict_json['laberinto']['puertasGlobales'], list)):
            puertas_data_list = self.dict_json['laberinto']['puertasGlobales']
        
        if puertas_data_list:
            print(f"DIRECTOR: Encontradas {len(puertas_data_list)} definiciones de puertas globales para procesar.")
            for puerta_def in puertas_data_list:
                if isinstance(puerta_def, list) and len(puerta_def) >= 4:
                    num_lado1, str_o1, num_lado2, str_o2 = puerta_def[0:4]
                    tipo_puerta = puerta_def[4] if len(puerta_def) > 4 else "PuertaNormal"
                    props_puerta = puerta_def[5] if len(puerta_def) > 5 and isinstance(puerta_def[5], dict) else {}
                    
                    # print(f"DIRECTOR: Fabricando Puerta: [{num_lado1}({str_o1}) <-> {num_lado2}({str_o2})] tipo: {tipo_puerta} props: {props_puerta}")
                    self.builder.fabricarPuerta(num_lado1, str_o1, num_lado2, str_o2, 
                                                tipo_puerta_str=tipo_puerta, **props_puerta)
                else:
                    print(f"DIRECTOR ERROR: Dato de puerta global inválido (se esperaba lista de 4-6 elementos): {puerta_def}")
        else:
            print("DIRECTOR INFO: No se encontró 'laberinto.puertasGlobales' o no es una lista en el JSON. No se fabricarán puertas globales.")


    def fabricarPersonajePrincipal(self, juego_obj_para_poblar):
        if not self.builder:
            print("DIRECTOR ERROR: No hay builder para fabricarPersonajePrincipal.")
            return
        if not self.dict_json or 'personajePrincipal' not in self.dict_json:
            print("DIRECTOR ERROR: No se encontró 'personajePrincipal' en JSON.")
            return

        datos_pj = self.dict_json['personajePrincipal']
     
        personaje_obj = self.builder.fabricarPersonaje(datos_pj, juego_obj_para_poblar) 

        if personaje_obj:
            juego_obj_para_poblar.personaje = personaje_obj 
            
            pos_inicial_data = datos_pj.get('posicionInicial', {})
            num_hab_inicial = pos_inicial_data.get('habitacionNum')

            if num_hab_inicial is not None and juego_obj_para_poblar.laberinto:
                hab_inicial_obj = juego_obj_para_poblar.laberinto.obtenerHabitacion(num_hab_inicial)
                if hab_inicial_obj:
                    personaje_obj.posicion = hab_inicial_obj
                    print(f"DIRECTOR: Personaje '{personaje_obj.nombre}' posicionado en Habitación num {hab_inicial_obj.num}.")
                else:
                    print(f"DIRECTOR ERROR: No se encontró habitación inicial num {num_hab_inicial} para el personaje en el laberinto.")
            elif num_hab_inicial is None:
                 print("DIRECTOR WARN: 'habitacionNum' para posición inicial no especificada en JSON para personaje.")
            else: 
                 print("DIRECTOR ERROR: Laberinto no disponible en el juego para posicionar al personaje.")
        else:
            print("DIRECTOR ERROR: Builder no pudo fabricar el personaje.")


    def leerArchivo(self, filename: str): 
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.dict_json = data
            print(f"DIRECTOR: Archivo JSON '{filename}' leído y parseado correctamente.")
            return data
        except FileNotFoundError:
            print(f"DIRECTOR ERROR: Archivo no encontrado: {filename}")
            self.dict_json = None; return None
        except json.JSONDecodeError as e:
            print(f"DIRECTOR ERROR: Formato JSON inválido en el archivo: {filename}. Error: {e}")
            self.dict_json = None; return None
        except Exception as e:
            print(f"DIRECTOR ERROR inesperado al leer el archivo '{filename}': {e}")
            self.dict_json = None; return None

    def fabricarBichos(self, juego_obj_para_poblar):
        if not self.builder: print("DIRECTOR ERROR: No hay builder para fabricarBichos."); return
        if not self.dict_json or 'laberinto' not in self.dict_json or \
           'bichos' not in self.dict_json['laberinto'] or \
           not isinstance(self.dict_json['laberinto']['bichos'], list):
            print("DIRECTOR INFO: No se encontró 'laberinto.bichos' en JSON o no es una lista. No se fabricarán bichos.")
            return

        print(f"DIRECTOR: Encontradas {len(self.dict_json['laberinto']['bichos'])} definiciones de bichos para procesar.")
        for bicho_data in self.dict_json['laberinto']['bichos']:
            modo = bicho_data.get('modo')
            posicion_num = bicho_data.get('posicion') 
            vidas = bicho_data.get('vidas', 10) 
            poder = bicho_data.get('poder', 3)  
            nombre_bicho = bicho_data.get('nombre', f"Bicho {modo if modo else 'Genérico'}") 
            drops_defs = bicho_data.get('drops', []) 
            
            if modo and posicion_num is not None:
                self.builder.fabricarBicho(modo, posicion_num, 
                                           vidas_b=vidas, poder_b=poder, 
                                           nombre_b_json=nombre_bicho, 
                                           drops_json_defs=drops_defs) 
            else:
                print(f"DIRECTOR WARN: Datos de bicho incompletos en JSON: {bicho_data}")
