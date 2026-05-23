import heapq

def construir_grafo(ruta_archivo):
    """
    Lee el archivo de texto y construye el grafo en formato de lista de adyacencia.
    Asume un grafo no dirigido.
    """
    grafo = {}
    
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split()
            
            if len(partes) == 3:
                origen = partes[0]
                destino = partes[1]
                peso = int(partes[2]) 
                
                if origen not in grafo:
                    grafo[origen] = []
                if destino not in grafo:
                    grafo[destino] = []
                    
                grafo[origen].append((destino, peso))
                grafo[destino].append((origen, peso))
                
    return grafo

def dijkstra(grafo, inicio, destino):
    """
    Calcula la ruta más corta entre un nodo de inicio y uno de destino 
    usando el algoritmo de Dijkstra con una cola de prioridad.
    """
    # Si alguno de los nodos no existe en el grafo, no hay ruta
    if inicio not in grafo or destino not in grafo:
        return float('inf'), []

    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    nodos_previos = {nodo: None for nodo in grafo}
    
    cola_prioridad = [(0, inicio)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual == destino:
            break
            
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual]:
            distancia_nueva = distancia_actual + peso
            
            if distancia_nueva < distancias[vecino]:
                distancias[vecino] = distancia_nueva
                nodos_previos[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia_nueva, vecino))
                
    # Reconstrucción de la ruta
    ruta_optima = []
    nodo_rastreo = destino
    
    while nodo_rastreo is not None:
        ruta_optima.insert(0, nodo_rastreo)
        nodo_rastreo = nodos_previos[nodo_rastreo]
        
    if ruta_optima[0] == inicio:
        return distancias[destino], ruta_optima
    else:
        return float('inf'), []

# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == '__main__':
    
    ruta_txt = 'ciudades_grafo.txt'
    print("Cargando grafo desde el archivo...")
    try:
        grafo_estaciones = construir_grafo(ruta_txt)
        print(f"¡Grafo cargado exitosamente! Total de nodos: {len(grafo_estaciones)}\n")

        origen = "N186" 
        destino = "N010"

        print(f"Calculando ruta más corta desde {origen} hasta {destino}...")
        distancia_total, ruta = dijkstra(grafo_estaciones, origen, destino)

        # Resultados
        if distancia_total != float('inf'):
            print("\nRUTA ENCONTRADA")
            print(f"Distancia total: {distancia_total} km")
            print(f"Recorrido: {' -> '.join(ruta)}")
        else:
            print("\nNo existe una ruta posible entre estas estaciones.")
            
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo '{ruta_txt}'. Asegúrate de que exista en el mismo directorio.")