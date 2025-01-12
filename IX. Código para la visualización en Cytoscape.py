import openpyxl
from collections import defaultdict

def cargar_reacciones(archivo):
    wb = openpyxl.load_workbook(archivo)
    hoja = wb.active
    reacciones = []

    for fila in hoja.iter_rows(min_row=1, values_only=True):
        reaccion_id = fila[0]
        reaccion = fila[1]
        reacciones.append((reaccion_id, reaccion))
    
    return reacciones

def expansion_red(seed_set_inicial, reacciones):
    seed_set = set(seed_set_inicial)
    todos_los_compuestos_creados = set(seed_set)
    todas_las_reacciones_evaluadas = set()
    conectividad = defaultdict(int)
    primera_aparicion = {}
    iteracion = 0
    cambios = True

    # Inicializar conectividad y primera aparicion para el seed set inicial
    for compuesto in seed_set:
        conectividad[compuesto] = 0
        primera_aparicion[compuesto] = (0, "seed set inicial")

    # Inicializar lista para almacenar los resultados de compuestos por iteracion
    compuestos_por_iteracion = [(0, len(seed_set))]  # Iteracion 0; seed set inicial

    seed_set_exclusivo_anterior = set(seed_set_inicial)

    while cambios:
        iteracion += 1
        cambios = False
        compuestos_creados = []
        
        for reaccion_id, reaccion in reacciones:
            reactantes, productos = reaccion.split("->")
            reactantes = reactantes.split("+")
            productos = productos.split("+")

            # Comprobar si todos los reactantes estan en el seed set
            if all(reactante in seed_set for reactante in reactantes):
                todas_las_reacciones_evaluadas.add(reaccion_id)

                # Verificar si los productos se deben agregar
                nuevos_productos = []
                for producto in productos:
                    es_nuevo = 1 if producto not in seed_set else 0
                    conectividad[producto] += 1  # Contar conectividad
                    if es_nuevo:
                        cambios = True
                        compuestos_creados.append(producto)
                        todos_los_compuestos_creados.add(producto)
                        if producto not in primera_aparicion:
                            primera_aparicion[producto] = (iteracion, reaccion_id)

        # Actualizar el seed set
        nuevos_compuestos = [p for p in compuestos_creados if p not in seed_set]
        seed_set.update(nuevos_compuestos)

        # Actualizar el seed set exclusivo creado
        seed_set_exclusivo_anterior = set(nuevos_compuestos)

        # Guardar el numero de compuestos creados exclusivamente en esta iteracion
        compuestos_por_iteracion.append((iteracion, len(seed_set_exclusivo_anterior)))

    # Imprimir resultados de compuestos por iteracion
    print("Iteracion;Numero de compuestos")
    for iteracion, num_compuestos in compuestos_por_iteracion:
        print(f"{iteracion};{num_compuestos}")

# Definir el seed set inicial con compuestos de tipo "cpd"
seed_set_inicial = ["cpd00001","cpd00009","cpd00011","cpd00013","cpd00020","cpd00021","cpd00024","cpd00029","cpd00032","cpd00034","cpd00036","cpd00040","cpd00047","cpd00057","cpd00067","cpd00106","cpd00130","cpd00139","cpd00149","cpd00180","cpd00205","cpd00239","cpd00242","cpd00254","cpd00260","cpd00308","cpd00331","cpd00830","cpd00971","cpd01078","cpd01194","cpd10515","cpd10516","cpd11574","cpd11608","cpd11609","cpd11610","cpd11614","cpd11616","cpd11625","cpd11632","cpd11640","cpd11848","cpd15574","cpd16654","cpd17287","cpd37270","cpd37272","cpd37275"]
# Cargar las reacciones desde el archivo
archivo_reacciones = "II. Base de datos KEGG version 2020 (anaerobica).xlsx"
reacciones = cargar_reacciones(archivo_reacciones)

# Ejecutar la expansion de red
expansion_red(seed_set_inicial, reacciones)
