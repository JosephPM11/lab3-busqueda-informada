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
