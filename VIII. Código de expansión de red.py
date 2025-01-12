import openpyxl

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
    iteracion = 0
    cambios = True

    print(f"Seed set inicial: {seed_set}")

    while cambios:
        iteracion += 1
        cambios = False
        compuestos_creados = []
        
        for reaccion_id, reaccion in reacciones:
            reactantes, productos = reaccion.split("->")
            reactantes = reactantes.split("+")
            productos = productos.split("+")

            # Comprobar si todos los reactantes estn en el seed set
            if all(reactante in seed_set for reactante in reactantes):
                todas_las_reacciones_evaluadas.add(reaccion_id)
                # Verificar los productos generados
                for producto in productos:
                    es_nuevo = 1 if producto not in seed_set else 0
                    if es_nuevo:
                        cambios = True
                        compuestos_creados.append((iteracion, reaccion_id, reactantes, productos, es_nuevo))
                        todos_los_compuestos_creados.add(producto)
        
        # Mostrar los compuestos creados en esta iteracin
        for comp in compuestos_creados:
            iter_num, rxn_id, reactantes, productos, es_nuevo = comp
            for reactante in reactantes:
                print(f"{{{iter_num};{rxn_id};{reactante};i;0}}")
            for producto in productos:
                print(f"{{{iter_num};{rxn_id};{producto};d;{es_nuevo}}}")
        
        # Actualizar el seed set
        seed_set.update([p for _, _, _, ps, _ in compuestos_creados for p in ps if p not in seed_set])
    
    print(f"Todos los compuestos creados: {list(todos_los_compuestos_creados)}")
    print(f"Todas las reacciones evaluadas: {list(todas_las_reacciones_evaluadas)}")

# Definir el seed set inicial
seed_set_inicial = ["cpd00001","cpd00009","cpd00011","cpd00013","cpd00020","cpd00021","cpd00024","cpd00029","cpd00032","cpd00034","cpd00036","cpd00040","cpd00047","cpd00057","cpd00067","cpd00106","cpd00130","cpd00139","cpd00149","cpd00180","cpd00205","cpd00239","cpd00242","cpd00254","cpd00260","cpd00308","cpd00331","cpd00830","cpd00971","cpd01078","cpd01194","cpd10515","cpd10516","cpd11574","cpd11608","cpd11609","cpd11610","cpd11614","cpd11616","cpd11625","cpd11632","cpd11640","cpd11848","cpd15574","cpd16654","cpd17287","cpd37270","cpd37272","cpd37275"]
# Cargar las reacciones desde el archivo
archivo_reacciones = "II. Base de datos KEGG version 2020 (anaerobica).xlsx"
reacciones = cargar_reacciones(archivo_reacciones)

# Ejecutar la expansin de red
expansion_red(seed_set_inicial, reacciones)
