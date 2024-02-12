"""
Calculadora Class:

Una clase para calcular las ventas totales basadas en la lista de productos y ventas.

Attributes:
    advertencias (dict): Un diccionario que almacena advertencias.
    nombres_archivos (list): Una lista que almacena el nombre de los archivos procesados.

Methods:
    __init__(): Inicializa Calculadora con 
    advertencias y nombres_archivos vacios.
    leer_archivo(path: str) -> list: Obtiene datos de un archivo JSON.
    leer_archivos_en_pares() -> list: Obtiene pares de archivos de los argumentos
    y devuelve sus datos..
    eproducto(product_name: str, product_list: list) -> Obtiene un producto por su nombre 
    en la lista de productos.
    dict: El producto si se encuentra, de lo contrario un diccionario vacío.
    calcular_ventas(product_list: list, sales: list, file_name: str) -> Calcula las ventas totales
    basadas en la lista de productos y los datos de ventas
    float: El monto total de ventas.
    escribir_a_archivo(results: str) -> None: Escribe los resultados en un archivo 
    llamado ResultadosVentas.txt
    calcular(): Calcula las ventas totales a partir de los archivos de entrada
    y escribe los resultados en un archivo.
"""
import json
import sys
import time


class Calculadora:
    """Clase para calcular las ventas en relación
    de las listas de productos y datos de ventas."""

    def __init__(self):
        """Se inicia la Calculadora con listas de advertencias
        y nombres de archivos vacías."""
        self.advertencias = {}
        self.nombres_archivos = []

    def leer_archivo(self, ruta: str) -> list:
        """Obtiene datos de un archivo JSON.

        Args:
            ruta (str): La ruta al archivo JSON.

        Returns:
            list: Los datos leídos del archivo JSON.
        """
        try:
            with open(ruta, encoding='utf8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            print(f'Error: No se pudo encontrar el archivo {ruta}.')
            return []
        return datos

    def leer_archivos_en_pares(self) -> list:
        """Obtiene pares de archivos de los argumentos
        y devuelve sus datos.

        Returns:
            list: Una lista que contiene pares de listas
            de productos y datos de ventas."""
        datos = []
        for i in range(0, len(sys.argv)-1, 2):
            lista_prod, archivo_ventas = sys.argv[i+1:i+3]
            if 'ListaProductos' in archivo_ventas:
                lista_prod, archivo_ventas = archivo_ventas, lista_prod
            lista_productos = self.leer_archivo(lista_prod)
            ventas = self.leer_archivo(archivo_ventas)
            self.nombres_archivos.append({'productos': lista_prod,
                                          'ventas': archivo_ventas})
            datos.append([lista_productos, ventas])
        return datos

    def eproducto(self, nombre_producto: str, lista_productos: list) -> dict:
        """Obtiene un producto por su nombre en la lista de productos.

        Args:
            nombre_producto (str): El nombre del producto a encontrar.
            lista_productos (list): La lista de productos en la que buscar.

        Returns:
            dict: El producto si se encuentra,
            de lo contrario un diccionario vacío."""
        for producto in lista_productos:
            if producto.get('titulo') == nombre_producto:
                return producto
        return {}

    def calcular_ventas(self, lista_productos: list, ventas: list,
                        nombre_archivo: str) -> float:
        """Calcula las ventas totales basadas en la lista
            de productos y los datos de ventas.

        Args:
            lista_productos (list): La lista de productos.
            ventas (list): Los datos de ventas.
            nombre_archivo (str): El nombre del archivo que se está procesando.

        Returns:
            float: El monto total de ventas.
        """
        total = 0
        self.advertencias[nombre_archivo] = []
        for venta in ventas:
            producto = self.eproducto(venta.get('Producto'), lista_productos)
            if not producto:
                self.advertencias[nombre_archivo].append(
                    f'Producto "{venta.get("Producto")}" no encontrado')
                continue
            total += venta.get('Cantidad', 0) * producto.get('precio', 0)
        return total

    def escribir_a_archivo(self, resultados: str) -> None:
        """Escribe los resultados en un archivo llamado ResultadosVentas.txt.

        Args:
            resultados (str): Los resultados que se escribirán en el archivo.
        """
        with open('ResultadosVentas.txt', 'w', encoding='utf8') as f:
            f.write(resultados)

    def calcular(self):
        """Calcula las ventas totales a partir de los archivos de entrada
           y escribe los resultados en un archivo."""
        tiempo_inicio = time.time()
        if (len(sys.argv) - 1) % 2 != 0:
            print('Error: Proporcionar las rutas de los archivos en pares.')
            sys.exit()

        datos = self.leer_archivos_en_pares()
        resultados = '\n'

        for i, (lista_productos, ventas) in enumerate(datos):
            nombre_lista_prod = self.nombres_archivos[i]['productos']
            total = self.calcular_ventas(lista_productos, ventas,
                                         nombre_lista_prod)
            resultados += f"""- Ventas totales en {self.nombres_archivos[i]
            ["ventas"]}:{total: ,.2f}\n"""
            if self.advertencias[nombre_lista_prod]:
                resultados += f"""\nAdvertencias: Productos no encontrados
                               en la lista {nombre_lista_prod}:\n\n"""
                resultados += '\n'.join(self.advertencias[nombre_lista_prod])

        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        resultados += f"""\n\nTiempo total de ejecución: {tiempo_total: .2f}
                       segundos\n"""

        self.escribir_a_archivo(resultados)
        print(resultados)


if __name__ == "__main__":
    calculator = Calculadora()
    calculator.calcular()
