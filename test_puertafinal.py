import unittest
from puerta import Puerta, PuertaDeSalida 
from habitacion import Habitacion
from ente import Personaje 
from inventario import Inventario 

class TestPuertaDeSalida(unittest.TestCase):

    def setUp(self):
        self.h_inicio = Habitacion(num=10)
        self.h_exterior_victoria = Habitacion(num=99) 
        
        self.codigo_secreto_correcto = "735"
        self.puerta_escape = PuertaDeSalida(self.h_inicio, 
                                            self.h_exterior_victoria, 
                                            codigo_secreto=self.codigo_secreto_correcto,
                                            nombre="Portal del Fin")

        self.personaje = Personaje(nombre="AventureroValiente", vidas=100, poder=20, juego=None, capacidad_inventario=5)
        self.personaje.posicion = self.h_inicio 

        if not hasattr(self.h_inicio, 'puertas'):
            self.h_inicio.puertas = {}
        self.h_inicio.puertas['SalidaEste'] = self.puerta_escape


    def test_01_puerta_salida_inicializacion(self):
        print("\n--- Test 01: Inicialización de PuertaDeSalida ---")
        self.assertFalse(self.puerta_escape.abierta, "La PuertaDeSalida debería estar cerrada al crearse.")
        self.assertEqual(self.puerta_escape.codigo_secreto, self.codigo_secreto_correcto, "El código secreto no se almacenó correctamente.")
        self.assertIn("Requiere código", str(self.puerta_escape), "La descripción debería indicar que requiere código.")
        print(f"Estado inicial: {self.puerta_escape}")

    def test_02_abrir_normal_falla_en_puerta_salida(self):
        print("\n--- Test 02: Intento de 'abrir' normal en PuertaDeSalida ---")
        resultado_abrir = self.puerta_escape.abrir() 
        self.assertFalse(resultado_abrir, "El método abrir() normal no debería abrir la PuertaDeSalida.")
        self.assertFalse(self.puerta_escape.abierta, "La PuertaDeSalida debería permanecer cerrada.")
        print(f"Estado tras intento de abrir normal: {self.puerta_escape}")

    def test_03_intentar_abrir_con_codigo_incorrecto(self):
        print("\n--- Test 03: Intentar abrir con código incorrecto ---")
        codigo_incorrecto = "123"
        resultado_intento = self.puerta_escape.intentar_abrir_con_codigo(codigo_incorrecto)
        self.assertFalse(resultado_intento, "Abrir con código incorrecto debería devolver False.")
        self.assertFalse(self.puerta_escape.abierta, "La puerta debería permanecer cerrada tras un código incorrecto.")
        print(f"Estado tras código incorrecto: {self.puerta_escape}")

    def test_04_intentar_abrir_con_codigo_correcto_puerta_cerrada(self):
        print("\n--- Test 04: Intentar abrir con código correcto (puerta cerrada) ---")
        resultado_intento = self.puerta_escape.intentar_abrir_con_codigo(self.codigo_secreto_correcto)
        self.assertTrue(resultado_intento, "Abrir con código correcto debería devolver True.")
        self.assertTrue(self.puerta_escape.abierta, "La puerta debería estar abierta tras el código correcto.")
        print(f"Estado tras código correcto: {self.puerta_escape}")

    def test_05_intentar_abrir_con_codigo_correcto_puerta_ya_abierta(self):
        print("\n--- Test 05: Intentar abrir con código correcto (puerta ya abierta) ---")

        self.puerta_escape.intentar_abrir_con_codigo(self.codigo_secreto_correcto)
        self.assertTrue(self.puerta_escape.abierta, "PRECONDICIÓN: La puerta debe estar abierta.")

        resultado_segundo_intento = self.puerta_escape.intentar_abrir_con_codigo(self.codigo_secreto_correcto)
    
        self.assertFalse(resultado_segundo_intento, "Intentar abrir una puerta ya abierta con código debería devolver False.")
        self.assertTrue(self.puerta_escape.abierta, "La puerta debería seguir abierta.")
        print(f"Estado tras segundo intento con código correcto (ya abierta): {self.puerta_escape}")

    def test_06_entrar_puerta_salida_cerrada(self):
        print("\n--- Test 06: Entrar por PuertaDeSalida cerrada ---")
        self.personaje.posicion = self.h_inicio
        self.assertFalse(self.puerta_escape.abierta, "PRECONDICIÓN: La puerta debe estar cerrada.")
        
        resultado_entrar = self.puerta_escape.entrar(self.personaje)
        self.assertFalse(resultado_entrar, "No se debería poder entrar por una PuertaDeSalida cerrada.")
        self.assertEqual(self.personaje.posicion, self.h_inicio, "El personaje no debería haberse movido.")
        print(f"Posición personaje: {self.personaje.posicion.num if self.personaje.posicion else 'None'}")

    def test_07_entrar_puerta_salida_abierta_con_codigo(self):
        print("\n--- Test 07: Entrar por PuertaDeSalida abierta con código ---")
        self.personaje.posicion = self.h_inicio
        self.puerta_escape.intentar_abrir_con_codigo(self.codigo_secreto_correcto) 
        self.assertTrue(self.puerta_escape.abierta, "PRECONDICIÓN: La puerta debe estar abierta.")

        resultado_entrar = self.puerta_escape.entrar(self.personaje)
        self.assertTrue(resultado_entrar, "Se debería poder entrar por la PuertaDeSalida abierta.")
    
        self.assertEqual(self.personaje.posicion, self.h_exterior_victoria, f"El personaje debería estar en la habitación de victoria ({self.h_exterior_victoria.num}).")
        print(f"Posición personaje tras entrar: {self.personaje.posicion.num if self.personaje.posicion else 'None'}")

if __name__ == '__main__':
    unittest.main(verbosity=2)