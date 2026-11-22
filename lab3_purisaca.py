"""
Laboratorio N° 3 — Búsqueda informada: Greedy Best-First Search y A*
Inteligencia Artificial — UNMSM / FISI / E.P. Ingeniería de Software
Alumno: Purisaca Moquillaza, Joseph Francis — Código: 23200290

Implementa sobre la misma lista de adyacencia: BFS, DFS, costo uniforme,
Greedy Best-First Search y A* (con ponderación w), con métricas de
nodos expandidos, generados y tamaño máximo de la frontera.
Solo usa la biblioteca estándar (csv, heapq, collections) y matplotlib.
"""
import csv
import heapq
from collections import deque

# ═════════════════════════════════════════════════════════════════════
# PASO 1. Lectura de los datos (funciones de la plantilla, sin modificar)
# ═════════════════════════════════════════════════════════════════════

def leer_aristas(ruta):
    """Lee el CSV de tramos tal como viene (sin limpiar).
    Devuelve una lista de diccionarios con las claves origen, destino, distancia_km."""
    with open(ruta, newline='', encoding='utf-8') as f:
        return [dict(fila) for fila in csv.DictReader(f)]


def leer_heuristica(ruta):
    """Lee el CSV de heurística y devuelve {ciudad: h_km} (nombre sin espacios)."""
    H = {}
    with open(ruta, newline='', encoding='utf-8') as f:
        for fila in csv.DictReader(f):
            H[fila['ciudad'].strip()] = int(fila['h_km'])
    return H


# ═════════════════════════════════════════════════════════════════════
# PASO 2. Limpieza de los datos y construcción del grafo
# ═════════════════════════════════════════════════════════════════════

# Variantes de nombre -> nombre normalizado (clave en minúsculas)
ALIAS = {
    'nazca': 'Nasca',
}


def normalizar(nombre):
    """R1 + R2: quita espacios sobrantes y aplica el diccionario ALIAS."""
    nombre = nombre.strip()                       # R1
    return ALIAS.get(nombre.lower(), nombre)      # R2


def limpiar(filas):
    """TODO 2.1 — Aplica las reglas R1-R4 en orden y devuelve una lista de
    tuplas (origen, destino, distancia_km) con la distancia como entero."""
    aristas = []
    vistas = set()                                # R4: aristas ya registradas
    for fila in filas:
        origen = normalizar(fila['origen'])
        destino = normalizar(fila['destino'])
        # R3: descartar filas sin distancia válida
        valor = (fila.get('distancia_km') or '').strip()
        try:
            distancia = int(valor)
        except ValueError:
            continue
        # R4: A-B y B-A son la misma arista en un grafo no dirigido
        clave = frozenset({origen, destino})
        if clave in vistas:
            continue
        vistas.add(clave)
        aristas.append((origen, destino, distancia))
    return aristas


def construir_grafo(aristas):
    """TODO 2.2 — Lista de adyacencia {ciudad: [(vecino, costo), ...]}.
    Cada arista se inserta en ambos sentidos y los vecinos quedan en orden
    alfabético (necesario para que BFS/DFS sean reproducibles)."""
    G = {}
    for a, b, costo in aristas:
        G.setdefault(a, []).append((b, costo))
        G.setdefault(b, []).append((a, costo))
    for ciudad in G:
        G[ciudad].sort()
    return G


# ═════════════════════════════════════════════════════════════════════
# PASO 3. Verificación de la heurística
# ═════════════════════════════════════════════════════════════════════

def costos_optimos_a(G, meta):
    """h*(n): costo óptimo de cada ciudad hasta la meta (Dijkstra desde la meta;
    el grafo es no dirigido, así que equivale a Dijkstra hacia atrás)."""
    dist = {meta: 0}
    heap = [(0, meta)]
    cerrados = set()
    while heap:
        d, n = heapq.heappop(heap)
        if n in cerrados:
            continue
        cerrados.add(n)
        for vecino, costo in G[n]:
            nd = d + costo
            if nd < dist.get(vecino, float('inf')):
                dist[vecino] = nd
                heapq.heappush(heap, (nd, vecino))
    return dist


def verificar_heuristica(G, H, meta):
    """TODO 3.1 — Devuelve (no_admisibles, inconsistentes):
    - no_admisibles: ciudades con h(n) > h*(n)
    - inconsistentes: pares (n, m) con h(n) > c(n, m) + h(m), revisando cada
      arista en ambos sentidos."""
    h_estrella = costos_optimos_a(G, meta)
    no_admisibles = [n for n in sorted(G) if H[n] > h_estrella[n]]
    inconsistentes = []
    for n in sorted(G):
        for m, costo in G[n]:
            if H[n] > costo + H[m]:
                inconsistentes.append((n, m))
    return no_admisibles, inconsistentes


# ═════════════════════════════════════════════════════════════════════
# PASO 4. Instrumentación (clase de la plantilla)
# ═════════════════════════════════════════════════════════════════════

class Metricas:
    """Contadores con las definiciones de la Tabla 7 de la guía."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.expandidos = 0
        self.generados = 0
        self.frontera_max = 0

    def observar_frontera(self, tamano):
        """Llamar justo antes de cada extracción de la frontera."""
        self.frontera_max = max(self.frontera_max, tamano)

    def expandir(self):
        """Llamar al procesar un nodo (no para entradas obsoletas)."""
        self.expandidos += 1

    def generar(self):
        """Llamar cada vez que se inserta un nodo en la frontera."""
        self.generados += 1

    def fila(self, costo):
        """Fila para la tabla comparativa."""
        return {'algoritmo': self.nombre, 'costo': costo, 'expandidos': self.expandidos,
                'generados': self.generados, 'frontera_max': self.frontera_max}


def reconstruir(padre, meta):
    """Reconstruye el camino recorriendo el diccionario de padres desde la meta."""
    camino = []
    n = meta
    while n is not None:
        camino.append(n)
        n = padre[n]
    return camino[::-1]


def costo_camino(G, camino):
    """Suma de los costos de las aristas del camino."""
    total = 0
    for a, b in zip(camino, camino[1:]):
        total += dict(G[a])[b]
    return total


def imprimir_tabla(resultados):
    """Imprime la tabla comparativa de algoritmos."""
    print(f"{'Algoritmo':<18}{'Costo (km)':>12}{'Expandidos':>12}{'Generados':>11}{'Frontera máx.':>15}")
    print('-' * 68)
    for r in resultados:
        costo = f"{r['costo']:,}".replace(',', ' ') if r['costo'] is not None else '—'
        print(f"{r['algoritmo']:<18}{costo:>12}{r['expandidos']:>12}{r['generados']:>11}{r['frontera_max']:>15}")


# ═════════════════════════════════════════════════════════════════════
# PASO 5. Búsqueda no informada: BFS y DFS
# ═════════════════════════════════════════════════════════════════════

def bfs(G, inicio, meta):
    """TODO 5.1 — BFS con cola (deque). Los nodos se marcan como visitados al
    generarlos; la prueba de meta se hace al extraer."""
    m = Metricas('BFS')
    padre = {inicio: None}
    frontera = deque([inicio])
    visitados = {inicio}
    m.generar()
    while frontera:
        m.observar_frontera(len(frontera))
        n = frontera.popleft()
        m.expandir()
        if n == meta:
            camino = reconstruir(padre, meta)
            return camino, costo_camino(G, camino), m
        for vecino, _costo in G[n]:
            if vecino not in visitados:
                visitados.add(vecino)
                padre[vecino] = n
                m.generar()
                frontera.append(vecino)
    return None, None, m


def dfs(G, inicio, meta):
    """TODO 5.2 — DFS con pila explícita (lista), sin recursión. Los vecinos se
    apilan en orden alfabético inverso para desapilarse en orden alfabético.
    - Un vecino puede apilarse otra vez aunque ya esté en la pila: la copia más
      reciente es la que se desapila primero (comportamiento real de una pila),
      por eso se actualiza su padre.
    - Al desapilar un nodo ya expandido (copia obsoleta) se descarta sin contarlo."""
    m = Metricas('DFS')
    padre = {inicio: None}
    frontera = [inicio]
    cerrados = set()
    m.generar()
    while frontera:
        m.observar_frontera(len(frontera))
        n = frontera.pop()
        if n in cerrados:                  # copia obsoleta: no es expansión
            continue
        m.expandir()
        if n == meta:
            camino = reconstruir(padre, meta)
            return camino, costo_camino(G, camino), m
        cerrados.add(n)
        for vecino, _costo in reversed(G[n]):
            if vecino in cerrados:
                continue
            padre[vecino] = n
            m.generar()
            frontera.append(vecino)
    return None, None, m
