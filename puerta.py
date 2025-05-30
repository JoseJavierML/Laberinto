from elemento_mapa import ElementoMapa

class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2): 
        super().__init__() 
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2

    def entrar(self, alguien): 
        # print(f"Puerta.entrar: {alguien.nombre} intenta entrar. Puerta abierta: {self.abierta}")
        if self.abierta:
            if alguien.posicion == self.lado1:
                print(f"Puerta '{getattr(self, 'nombre', 'Puerta')}' abierta, {alguien.nombre} va de {self.lado1} a {self.lado2}")
                self.lado2.entrar(alguien) 
                return True 
            elif alguien.posicion == self.lado2:
                print(f"Puerta '{getattr(self, 'nombre', 'Puerta')}' abierta, {alguien.nombre} va de {self.lado2} a {self.lado1}")
                self.lado1.entrar(alguien) 
                return True 
            else:
                print(f"Error: {alguien.nombre} no está en un lado válido ({self.lado1} o {self.lado2}) de la puerta '{getattr(self, 'nombre', 'Puerta')}'. Posición actual: {alguien.posicion}")
                return False
        else:
            print(f"La puerta '{getattr(self, 'nombre', 'Puerta')}' está cerrada.")
            return False 

    def abrir(self):
        if not self.abierta:
            print(f"Abriendo puerta '{getattr(self, 'nombre', 'Puerta')}'")
            self.abierta = True
        else:
            print(f"La puerta '{getattr(self, 'nombre', 'Puerta')}' ya estaba abierta.")
        return self.abierta


    def cerrar(self):
        if self.abierta:
            print(f"Cerrando puerta '{getattr(self, 'nombre', 'Puerta')}'")
            self.abierta = False
        else:
            print(f"La puerta '{getattr(self, 'nombre', 'Puerta')}' ya estaba cerrada.")
        return not self.abierta


    def esPuerta(self): 
        return True

    def __str__(self): 
        estado = "Abierta" if self.abierta else "Cerrada"
        return f"{getattr(self, 'nombre', 'puerta')} ({estado})"


class PuertaConLlaveGenerica(Puerta):
    def __init__(self, lado1, lado2, nombre="Puerta con Cerradura"): 
        super().__init__(lado1, lado2) 
        self.nombre = nombre 
        self.esta_bloqueada: bool = True 
        print(f"Puerta '{self.nombre}' creada entre {lado1} y {lado2}. Está BLOQUEADA.")

    def __str__(self):
        estado_abierta = "Abierta" if self.abierta else "Cerrada"
        estado_bloqueo = "Bloqueada" if self.esta_bloqueada else "Desbloqueada"
        return f"{self.nombre} ({estado_abierta}, {estado_bloqueo})"

    def abrir(self):
        if self.esta_bloqueada:
            print(f"¡La {self.nombre} está bloqueada con llave! Necesitas desbloquearla primero.")
            return False 
        super().abrir()
        
        return self.abierta 

    def desbloquear_con_llave(self) -> bool:
        if self.esta_bloqueada:
            self.esta_bloqueada = False

            print(f"La {self.nombre} ha sido desbloqueada. Ahora puedes intentar abrirla.")
            return True
        else:
            print(f"La {self.nombre} ya estaba desbloqueada.")
            return False

    def entrar(self, alguien):
        if self.esta_bloqueada:
            print(f"No puedes pasar. ¡La {self.nombre} está bloqueada con llave!")
            return False

        return super().entrar(alguien)
    
class PuertaDeSalida(Puerta):
    def __init__(self, lado1, lado2, codigo_secreto: str, nombre="Puerta de Escape Mágica"):
        super().__init__(lado1, lado2) 
        self.nombre: str = nombre
        self.codigo_secreto: str = codigo_secreto

        print(f"Puerta de Salida '{self.nombre}' creada entre {lado1} y {lado2}. Requiere un código.")

    def __str__(self):
        estado_abierta = "Abierta" if self.abierta else "Cerrada"
        return f"{self.nombre} ({estado_abierta} - Requiere código)"

    def intentar_abrir_con_codigo(self, codigo_introducido: str) -> bool:
        if self.abierta:
            print(f"La {self.nombre} ya está abierta.")
            return False 

        if codigo_introducido == self.codigo_secreto:
            self.abierta = True
            print(f"¡CLIC! El código '{codigo_introducido}' es correcto. ¡La {self.nombre} se ha abierto!")
            return True
        else:
            print(f"El código '{codigo_introducido}' es incorrecto. La {self.nombre} permanece cerrada.")
            return False

    def abrir(self):
        if self.abierta:
            print(f"La {self.nombre} ya está abierta.")
            return True
        else:
            print(f"La {self.nombre} no se puede abrir de forma normal. ¡Necesita un código secreto!")
            return False
