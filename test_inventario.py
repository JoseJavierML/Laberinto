import unittest
from inventario import Inventario 
from hoja import Hoja 

class TestInventario(unittest.TestCase):

    def setUp(self):
        self.hoja_espada = Hoja(nombre="Espada Corta")
        self.hoja_escudo = Hoja(nombre="Escudo de Madera")
        self.hoja_pocion = Hoja(nombre="Poción de Vida")
        self.hoja_llave = Hoja(nombre="Llave Vieja")
        self.hoja_gema = Hoja(nombre="Gema Brillante")
        self.hoja_extra = Hoja(nombre="Daga")

    def test_crear_inventario_capacidad_correcta(self):
        inventario_pequeno = Inventario(capacidad=3)
        self.assertEqual(inventario_pequeno.capacidad_maxima, 3)
        self.assertEqual(len(inventario_pequeno.items), 0)

        inventario_grande = Inventario(capacidad=5) 
        self.assertEqual(inventario_grande.capacidad_maxima, 5)

    def test_agregar_item_inventario_no_lleno(self):
        inventario = Inventario(capacidad=2)
        resultado = inventario.agregar_item(self.hoja_espada)
        self.assertTrue(resultado)
        self.assertIn(self.hoja_espada, inventario.items)
        self.assertEqual(len(inventario.items), 1)

    def test_agregar_item_inventario_lleno(self):
        inventario = Inventario(capacidad=1)
        inventario.agregar_item(self.hoja_espada) 
        
        resultado = inventario.agregar_item(self.hoja_escudo) 
        self.assertFalse(resultado)
        self.assertNotIn(self.hoja_escudo, inventario.items) 
        self.assertEqual(len(inventario.items), 1)

    def test_esta_lleno(self):
        inventario = Inventario(capacidad=1)
        self.assertFalse(inventario.esta_lleno())
        inventario.agregar_item(self.hoja_espada)
        self.assertTrue(inventario.esta_lleno())

    def test_quitar_item_existente(self):
        inventario = Inventario(capacidad=3)
        inventario.agregar_item(self.hoja_espada)
        inventario.agregar_item(self.hoja_pocion)
        
        item_quitado = inventario.quitar_item_por_nombre("Espada Corta")
        self.assertEqual(item_quitado, self.hoja_espada)
        self.assertNotIn(self.hoja_espada, inventario.items)
        self.assertEqual(len(inventario.items), 1)
        self.assertIn(self.hoja_pocion, inventario.items) 

    def test_quitar_item_no_existente(self):
        inventario = Inventario(capacidad=3)
        inventario.agregar_item(self.hoja_espada)
        
        item_quitado = inventario.quitar_item_por_nombre("Escudo Mágico")
        self.assertIsNone(item_quitado)
        self.assertEqual(len(inventario.items), 1) 

    def test_buscar_item_existente(self):
        inventario = Inventario(capacidad=3)
        inventario.agregar_item(self.hoja_espada)
        inventario.agregar_item(self.hoja_pocion)

        item_encontrado = inventario.buscar_item_por_nombre("Poción de Vida")
        self.assertEqual(item_encontrado, self.hoja_pocion)
        self.assertEqual(len(inventario.items), 2) 

    def test_buscar_item_no_existente(self):
        inventario = Inventario(capacidad=3)
        inventario.agregar_item(self.hoja_espada)

        item_encontrado = inventario.buscar_item_por_nombre("Poción de Vida")
        self.assertIsNone(item_encontrado)

    def test_listar_items_vacio(self):
        inventario = Inventario(capacidad=3)
        self.assertEqual(inventario.listar_items(), "El inventario está vacío.")

    def test_listar_items_con_contenido(self):
        inventario = Inventario(capacidad=3)
        inventario.agregar_item(self.hoja_espada)
        inventario.agregar_item(self.hoja_pocion)
        
        esperado = "Inventario:\n1. Espada Corta\n2. Poción de Vida"
        self.assertEqual(inventario.listar_items(), esperado)

    def test_str_inventario(self):
        inventario = Inventario(capacidad=2)
        inventario.agregar_item(self.hoja_espada)
        esperado = "Inventario:\n1. Espada Corta"
        self.assertEqual(str(inventario), esperado)

if __name__ == '__main__':
    unittest.main()