# ==========================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# ESCUELA DE CIENCIAS BÁSICAS TECNOLOGÍA E INGENIERÍA
# CURSO: PROGRAMACIÓN
# CÓDIGO: 213023
#
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
# SERVICIOS Y RESERVAS
#
# ESTUDIANTE: Jesly Manuel Barbudo Oviedo y Ebed Melec Mayorca Gutierrez
# GRUPO: 213023_43
# ÁREA DE FORMACIÓN: Ingeniería de Sistemas
# TUTOR: Yahith Yamid Gutierrez Gomez
#
# DESCRIPCIÓN:
# Sistema desarrollado en Python usando:
# ✔ Programación Orientada a Objetos
# ✔ Herencia
# ✔ Polimorfismo
# ✔ Encapsulación
# ✔ Clases Abstractas
# ✔ Manejo Avanzado de Excepciones
# ✔ Tkinter
# ✔ Archivo de Logs
# ✔ Validaciones Robustas
#
# ==========================================================

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================================
# FUNCIÓN DE LOGS
# ==========================================================

def registrar_log(mensaje):

    with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:

        archivo.write(
            f"{datetime.now()} -> {mensaje}\n"
        )

# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# ==========================================================
# CLASE ABSTRACTA PERSONA
# ==========================================================

class Persona(ABC):

    def __init__(self, nombre, documento):

        self.nombre = nombre
        self.documento = documento

    @abstractmethod
    def mostrar_datos(self):
        pass

# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(Persona):

    def __init__(self, nombre, documento, telefono):

        if nombre.strip() == "":
            raise ClienteError(
                "El nombre no puede estar vacío"
            )

        if not documento.isdigit():
            raise ClienteError(
                "El documento debe ser numérico"
            )

        if not telefono.isdigit():
            raise ClienteError(
                "El teléfono debe ser numérico"
            )

        super().__init__(nombre, documento)

        self.__telefono = telefono

    def obtener_telefono(self):

        return self.__telefono

    def mostrar_datos(self):

        return (
            f"{self.nombre} - "
            f"{self.documento} - "
            f"{self.__telefono}"
        )

# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ABC):

    def __init__(self, nombre, precio):

        if precio <= 0:
            raise ServicioError(
                "El precio debe ser mayor a cero"
            )

        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ==========================================================
# SERVICIO RESERVA SALA
# ==========================================================

class ReservaSala(Servicio):

    def __init__(self, nombre, precio, horas):

        super().__init__(nombre, precio)

        self.horas = horas

    def calcular_costo(self):

        return self.precio * self.horas

    def descripcion(self):

        return (
            f"Reserva de sala "
            f"por {self.horas} horas"
        )

# ==========================================================
# SERVICIO ALQUILER EQUIPO
# ==========================================================

class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio, dias):

        super().__init__(nombre, precio)

        self.dias = dias

    def calcular_costo(self):

        return self.precio * self.dias

    def descripcion(self):

        return (
            f"Alquiler por "
            f"{self.dias} días"
        )

# ==========================================================
# SERVICIO ASESORÍA
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, precio, nivel):

        super().__init__(nombre, precio)

        self.nivel = nivel

    def calcular_costo(self):

        if self.nivel == "Avanzado":

            return self.precio * 1.5

        return self.precio

    def descripcion(self):

        return (
            f"Asesoría nivel "
            f"{self.nivel}"
        )

# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ReservaError(
                "Duración inválida"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        self.estado = "Confirmada"

    def cancelar(self):

        self.estado = "Cancelada"

    def procesar(self):

        try:

            total = self.servicio.calcular_costo()

            self.confirmar()

            return total

        except Exception as error:

            raise ReservaError(
                "Error procesando reserva"
            ) from error

# ==========================================================
# LISTAS PRINCIPALES
# ==========================================================

clientes = []
reservas = []

# ==========================================================
# CREACIÓN DE VENTANA
# ==========================================================

ventana = tk.Tk()

ventana.title(
    "Sistema Integral de Gestión - Software FJ"
)

ventana.state("zoomed")

ventana.configure(bg="#F2F2F2")

# ==========================================================
# TÍTULO
# ==========================================================

titulo = tk.Label(
    ventana,
    text=(
        "SISTEMA INTEGRAL DE GESTIÓN "
        "DE CLIENTES Y RESERVAS"
    ),
    font=("Arial", 20, "bold"),
    bg="#F2F2F2",
    fg="#003366"
)

titulo.pack(pady=20)

# ==========================================================
# FRAME PRINCIPAL
# ==========================================================

frame_principal = tk.Frame(
    ventana,
    bg="white",
    bd=2,
    relief="solid"
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# ==========================================================
# FUNCIONES CLIENTES
# ==========================================================

def registrar_cliente():

    try:

        nombre = entry_nombre.get()
        documento = entry_documento.get()
        telefono = entry_telefono.get()

        cliente = Cliente(
            nombre,
            documento,
            telefono
        )

        clientes.append(cliente)

        tabla_clientes.insert(
            "",
            tk.END,
            values=(
                cliente.nombre,
                cliente.documento,
                cliente.obtener_telefono()
            )
        )

        registrar_log(
            f"Cliente registrado: {cliente.nombre}"
        )

        messagebox.showinfo(
            "Éxito",
            "Cliente registrado"
        )

        entry_nombre.delete(0, tk.END)
        entry_documento.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

    except Exception as error:

        registrar_log(
            f"Error registrando cliente: {error}"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )

# ==========================================================
# MOSTRAR CLIENTES
# ==========================================================

def ver_clientes():

    try:

        lista_clientes.delete(0, tk.END)

        if len(clientes) == 0:

            lista_clientes.insert(
                tk.END,
                "No existen clientes"
            )

            return

        for cliente in clientes:

            texto = (
                f"{cliente.nombre} | "
                f"{cliente.documento} | "
                f"{cliente.obtener_telefono()}"
            )

            lista_clientes.insert(
                tk.END,
                texto
            )

    except Exception as error:

        registrar_log(
            f"Error mostrando clientes: {error}"
        )

# ==========================================================
# BUSCAR CLIENTE
# ==========================================================

def buscar_cliente():

    try:

        documento = entry_buscar.get()

        lista_clientes.delete(0, tk.END)

        encontrado = False

        for cliente in clientes:

            if cliente.documento == documento:

                texto = (
                    f"Cliente encontrado: "
                    f"{cliente.nombre}"
                )

                lista_clientes.insert(
                    tk.END,
                    texto
                )

                encontrado = True

        if not encontrado:

            raise ClienteError(
                "Cliente no encontrado"
            )

    except Exception as error:

        registrar_log(
            f"Error buscando cliente: {error}"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )

# ==========================================================
# ELIMINAR CLIENTE
# ==========================================================

def eliminar_cliente():

    try:

        documento = entry_buscar.get()

        eliminado = False

        for cliente in clientes:

            if cliente.documento == documento:

                clientes.remove(cliente)

                eliminado = True

                registrar_log(
                    f"Cliente eliminado: {cliente.nombre}"
                )

                break

        if not eliminado:

            raise ClienteError(
                "Cliente no encontrado"
            )

        ver_clientes()

        messagebox.showinfo(
            "Éxito",
            "Cliente eliminado"
        )

    except Exception as error:

        registrar_log(
            f"Error eliminando cliente: {error}"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )

# ==========================================================
# CREAR RESERVAS
# ==========================================================

def crear_reserva():

    try:

        nombre_cliente = (
            entry_reserva_cliente.get().strip()
        )

        tipo_servicio = combo_tipo.get()

        precio = float(
            entry_precio.get()
        )

        cantidad = int(
            entry_cantidad.get()
        )

        cliente_objeto = None

        for cliente in clientes:

            if cliente.nombre.lower() == nombre_cliente.lower():

                cliente_objeto = cliente

                break

        if cliente_objeto is None:

            raise ReservaError(
                "Cliente no registrado"
            )

        # ==============================================
        # CREAR SERVICIO
        # ==============================================

        if tipo_servicio == "Reserva por Horas":

            servicio = ReservaSala(
                "Sala Empresarial",
                precio,
                cantidad
            )

        elif tipo_servicio == "Reserva por Días":

            servicio = AlquilerEquipo(
                "Equipo",
                precio,
                cantidad
            )

        else:

            servicio = AsesoriaEspecializada(
                "Asesoría",
                precio,
                "Avanzado"
            )

        reserva = Reserva(
            cliente_objeto,
            servicio,
            cantidad
        )

        reservas.append(reserva)

        total = reserva.procesar()

        texto = (
            f"Cliente: {cliente_objeto.nombre} | "
            f"Servicio: {tipo_servicio} | "
            f"Cantidad: {cantidad} | "
            f"Total: ${total:,.0f}"
        )

        lista_reservas.insert(
            tk.END,
            texto
        )

        registrar_log(
            f"Reserva creada: {texto}"
        )

        messagebox.showinfo(
            "Éxito",
            "Reserva registrada"
        )

        entry_reserva_cliente.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Precio y cantidad deben ser numéricos"
        )

    except Exception as error:

        registrar_log(
            f"Error creando reserva: {error}"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )

# ==========================================================
# FORMULARIO CLIENTES
# ==========================================================

frame_formulario = tk.LabelFrame(
    frame_principal,
    text="Registro Clientes",
    font=("Arial", 12, "bold"),
    bg="white"
)

frame_formulario.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    frame_formulario,
    text="Nombre:",
    bg="white"
).grid(row=0, column=0, padx=10)

entry_nombre = tk.Entry(
    frame_formulario,
    width=25
)

entry_nombre.grid(row=0, column=1)

tk.Label(
    frame_formulario,
    text="Documento:",
    bg="white"
).grid(row=0, column=2)

entry_documento = tk.Entry(
    frame_formulario,
    width=25
)

entry_documento.grid(row=0, column=3)

tk.Label(
    frame_formulario,
    text="Teléfono:",
    bg="white"
).grid(row=0, column=4)

entry_telefono = tk.Entry(
    frame_formulario,
    width=25
)

entry_telefono.grid(row=0, column=5)

btn_registrar = tk.Button(
    frame_formulario,
    text="Registrar Cliente",
    bg="#4CAF50",
    fg="white",
    command=registrar_cliente
)

btn_registrar.grid(
    row=0,
    column=6,
    padx=10
)

# ==========================================================
# TABLA CLIENTES
# ==========================================================

tabla_clientes = ttk.Treeview(
    frame_principal,
    columns=(
        "Nombre",
        "Documento",
        "Teléfono"
    ),
    show="headings",
    height=8
)

tabla_clientes.heading(
    "Nombre",
    text="Nombre"
)

tabla_clientes.heading(
    "Documento",
    text="Documento"
)

tabla_clientes.heading(
    "Teléfono",
    text="Teléfono"
)

tabla_clientes.pack(
    fill="x",
    padx=10,
    pady=10
)

# ==========================================================
# FRAME BUSCAR CLIENTES
# ==========================================================

frame_busqueda = tk.LabelFrame(
    frame_principal,
    text="Buscar y Eliminar Clientes",
    font=("Arial", 12, "bold"),
    bg="white"
)

frame_busqueda.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    frame_busqueda,
    text="Documento:",
    bg="white"
).grid(row=0, column=0, padx=10)

entry_buscar = tk.Entry(
    frame_busqueda,
    width=25
)

entry_buscar.grid(row=0, column=1)

btn_buscar = tk.Button(
    frame_busqueda,
    text="Buscar",
    bg="#2196F3",
    fg="white",
    command=buscar_cliente
)

btn_buscar.grid(
    row=0,
    column=2,
    padx=10
)

btn_eliminar = tk.Button(
    frame_busqueda,
    text="Eliminar",
    bg="#F44336",
    fg="white",
    command=eliminar_cliente
)

btn_eliminar.grid(
    row=0,
    column=3,
    padx=10
)

btn_ver = tk.Button(
    frame_busqueda,
    text="Ver Clientes",
    bg="#009688",
    fg="white",
    command=ver_clientes
)

btn_ver.grid(
    row=0,
    column=4,
    padx=10
)

# ==========================================================
# LISTA CLIENTES
# ==========================================================

lista_clientes = tk.Listbox(
    frame_principal,
    height=6,
    font=("Arial", 10)
)

lista_clientes.pack(
    fill="x",
    padx=10,
    pady=10
)

# ==========================================================
# FRAME RESERVAS
# ==========================================================

frame_reservas = tk.LabelFrame(
    frame_principal,
    text="Gestión de Reservas",
    font=("Arial", 12, "bold"),
    bg="white"
)

frame_reservas.pack(
    fill="x",
    padx=10,
    pady=10
)

tk.Label(
    frame_reservas,
    text="Cliente:",
    bg="white"
).grid(row=0, column=0, padx=10)

entry_reserva_cliente = tk.Entry(
    frame_reservas,
    width=20
)

entry_reserva_cliente.grid(
    row=0,
    column=1
)

tk.Label(
    frame_reservas,
    text="Tipo:",
    bg="white"
).grid(row=0, column=2)

combo_tipo = ttk.Combobox(
    frame_reservas,
    values=[
        "Reserva por Horas",
        "Reserva por Días",
        "Asesoría"
    ],
    width=20
)

combo_tipo.grid(
    row=0,
    column=3
)

combo_tipo.current(0)

tk.Label(
    frame_reservas,
    text="Precio:",
    bg="white"
).grid(row=0, column=4)

entry_precio = tk.Entry(
    frame_reservas,
    width=15
)

entry_precio.grid(
    row=0,
    column=5
)

tk.Label(
    frame_reservas,
    text="Horas/Días:",
    bg="white"
).grid(row=0, column=6)

entry_cantidad = tk.Entry(
    frame_reservas,
    width=15
)

entry_cantidad.grid(
    row=0,
    column=7
)

btn_reserva = tk.Button(
    frame_reservas,
    text="Crear Reserva",
    bg="#673AB7",
    fg="white",
    command=crear_reserva
)

btn_reserva.grid(
    row=0,
    column=8,
    padx=10
)

# ==========================================================
# LISTA RESERVAS
# ==========================================================

lista_reservas = tk.Listbox(
    frame_principal,
    height=8,
    font=("Arial", 10)
)

lista_reservas.pack(
    fill="x",
    padx=10,
    pady=10
)

# ==========================================================
# FOOTER
# ==========================================================

footer = tk.Label(
    ventana,
    text=(
        "UNAD - Programación 213023 "
        "| Sistema desarrollado en Python"
    ),
    font=("Arial", 10),
    bg="#F2F2F2",
    fg="#555555"
)

footer.pack(pady=10)

# ==========================================================
# EJECUCIÓN SEGURA
# ==========================================================

if __name__ == "__main__":

    try:

        registrar_log(
            "Sistema iniciado correctamente"
        )

        ventana.mainloop()

    except Exception as error:

        registrar_log(
            f"Error fatal: {error}"
        )

        print(
            "Error crítico:",
            error
        )

    finally:

        registrar_log(
            "Sistema finalizado"
        )
