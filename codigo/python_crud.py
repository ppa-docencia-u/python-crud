# Asignatura UNAB 10496 Base de Datos
# Profesor Pablo Poblete Arrué
#
# Ejemplo básico para la:
# Implementación de un CRUD en Python con MySQL
# Llamada a procedimiento alamacenado
# Generación de gráfico a partir de query
# Ejemplos varios

import mysql.connector
from mysql.connector import Error

import matplotlib
# Configura backend sin GUI
# matplotlib.use('Agg') # Anti-Grain Geometry

# Para Backend interactivo (con GUI)
matplotlib.use('TkAgg') # Renderizado en lienzo (canvas) Tk (TkInter)
import matplotlib.pyplot as plt


# Configuración de conexión
def crea_conexion():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            database='classicmodels',
            user='reemplazar con su usurio',
            password='reemplazar con la clave del usuario'
        )
        if conn.is_connected():
            print("Conectado a la base de datos")
        return conn
    except Error as e:
        print(f"Error al intentar conectar: {e}")
        return None


# Funciones CRUD

# C--> CREATE: Añadir un nuevo producto
def crear_producto(producto):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = """INSERT INTO products (productCode, productName, productLine, 
            productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, producto)
            conn.commit()
            print("Producto añadido exitosamente")
        except Error as e:
            print(f"Error al añadir producto: {e}")
        finally:
            cursor.close()
            conn.close()


# R--> READ: Obtener datos de un producto por su código
def read_producto(productCode):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE productCode = %s"
            cursor.execute(query, productCode)

            result = cursor.fetchone()
            print("Producto:", result)
        except Error as e:
            print(f"Error al obtener producto: {e}")
        finally:
            cursor.close()
            conn.close()


# U--> UPDATE: Actualizar datos de un cliente
def update_producto(cantProd):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE products SET quantityInStock = quantityInStock + %s WHERE productCode = %s"
            cursor.execute(query, cantProd)
            conn.commit()
            print(f"Producto código {cantProd[1]} incrementado en: {cantProd[0]}")
        except Error as e:
            print(f"Error al actualizar existencia del producto código {cantProd[1]}: {e}")
        finally:
            cursor.close()
            conn.close()


# D--> DELETE: Eliminar un producto
def delete_producto(codigoProducto):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM products WHERE productCode = %s"
            cursor.execute(query, codigoProducto)
            conn.commit()
            print("Producto eliminado correctamente")
        except Error as e:
            print(f"Error al eliminar producto: {e}")
        finally:
            cursor.close()
            conn.close()


# DELETE: Eliminar un pedido
def delete_order(numeroOrden):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM orders WHERE orderNumber = %s"
            cursor.execute(query, numeroOrden)
            conn.commit()
            print("Pedido eliminado correctamente")
        except Error as e:
            print(f"Error al eliminar pedido: {e}")
        finally:
            cursor.close()
            conn.close()


# Función para ejecutar un procedimiento almacenado
def ejecuta_sp(nombre_sp, parametros=()):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc(nombre_sp, parametros)
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
            print(f"Resultados del procedimiento '{nombre_sp}':", resultados)
            return resultados
        except Error as e:
            print(f"Error al ejecutar procedimiento almacenado: {e}")
        finally:
            cursor.close()
            conn.close()


# Función para generar un gráfico de evolución de ventas
def grafico_evolucion_ventas():
    conn = crea_conexion()
    if conn.is_connected():
        try:
            cursor = conn.cursor()
            query = """
                        SELECT DATE_FORMAT(o.orderDate, '%Y-%m') AS mesOC, 
                               SUM(od.priceEach * od.quantityOrdered) AS valorTotalOC
                        FROM orders o
                        INNER JOIN orderdetails od USING (orderNumber)
                        GROUP BY 1
                        ORDER BY 1;
                        """
            cursor.execute(query)
            resultados = cursor.fetchall()

            print(f"Resultado >>> {resultados}")

            # Convertir resultados a listas
            # Genera lista con el item 0 (Año-mes) de cada tupla
            meses = [row[0] for row in resultados]  # Lista de meses
            # Genera lista con el item 1 de cada tupla
            ventas = [row[1] for row in resultados]  # Lista de ventas totales

            if meses and ventas:
                # Crear el gráfico
                plt.figure(figsize=(10, 6))
                plt.plot(meses, ventas, marker='o', linestyle='-', color='b')

                # Títuloa del gráfico
                plt.title("Evolución de Ventas Mensuales", fontsize=16)
                # Etiqueta del eje X
                plt.xlabel("Mes", fontsize=14)
                # Etiqueta del eje Y
                plt.ylabel("Ventas Totales (USD)", fontsize=14)

                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()

                if matplotlib.get_backend() == 'TkAgg':
                    # Despliega gráfico en entornos interactivos (con GUI)
                    # Como Jupyter Notebook o una IDE con soporte gráfico
                    plt.show()
                else:
                    # Genera y almacena el gráfico en un archivo
                    # Para entornos sin GUI
                    plt.savefig("ventas_mensuales.png")
                    print("El gráfico se guardó como 'ventas_mensuales.png'")
            else:
                print("No se encontraron datos para graficar")

        except Error as e:
            print(f"Error al generar gráfico de ventas: {e}")
        finally:
            conn.close()


# fetchall() lee todos los registros obtenidos por la query
def get_all_productos():
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)

            # Recupera todo
            registros = cursor.fetchall()
            print(f"Filas encontradas: {cursor.rowcount}")
            for fila, registro in enumerate(registros):
                print(f"{fila + 1}: {registro}")
        except Error as e:
            print(f"Error al obtener producto: {e}")
        finally:
            cursor.close()
            conn.close()


# fetchmany(n) lee los siguientes n registros recuperados por la query
def get_many_productos(n):
    conn = crea_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)

            # Recupera n registros
            registros = cursor.fetchmany(size=n)
            for fila, registro in enumerate(registros):
                print(f"{fila + 1}: {registro}")
        except Error as e:
            print(f"Error al obtener producto: {e}")
        finally:
            # Es necesario recuperar todas las filas pendientes en la query antes de
            # ejecutar otra query o cerrar la conexión
            cursor.fetchall()
            cursor.close()
            conn.close()


# Ejemplo de uso
if __name__ == "__main__":
    # Añadir un producto
    producto = ("S800_1678", "Harley Davidson", "Motorcycles", "1:10",
                "Min Lin Diecast", "Detailed replica", 7900, 95.70, 103.42)

    # C: Crear (insertar) el producto
    crear_producto(producto)

    # R: recuperar (leer) productos
    read_producto(("S800_1678",))

    # U: actualiza cantida producto
    update_producto((100, "S800_1678"))

    #    Validación
    read_producto(("S800_1678",))

    # D: Eliminar el producto
    delete_producto(("S800_1678",))

    # Ejemplo de llamada a un procedimiento almacenado
    # nombre_sp = 'get_clientes_alto_valor'
    # con parámetro min_credito
    ejecuta_sp('get_clientes_alto_valor', (120000,))

    # Ejemplo: Generar gráfico de evolución de ventas
    grafico_evolucion_ventas()


    ######################
    # Otros ejemplos
    ######################
    # Listado de productos
    #get_all_productos()

    # Listar algunnos
    #get_many_productos(5)

