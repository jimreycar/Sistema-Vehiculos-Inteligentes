
import tkinter as tk
from tkinter import messagebox
import logging
from decimal import Decimal, InvalidOperation


# =====================================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# =====================================================

logging.basicConfig(
    filename="vehiculos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger("SistemaVehiculos")


# =====================================================
# 2. CLASE VEHICULO
# =====================================================

class Vehiculo:

    def __init__(self, marca, modelo, precio):

        self.marca = marca.strip()
        self.modelo = modelo.strip()
        self.precio = self.convertir_decimal(precio)

        if not self.marca or not self.modelo:
            raise ValueError(
                "La marca y el modelo son obligatorios."
            )

        if self.precio < 0:
            raise ValueError(
                "El precio no puede ser negativo."
            )

        logger.info(
            "Vehículo creado: %s %s",
            self.marca,
            self.modelo
        )

    # -------------------------------------------------
    # MÉTODO AUXILIAR PARA VALIDAR VALORES NUMÉRICOS
    # -------------------------------------------------

    @staticmethod
    def convertir_decimal(valor):

        if isinstance(valor, bool):
            raise TypeError("El valor debe ser numérico.")

        try:
            numero = Decimal(str(valor))

            if not numero.is_finite():
                raise ValueError(
                    "El valor debe ser un número finito."
                )

            return numero

        except (InvalidOperation, ValueError, TypeError) as error:
            raise ValueError(
                "Se debe ingresar un valor numérico válido."
            ) from error

    # -------------------------------------------------
    # MÉTODO CON DIFERENTES VARIANTES DE CÁLCULO
    # -------------------------------------------------

    def calcular_costo(self, impuesto=0, descuento=0):

        try:

            impuesto = self.convertir_decimal(impuesto)
            descuento = self.convertir_decimal(descuento)

            # Validar impuesto
            if impuesto < 0 or impuesto > 100:
                raise ValueError(
                    "El impuesto debe estar entre 0 y 100 %."
                )

            # Validar descuento
            if descuento < 0 or descuento > self.precio:
                raise ValueError(
                    "El descuento no puede superar el precio."
                )

            # Calcular subtotal
            subtotal = self.precio - descuento

            # Calcular valor del impuesto
            valor_impuesto = (
                subtotal * impuesto / Decimal("100")
            )

            # Calcular costo final
            costo_total = subtotal + valor_impuesto

            logger.info(
                "Cálculo realizado para %s %s. "
                "Precio: %s, Impuesto: %s%%, "
                "Descuento: %s, Total: %s",
                self.marca,
                self.modelo,
                self.precio,
                impuesto,
                descuento,
                costo_total
            )

            return costo_total

        except (ValueError, TypeError):

            logger.exception(
                "Error al calcular el costo del vehículo %s %s",
                self.marca,
                self.modelo
            )

            raise

    # -------------------------------------------------
    # MÉTODO PARA MOSTRAR INFORMACIÓN DEL VEHÍCULO
    # -------------------------------------------------

    def obtener_informacion(self):

        return (
            f"Marca: {self.marca}\n"
            f"Modelo: {self.modelo}\n"
            f"Precio: ${self.precio:,.2f}"
        )


# =====================================================
# 3. CLASE DE LA INTERFAZ GRÁFICA CON TKINTER
# =====================================================

class SistemaVehiculos:

    def __init__(self, ventana):

        self.ventana = ventana
        self.vehiculo = None

        self.ventana.title(
            "Sistema de Vehículos Inteligentes"
        )

        self.ventana.geometry("500x520")
        self.ventana.resizable(False, False)

        logger.info("Aplicación iniciada correctamente.")

        self.crear_interfaz()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    # -------------------------------------------------
    # CREACIÓN DE LOS ELEMENTOS DE LA INTERFAZ
    # -------------------------------------------------

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="SISTEMA DE VEHÍCULOS INTELIGENTES",
            font=("Arial", 15, "bold")
        )

        titulo.pack(pady=20)

        # Marca
        tk.Label(
            self.ventana,
            text="Marca del vehículo:"
        ).pack()

        self.entrada_marca = tk.Entry(
            self.ventana,
            width=35
        )

        self.entrada_marca.pack(pady=5)

        # Modelo
        tk.Label(
            self.ventana,
            text="Modelo del vehículo:"
        ).pack()

        self.entrada_modelo = tk.Entry(
            self.ventana,
            width=35
        )

        self.entrada_modelo.pack(pady=5)

        # Precio
        tk.Label(
            self.ventana,
            text="Precio del vehículo:"
        ).pack()

        self.entrada_precio = tk.Entry(
            self.ventana,
            width=35
        )

        self.entrada_precio.pack(pady=5)

        # Impuesto
        tk.Label(
            self.ventana,
            text="Impuesto (%):"
        ).pack()

        self.entrada_impuesto = tk.Entry(
            self.ventana,
            width=35
        )

        self.entrada_impuesto.insert(0, "0")
        self.entrada_impuesto.pack(pady=5)

        # Descuento
        tk.Label(
            self.ventana,
            text="Descuento:"
        ).pack()

        self.entrada_descuento = tk.Entry(
            self.ventana,
            width=35
        )

        self.entrada_descuento.insert(0, "0")
        self.entrada_descuento.pack(pady=5)

        # Botón de registro
        tk.Button(
            self.ventana,
            text="Registrar vehículo",
            width=25,
            command=self.registrar_vehiculo
        ).pack(pady=10)

        # Botón de cálculo
        tk.Button(
            self.ventana,
            text="Calcular costo",
            width=25,
            command=self.calcular_costo
        ).pack(pady=5)

        # Área de resultados
        self.resultado = tk.Label(
            self.ventana,
            text="Esperando información...",
            font=("Arial", 11),
            justify="left"
        )

        self.resultado.pack(pady=15)

    # -------------------------------------------------
    # REGISTRAR VEHÍCULO
    # -------------------------------------------------

    def registrar_vehiculo(self):

        try:

            marca = self.entrada_marca.get().strip()
            modelo = self.entrada_modelo.get().strip()
            precio = self.entrada_precio.get().strip()

            self.vehiculo = Vehiculo(
                marca,
                modelo,
                precio
            )

            logger.info(
                "Registro exitoso del vehículo: %s %s",
                marca,
                modelo
            )

            messagebox.showinfo(
                "Registro exitoso",
                "El vehículo fue registrado correctamente."
            )

            self.resultado.config(
                text=self.vehiculo.obtener_informacion()
            )

        except (ValueError, TypeError) as error:

            logger.warning(
                "No fue posible registrar el vehículo: %s",
                error
            )

            messagebox.showerror(
                "Error de registro",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado al registrar el vehículo."
            )

            messagebox.showerror(
                "Error",
                "Ocurrió un error inesperado."
            )

    # -------------------------------------------------
    # CALCULAR COSTO DEL VEHÍCULO
    # -------------------------------------------------

    def calcular_costo(self):

        try:

            # Verificar que exista un vehículo registrado
            if self.vehiculo is None:
                raise ValueError(
                    "Primero debe registrar un vehículo."
                )

            impuesto = self.entrada_impuesto.get().strip()
            descuento = self.entrada_descuento.get().strip()

            # Calcular utilizando los parámetros opcionales
            total = self.vehiculo.calcular_costo(
                impuesto=impuesto or "0",
                descuento=descuento or "0"
            )

            self.resultado.config(
                text=(
                    f"{self.vehiculo.marca} "
                    f"{self.vehiculo.modelo}\n"
                    f"Costo final: ${total:,.2f}"
                )
            )

            messagebox.showinfo(
                "Cálculo realizado",
                f"El costo final es: ${total:,.2f}"
            )

        except (ValueError, TypeError) as error:

            logger.warning(
                "No se pudo realizar el cálculo: %s",
                error
            )

            messagebox.showerror(
                "Error de cálculo",
                str(error)
            )

        except Exception:

            logger.exception(
                "Error inesperado durante el cálculo."
            )

            messagebox.showerror(
                "Error",
                "Ocurrió un error inesperado."
            )

    # -------------------------------------------------
    # CERRAR APLICACIÓN
    # -------------------------------------------------

    def cerrar_aplicacion(self):

        logger.info(
            "Sistema de Vehículos Inteligentes finalizado."
        )

        self.ventana.destroy()


# =====================================================
# 4. EJECUCIÓN PRINCIPAL DEL PROGRAMA
# =====================================================

if __name__ == "__main__":

    try:

        ventana = tk.Tk()

        aplicacion = SistemaVehiculos(ventana)

        ventana.mainloop()

    except Exception:

        logger.exception(
            "Error crítico durante la ejecución del sistema."
        )

        raise
