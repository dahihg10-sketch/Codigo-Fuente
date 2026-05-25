import heapq # Librería para usar la Cola de Prioridad en Dijkstra
import itertools # Librería para generar las permutaciones en el TSP
# BLOQUE 1:Construccion del grafo
def construirGrafo(rutaArchivo):
    # Se hace nuestra estructura de datos principal una Lista de Adyacencia usando un diccionario de Python
    grafo = {}
    with open(rutaArchivo, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split() # .strip() limpia texto invisible (saltos de línea), .split() divide por los espacios
            if len(partes) == 3:
                origen = partes[0]
                destino = partes[1]
                peso = int(partes[2])
                if origen not in grafo:
                    grafo[origen] = []
                if destino not in grafo:
                    grafo[destino] = []
                # Se usa el método .append() dos veces por cada línea que lee el archivo
                # primero conectamos el origen con el destino, y luego el destino de vuelta con el origen
                # Esto es lo que define matemáticamente a un grafo no dirigido
                grafo[origen].append((destino, peso))
                grafo[destino].append((origen, peso))
    return grafo
# BLOQUE 2: Ruta mas corta
def dijkstra(grafo, inicio, destino):
    # si una de las ciudades no está en el mapa, no hay ruta posible
    if inicio not in grafo or destino not in grafo:
        return float('inf'), []
    # Iniciamos todas las distancias conocidas
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    # Diccionario nodosPrevios para rastrear el camino de regreso. Cada vez que Dijkstra
    # encuentra un camino más corto hacia una estación, aquí se anota de dónde venía
    nodosPrevios = {nodo: None for nodo in grafo}
    # Creamos la Cola de Prioridad en 3 partes
    colaPrioridad = [(0, inicio)]
    while colaPrioridad:
        distanciaActual, nodoActual = heapq.heappop(colaPrioridad)
        # Si ya llegamos al destino, se detiene la búsqueda
        if nodoActual == destino:
            break
        # Ignoramos caminos guardados en la cola que ya son viejos o más largos que el mejor registrado
        if distanciaActual > distancias[nodoActual]:
            continue
        for vecino, peso in grafo[nodoActual]:
            distanciaNueva = distanciaActual + peso
            # Si descubrimos que pasar por este camino ofrece una 'distanciaNueva' menor a la
            # que teníamos registrada previamente para ese vecino pasa lo siguiente
            if distanciaNueva < distancias[vecino]:
                distancias[vecino] = distanciaNueva # Actualizamos nuestro nuevo peso en las distancias
                nodosPrevios[vecino] = nodoActual # Actualizamos de dónde veníamos para poder reconstruir el camino
                # Metemos este vecino a la fila para seguir explorando desde ahí
                heapq.heappush(colaPrioridad, (distanciaNueva, vecino))
    rutaOptima = []
    nodoRastreo = destino
    while nodoRastreo is not None:
        rutaOptima.insert(0, nodoRastreo)
        nodoRastreo = nodosPrevios[nodoRastreo]
    if rutaOptima[0] == inicio:
        return distancias[destino], rutaOptima
    else:
        return float('inf'), []
# BLOQUE 3: Kruskal, Arbol de expancion minima
def kruskal(grafo):
    aristas = []
    visitadas = set()
    # Extraemos las carreteras únicas para no duplicar datos
    for origen in grafo:
        for destino, peso in grafo[origen]:
            camino = tuple(sorted((origen, destino)))
            if camino not in visitadas:
                visitadas.add(camino)
                aristas.append((peso, origen, destino))
    # .sort para ordenar las carreteras del mapa de la más barata a la más cara
    aristas.sort()
    padre = {nodo: nodo for nodo in grafo}
    def encontrar(nodo):
        if padre[nodo] == nodo:
            return nodo
        padre[nodo] = encontrar(padre[nodo])
        return padre[nodo]
    # Esta función conecta nodos
    def unir(nodo1, nodo2):
        raiz1 = encontrar(nodo1)
        raiz2 = encontrar(nodo2)
        # Si pertenecen a grupos distintos, los unimos y devuelve True
        if raiz1 != raiz2:
            padre[raiz1] = raiz2
            return True
        # Si tienen la misma raíz, significa que las dos ciudades ya estaban conectadas
        # de forma indirecta por otras vías y devuelve False y la carretera se descarta
        return False
    mst = []
    pesoTotal = 0
    # El bucle for evalúa cada carretera en orden de menor a mayor distancia.
    for peso, origen, destino in aristas:
        if unir(origen, destino): # Si al unirlas no formamos un bucle
            mst.append((origen, destino, peso)) # Se agrega a nuestro Árbol de Expansión Mínima
            pesoTotal += peso # Sumamos los kilómetros al costo total
    return mst, pesoTotal
# BLOQUE 4: TSP
def tspOptimo(grafo, nodosTsp):
    inicio = nodosTsp[0] # El primer elemento será nuestra estación de inicio y regreso
    nodosAVisitar = nodosTsp[1:] # El resto son las paradas obligatorias
    mejorRuta = []
    menorDistancia = float('inf')
    # Para resolver el Problema del Viajante de Comercio, usamos la función
    # itertools.permutations. Como nuestro objetivo es visitar un subconjunto de paradas,
    # esta instrucción genera de forma matemática todas las secuencias y combinaciones de orden posibles
    for permutacion in itertools.permutations(nodosAVisitar):
        # cuando lo creamos lo ponemos para que inicie en 'incio' y termine igual ahi
        rutaActual = [inicio] + list(permutacion) + [inicio]
        distanciaActual = 0
        esValida = True
        # Calculamos la distancia total de este itinerario específico tramo por tramo
        for i in range(len(rutaActual) - 1):
            nodoOrigen = rutaActual[i]
            nodoDestino = rutaActual[i+1]
            # reutiliza la función de Dijkstra
            distTramo, _ = dijkstra(grafo, nodoOrigen, nodoDestino)
            if distTramo == float('inf'):
                esValida = False
                break
            distanciaActual += distTramo
        # El programa mide el costo de cada combinación y se queda con la ruta
        # que arrojó el menor costo
        if esValida and distanciaActual < menorDistancia:
            menorDistancia = distanciaActual
            mejorRuta = rutaActual
    return mejorRuta, menorDistancia
# BLOQUE 5: Ejecucion
if __name__ == '__main__':
    rutaTxt = 'ciudades_grafo.txt'
    grafoEstaciones = construirGrafo(rutaTxt)
    print("\n")
    print("1. RUTA MÁS CORTA (DIJKSTRA)")
    print("\n")
    origenTest = "N186"
    destinoTest = "N010"
    distanciaTotal, ruta = dijkstra(grafoEstaciones, origenTest, destinoTest)
    if distanciaTotal != float('inf'):
        print(f"Ruta encontrada: {' -> '.join(ruta)}")
        print(f"Distancia total: {distanciaTotal} km")
    else:
        print("No hay ruta.")
    print("\n")
    print("2. ÁRBOL DE EXPANSIÓN MÍNIMA")
    print("\n")
    aristasMst, pesoMst = kruskal(grafoEstaciones)
    for origenMst, destinoMst, peso in aristasMst[:5]:
        print(f"Arista: {origenMst} - {destinoMst} | Peso: {peso} km")
    print(f"(mostrando solo 5 de las {len(aristasMst)})")
    print(f"PESO TOTAL DEL ÁRBOL: {pesoMst} km")
    print("\n")
    print("3. RUTA ÓPTIMA TSP")
    print("\n")
    nodosParaTsp = ["N001", "N003", "N005", "N007", "N009"]
    rutaTsp, distTsp = tspOptimo(grafoEstaciones, nodosParaTsp)
    print(f"Subconjunto a visitar: {nodosParaTsp}")
    print(f"Orden de visita: {' -> '.join(rutaTsp)}")
    print(f"Distancia total del recorrido: {distTsp} km")
    print("\n")