import unittest
from fragmento_codigo import FragmentoCodigo 
from ente import Personaje 
from inventario import Inventario 


class TestFragmentoCodigo(unittest.TestCase):

    def setUp(self):
        self.personaje_dummy = Personaje(nombre="Lector", vidas=10, poder=5, juego=None, capacidad_inventario=2)
        self.fragmento1 = FragmentoCodigo(nombre="Papiro Antiguo", pista="El primer número es el de los sabios: 7")
        self.fragmento2 = FragmentoCodigo(nombre="Esquirla Grabada", pista="Sigue la cuenta: ...y luego el 4.")

    def test_creacion_fragmento(self):
        print("\n--- Test: Creación de FragmentoCodigo ---")
        self.assertEqual(self.fragmento1.nombre, "Papiro Antiguo")
        self.assertEqual(self.fragmento1.pista, "El primer número es el de los sabios: 7")
        self.assertIn("Contiene una pista", str(self.fragmento1))
        print(f"Creado: {self.fragmento1.nombre}, Pista: '{self.fragmento1.pista}'")

    def test_usar_fragmento_revela_pista(self):
        print("\n--- Test: Usar FragmentoCodigo revela pista ---")
        self.personaje_dummy.inventario.agregar_item(self.fragmento1)
        
        print(f"Personaje '{self.personaje_dummy.nombre}' va a usar '{self.fragmento1.nombre}'...")
        resultado_uso = self.fragmento1.usar(self.personaje_dummy)
        
        self.assertTrue(resultado_uso, "El método usar() de FragmentoCodigo debería devolver True.")
       
        print(f"'{self.fragmento1.nombre}' usado por '{self.personaje_dummy.nombre}'.")
