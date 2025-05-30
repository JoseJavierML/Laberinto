import unittest
from elemento_mapa import ElementoMapa  
from puerta import Puerta, PuertaConLlaveGenerica
from llave import Llave 
from arma import Arma  
from hoja import Hoja
from habitacion import Habitacion
from ente import Personaje 
from inventario import Inventario 

class TestPuertaConLlave(unittest.TestCase):

    def setUp(self):
        self.h1 = Habitacion(num=1)
        self.h2 = Habitacion(num=2)
        
        self.personaje = Personaje(nombre="Tester", vidas=10, poder=5, juego=None, capacidad_inventario=3)
        self.personaje.posicion = self.h1 

        self.puerta_con_llave = PuertaConLlaveGenerica(self.h1, self.h2, nombre="Puerta_Norte_Bloqueada")
 
        if not hasattr(self.h1, 'puertas'):
            self.h1.puertas = {} 
        self.h1.puertas['Norte'] = self.puerta_con_llave

        self.llave_comun = Llave(nombre="Llave Común")
        self.item_no_llave = Arma(nombre="Palo", poder_adicional=1)

    def test_01_puerta_inicialmente_bloqueada_y_cerrada(self):
        print("\n--- Test 01: Puerta inicialmente bloqueada y cerrada ---")
        self.assertTrue(self.puerta_con_llave.esta_bloqueada, "La puerta debería estar bloqueada al crearse.")
        self.assertFalse(self.puerta_con_llave.abierta, "La puerta debería estar cerrada al crearse.")
        print(f"Estado inicial: {self.puerta_con_llave}")

    def test_02_abrir_puerta_bloqueada_falla(self):
        print("\n--- Test 02: Abrir puerta bloqueada falla ---")
        self.personaje.posicion = self.h1
        resultado_abrir = self.puerta_con_llave.abrir() 
        self.assertFalse(resultado_abrir, "No debería poderse abrir una puerta bloqueada.")
        self.assertFalse(self.puerta_con_llave.abierta, "La puerta debería seguir cerrada.")
        self.assertTrue(self.puerta_con_llave.esta_bloqueada, "La puerta debería seguir bloqueada.")
        print(f"Estado tras intento de abrir: {self.puerta_con_llave}")

    def test_03_entrar_puerta_bloqueada_falla(self):
        print("\n--- Test 03: Entrar puerta bloqueada falla ---")
        self.personaje.posicion = self.h1
        resultado_entrar = self.puerta_con_llave.entrar(self.personaje)
        self.assertFalse(resultado_entrar, "No debería poderse entrar por una puerta bloqueada.")
        self.assertEqual(self.personaje.posicion, self.h1, "El personaje no debería haberse movido.")
        print(f"Posición personaje: {self.personaje.posicion.num if self.personaje.posicion else 'None'}")

    def test_04_desbloquear_con_llave(self):
        print("\n--- Test 04: Desbloquear con llave ---")
        self.assertTrue(self.puerta_con_llave.esta_bloqueada, "Puerta debe estar bloqueada inicialmente.")
        

        resultado_desbloqueo = self.puerta_con_llave.desbloquear_con_llave()
        
        self.assertTrue(resultado_desbloqueo, "El desbloqueo debería ser exitoso.")
        self.assertFalse(self.puerta_con_llave.esta_bloqueada, "La puerta debería estar desbloqueada.")
        self.assertFalse(self.puerta_con_llave.abierta, "La puerta debería seguir cerrada después de desbloquear.")
        print(f"Estado tras desbloquear: {self.puerta_con_llave}")

        resultado_desbloqueo_2 = self.puerta_con_llave.desbloquear_con_llave()
        self.assertFalse(resultado_desbloqueo_2, "Desbloquear una puerta ya desbloqueada debería fallar (o devolver False).")
        print(f"Estado tras segundo intento de desbloquear: {self.puerta_con_llave}")

    def test_05_usar_llave_en_puerta_bloqueada(self):
        print("\n--- Test 05: Usar Llave (item) en puerta bloqueada ---")
        self.personaje.inventario.agregar_item(self.llave_comun)
        self.assertTrue(self.puerta_con_llave.esta_bloqueada)

        fue_usada_con_exito = self.llave_comun.usar(self.personaje, puerta_objetivo=self.puerta_con_llave)
        
        self.assertTrue(fue_usada_con_exito, "El método usar() de la llave debería devolver True.")
        self.assertFalse(self.puerta_con_llave.esta_bloqueada, "La puerta debería estar desbloqueada.")
        self.assertFalse(self.puerta_con_llave.abierta, "La puerta permanece cerrada tras el uso de la llave.")

        item_quitado = self.personaje.inventario.quitar_item_por_nombre(self.llave_comun.nombre)
        self.assertEqual(item_quitado, self.llave_comun, "La llave debería poder quitarse del inventario.")
        print(f"Estado puerta tras usar llave: {self.puerta_con_llave}")

    def test_06_usar_llave_en_puerta_ya_desbloqueada(self):
        print("\n--- Test 06: Usar Llave (item) en puerta ya desbloqueada ---")
        self.personaje.inventario.agregar_item(self.llave_comun)
        self.puerta_con_llave.desbloquear_con_llave() 
        self.assertFalse(self.puerta_con_llave.esta_bloqueada)

        fue_usada_con_exito = self.llave_comun.usar(self.personaje, puerta_objetivo=self.puerta_con_llave)
        
        self.assertFalse(fue_usada_con_exito, "El método usar() de la llave debería devolver False si la puerta ya está desbloqueada.")
        self.assertIn(self.llave_comun, self.personaje.inventario.items, "La llave no debería haberse consumido.")
        print(f"Estado puerta: {self.puerta_con_llave}")

    def test_07_usar_item_no_llave_en_puerta(self):
        print("\n--- Test 07: Usar item que no es Llave en puerta ---")
        self.personaje.inventario.agregar_item(self.item_no_llave) 
        self.assertTrue(self.puerta_con_llave.esta_bloqueada)

        fue_usada_con_exito = self.item_no_llave.usar(self.personaje, puerta_objetivo=self.puerta_con_llave)

        self.assertFalse(fue_usada_con_exito, "Usar un item no llave no debería afectar la puerta de esta manera.")
        self.assertTrue(self.puerta_con_llave.esta_bloqueada, "La puerta debería seguir bloqueada.")
        print(f"Estado puerta: {self.puerta_con_llave}")

    def test_08_abrir_y_entrar_puerta_desbloqueada(self):
        print("\n--- Test 08: Abrir y entrar puerta desbloqueada ---")
        self.personaje.posicion = self.h1
        self.puerta_con_llave.desbloquear_con_llave() 
        self.assertFalse(self.puerta_con_llave.esta_bloqueada, "Puerta está desbloqueada.")
        self.assertFalse(self.puerta_con_llave.abierta, "Puerta está cerrada.")

        resultado_entrar_cerrada = self.puerta_con_llave.entrar(self.personaje)
        self.assertFalse(resultado_entrar_cerrada, "No se puede entrar por puerta desbloqueada pero cerrada.")
        self.assertEqual(self.personaje.posicion, self.h1)
        print(f"Posición personaje (antes de abrir): {self.personaje.posicion.num}")

        self.puerta_con_llave.abrir()
        self.assertTrue(self.puerta_con_llave.abierta, "La puerta debería estar abierta.")
        print(f"Estado puerta tras abrir: {self.puerta_con_llave}")

        resultado_entrar_abierta = self.puerta_con_llave.entrar(self.personaje)
        self.assertTrue(resultado_entrar_abierta, "Se debería poder entrar por puerta desbloqueada y abierta.")

        self.assertEqual(self.personaje.posicion, self.h2, "El personaje debería estar en h2.")
        print(f"Posición personaje (después de entrar): {self.personaje.posicion.num}")

    def test_09_llave_usar_en_objeto_no_puerta(self):
        print("\n--- Test 09: Usar Llave en objeto que no es PuertaConLlaveGenerica ---")
        self.personaje.inventario.agregar_item(self.llave_comun)
        objeto_no_puerta = ElementoMapa() 
        
        fue_usada_con_exito = self.llave_comun.usar(self.personaje, puerta_objetivo=objeto_no_puerta)
        self.assertFalse(fue_usada_con_exito, "Usar llave en algo que no es PuertaConLlaveGenerica debería fallar.")
        self.assertIn(self.llave_comun, self.personaje.inventario.items, "La llave no debería consumirse.")

if __name__ == '__main__':
    unittest.main(verbosity=2) 