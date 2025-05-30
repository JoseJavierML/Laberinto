from typing import List, Union 
from hoja import Hoja


class Inventario:
    def __init__(self, capacidad: int):
        self.items: List[Hoja] = []
        self.capacidad_maxima: int = capacidad
        print(f"Inventario creado con capacidad para {capacidad} items.")

    def esta_lleno(self) -> bool:
        return len(self.items) >= self.capacidad_maxima

    def agregar_item(self, item: Hoja) -> bool:
        if not self.esta_lleno():
            self.items.append(item)
            print(f"'{item.nombre}' agregado al inventario.")
            return True
        else:
            print(f"Inventario lleno. No se pudo agregar '{item.nombre}'.")
            return False

    def quitar_item_por_nombre(self, nombre_item: str) -> Union['Hoja', None]:
        nombre_item_a_quitar_lower = nombre_item.lower() 
        for i, item_actual in enumerate(self.items):
            if hasattr(item_actual, 'nombre') and item_actual.nombre.lower() == nombre_item_a_quitar_lower: 
                print(f"'{item_actual.nombre}' quitado del inventario.")
                return self.items.pop(i)
        return None

    def buscar_item_por_nombre(self, nombre_item: str) -> Union['Hoja', None]: 
        nombre_item_a_buscar_lower = nombre_item.lower() 
        for item_actual in self.items:
            if hasattr(item_actual, 'nombre') and item_actual.nombre.lower() == nombre_item_a_buscar_lower: 
                return item_actual
        return None
    def listar_items(self) -> str:
        if not self.items:
            return "El inventario está vacío."
        
        nombres_items = [f"{i+1}. {item.nombre}" for i, item in enumerate(self.items)]
        return "Inventario:\n" + "\n".join(nombres_items)

    def __str__(self) -> str:
        return self.listar_items()