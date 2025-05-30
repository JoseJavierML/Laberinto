from contenedor import Contenedor 
from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from habitacion import Habitacion 
    from ente import Ente         
class Laberinto(Contenedor):
    def __init__(self, descripcion: str = "Un laberinto misterioso y sin nombre"):
        super().__init__()
        self.nombre: str = "Laberinto Principal" 
        self.descripcion: str = descripcion
        self.habitaciones: List['Habitacion'] = [] 
        self.mapa_habitaciones_num: Dict[int, 'Habitacion'] = {} 
        self.mapa_habitaciones_id: Dict[str, 'Habitacion'] = {}  
        # print(f"LABERINTO: Instancia de Laberinto creada. Descripción: '{self.descripcion}'")

    def entrar(self, alguien: 'Ente', num_habitacion_inicial: int = 1):
        # print(f"LABERINTO: {getattr(alguien, 'nombre', 'Un ente')} intenta entrar al laberinto en la habitación {num_habitacion_inicial}.")
    
        if not self.habitaciones:
            print("LABERINTO WARN: No hay habitaciones en este laberinto para entrar.")
            return

        hab_inicial = self.obtenerHabitacion(num_habitacion_inicial)
        if hab_inicial:
            hab_inicial.entrar(alguien) 
        else:
            print(f"LABERINTO WARN: No se encontró la habitación inicial con num/id '{num_habitacion_inicial}' para entrar.")

    def agregar_habitacion(self, habitacion: 'Habitacion'):
        if habitacion not in self.habitaciones:
            self.habitaciones.append(habitacion)
            
            num_hab = getattr(habitacion, 'num', None)
            id_str_hab = getattr(habitacion, 'id_str', None)

            if num_hab is not None:
                self.mapa_habitaciones_num[num_hab] = habitacion
            if id_str_hab is not None:
                self.mapa_habitaciones_id[id_str_hab] = habitacion

    def obtenerHabitacion(self, num_o_id) -> Optional['Habitacion']:
        hab_encontrada = None
        if isinstance(num_o_id, int):
            hab_encontrada = self.mapa_habitaciones_num.get(num_o_id)
        
        if not hab_encontrada and isinstance(num_o_id, str): 
            hab_encontrada = self.mapa_habitaciones_id.get(num_o_id)
        
        if hab_encontrada:
            return hab_encontrada

        # print(f"LABERINTO DEBUG: No se encontró la habitación con num/id: {num_o_id} en mapas. Buscando por iteración...")
        for habitacion_iter in self.habitaciones:
            if hasattr(habitacion_iter, 'num') and habitacion_iter.num == num_o_id:
                return habitacion_iter
            if hasattr(habitacion_iter, 'id_str') and habitacion_iter.id_str == str(num_o_id):
                return habitacion_iter
                
        print(f"LABERINTO WARN: No se encontró la habitación con num/id: {num_o_id} tras búsqueda exhaustiva.")
        return None

    def __str__(self) -> str:
        return f"{self.descripcion} (Actualmente con {len(self.habitaciones)} habitaciones mapeadas)"

    def recorrer(self, func):
        func(self) 
        # print(f"DEBUG Laberinto.recorrer: Iterando sobre {len(self.habitaciones)} habitaciones...")
        for habitacion_obj in self.habitaciones:
            func(habitacion_obj) 