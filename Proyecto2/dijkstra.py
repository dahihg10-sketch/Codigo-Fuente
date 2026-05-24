import heapq
import itertools

def construir_grafo(ruta_archivo):
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

# --- PUNTO 1: RUTA MAS CORTA ---
def dijkstra(grafo, inicio, destino):
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
                
    ruta_optima = []
    nodo_rastreo = destino
    while nodo_rastreo is not None:
        ruta_optima.insert(0, nodo_rastreo)
        nodo_rastreo = nodos_previos[nodo_rastreo]
        
    if ruta_optima[0] == inicio:
        return distancias[destino], ruta_optima
    else:
        return float('inf'), []

# --- PUNTO 2: ARBOL DE EXPANSION MINIMA ---
def kruskal(grafo):
    aristas = []
    visitadas = set()
    for origen in grafo:
        for destino, peso in grafo[origen]:
            camino = tuple(sorted((origen, destino)))
            if camino not in visitadas:
                visitadas.add(camino)
                aristas.append((peso, origen, destino))

    aristas.sort()
    padre = {nodo: nodo for nodo in grafo}

    def encontrar(nodo):
        if padre[nodo] == nodo:
            return nodo
        padre[nodo] = encontrar(padre[nodo])
        return padre[nodo]

    def unir(nodo1, nodo2):
        raiz1 = encontrar(nodo1)
        raiz2 = encontrar(nodo2)
        if raiz1 != raiz2:
            padre[raiz1] = raiz2
            return True
        return False

    mst = []
    peso_total = 0

    for peso, origen, destino in aristas:
        if unir(origen, destino):
            mst.append((origen, destino, peso))
            peso_total += peso

    return mst, peso_total

# --- PUNTO 3: TSP ---
def tsp_optimo(grafo, nodos_tsp):
    inicio = nodos_tsp[0]
    nodos_a_visitar = nodos_tsp[1:]
    mejor_ruta = []
    menor_distancia = float('inf')

    for permutacion in itertools.permutations(nodos_a_visitar):
        ruta_actual = [inicio] + list(permutacion) + [inicio]
        distancia_actual = 0
        es_valida = True

        for i in range(len(ruta_actual) - 1):
            nodo_origen = ruta_actual[i]
            nodo_destino = ruta_actual[i+1]
            dist_tramo, _ = dijkstra(grafo, nodo_origen, nodo_destino)
            
            if dist_tramo == float('inf'):
                es_valida = False
                break
            distancia_actual += dist_tramo

        if es_valida and distancia_actual < menor_distancia:
            menor_distancia = distancia_actual
            mejor_ruta = ruta_actual

    return mejor_ruta, menor_distancia


if __name__ == '__main__':
    ruta_txt = 'ciudades_grafo.txt' 
    grafo_estaciones = construir_grafo(ruta_txt)
    
    print("\n" + "="*40)
    print("1. RUTA MÁS CORTA (DIJKSTRA)")
    print("="*40)
    origen = "N186" 
    destino = "N010"
    distancia_total, ruta = dijkstra(grafo_estaciones, origen, destino)
    if distancia_total != float('inf'):
        print(f"Ruta encontrada: {' -> '.join(ruta)}")
        print(f"Distancia total: {distancia_total} km")
    else:
        print("No hay ruta.")

    print("\n" + "="*40)
    print("2. ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("="*40)
    aristas_mst, peso_mst = kruskal(grafo_estaciones)
    for origen_mst, destino_mst, peso in aristas_mst[:5]:
        print(f"Arista: {origen_mst} - {destino_mst} | Peso: {peso} km")
    print(f"... (mostrando solo 5 de las {len(aristas_mst)} aristas para no saturar la pantalla)")
    print(f"PESO TOTAL DEL ÁRBOL: {peso_mst} km")

    print("\n" + "="*40)
    print("3. RUTA ÓPTIMA TSP")
    print("="*40)
    nodos_para_tsp = ["N001", "N003", "N005", "N007", "N009"] 
    ruta_tsp, dist_tsp = tsp_optimo(grafo_estaciones, nodos_para_tsp)
    print(f"Subconjunto a visitar: {nodos_para_tsp}")
    print(f"Orden de visita: {' -> '.join(ruta_tsp)}")
    print(f"Distancia total del recorrido: {dist_tsp} km")
    print("\n")