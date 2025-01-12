import openpyxl
from collections import defaultdict

def cargar_reacciones(archivo):
    """Carga las reacciones desde un archivo de Excel."""
    wb = openpyxl.load_workbook(archivo)
    hoja = wb.active
    reacciones = []

    for fila in hoja.iter_rows(min_row=1, values_only=True):
        reaccion_id = fila[0]
        reaccion = fila[1]
        reacciones.append((reaccion_id, reaccion))
    
    return reacciones

def evaluar_frecuencia_compuestos(reacciones):
    """
    Evala en cuntas reacciones aparece cada compuesto,
    ya sea como reactante o como producto.
    """
    frecuencia = defaultdict(int)

    for reaccion_id, reaccion in reacciones:
        # Separar reactantes y productos
        reactantes, productos = reaccion.split("->")
        reactantes = reactantes.split("+")
        productos = productos.split("+")

        # Contar cada compuesto como reactante o producto
        for compuesto in reactantes + productos:
            frecuencia[compuesto] += 1

    return frecuencia

# Archivo de reacciones y anlisis
archivo_reacciones = "Reacciones Evaluadas.xlsx"
reacciones = cargar_reacciones(archivo_reacciones)

# Evaluar frecuencias
frecuencia_compuestos = evaluar_frecuencia_compuestos(reacciones)

# Mostrar resultados
print("Frecuencia de compuestos en las reacciones (como reactante o producto):")
for compuesto, frecuencia in sorted(frecuencia_compuestos.items(), key=lambda x: x[1], reverse=True):
    print(f"{compuesto}: {frecuencia} reacciones")
