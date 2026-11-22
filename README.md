# Laboratorio N° 3 – Búsqueda informada: Greedy Best-First Search y A*

**Curso:** Inteligencia Artificial – UNMSM, FISI  
**Alumno:** Joseph Francis Purisaca Moquillaza (23200290)  
**Docente:** Prof. Juan Gamarra Moreno

Planificación de rutas sobre la red vial del sur del Perú (Cusco → Lima) y su extensión al norte
(Cusco → Trujillo), comparando BFS, DFS, costo uniforme, Greedy Best-First Search, A* y A* ponderado.

## Estructura

```
lab3-busqueda-informada/
├── datos/
│   ├── rutas_peru_sur.csv          (con los 4 errores intencionales de la guía)
│   ├── rutas_peru_norte.csv
│   ├── heuristica_lima.csv
│   └── heuristica_trujillo.csv
├── lab3_purisaca.py                (plantilla completada: limpieza, grafo, heurística y algoritmos)
├── LabSem03_Purisaca_Moquillaza.ipynb   (notebook ejecutado, pasos 1–11 y actividad propuesta)
├── figuras/
│   ├── ponderado.png               (paso 10)
│   └── ponderado_trujillo.png      (actividad, T4)
├── informe.pdf
└── README.md
```

## Requisitos

- Python 3.10 o superior
- Biblioteca estándar: `csv`, `heapq`, `collections`
- `matplotlib` (solo para las gráficas) y `jupyter` para abrir el notebook

```bash
pip install matplotlib jupyter
```

## Ejecución

Todos los comandos se ejecutan **desde esta carpeta** (las rutas `datos/...` son relativas).

1. **Notebook completo** (recomendado):
   ```bash
   jupyter notebook LabSem03_Purisaca_Moquillaza.ipynb
   ```
   Luego, en el menú, *Kernel → Restart & Run All*. También puede ejecutarse sin abrirlo:
   ```bash
   jupyter nbconvert --to notebook --execute --inplace LabSem03_Purisaca_Moquillaza.ipynb
   ```
2. **Solo el módulo** (imprime las tablas comparativas de ambos problemas):
   ```bash
   python lab3_purisaca.py
   ```

## Resultados esperados

| Problema | Algoritmo | Costo (km) | Expandidos | Generados | Frontera máx. |
|---|---|---|---|---|---|
| Cusco → Lima | BFS | 1173 | 13 | 13 | 3 |
| | DFS | 1297 | 8 | 10 | 3 |
| | Costo uniforme | 1173 | 13 | 13 | 3 |
| | Greedy | 1180 | 8 | 10 | 3 |
| | A* | 1173 | 12 | 13 | 3 |
| Cusco → Trujillo | BFS | 1738 | 18 | 18 | 3 |
| | DFS | 1862 | 12 | 17 | 6 |
| | Costo uniforme | 1738 | 18 | 18 | 3 |
| | Greedy | 1862 | 12 | 16 | 5 |
| | A* | 1738 | 17 | 19 | 3 |

Coinciden con las Tablas 8 y 11 de la guía. La limpieza da 14 aristas y 13 ciudades, y ambas
heurísticas son admisibles y consistentes.

## Notas

- Los CSV se reconstruyeron a partir del contenido publicado en la guía (secciones 3.1–3.3 y Anexo A).
- En DFS un vecino puede volver a apilarse aunque ya esté en la pila, y las copias de nodos ya
  expandidos se descartan sin contarlas como expansión. Esta convención reproduce la Tabla 11.
- La declaración de uso de IA está al final de `informe.pdf`.
