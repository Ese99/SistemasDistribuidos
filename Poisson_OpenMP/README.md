# Proyecto de Paralelización con OpenMP — Ecuación de Poisson 2D

Este proyecto resuelve la ecuación de Poisson bidimensional mediante el método numérico de diferencias finitas. Se implementan y comparan múltiples estrategias de paralelización utilizando **C++**, la API **OpenMP** y **Python** para la visualización de resultados y análisis de rendimiento en clúster.

---

## 📁 Estructura del Proyecto

Taller_OpenMP_Poisson/
├── src/
│   ├── poisson_serial.cpp          # Código base sin paralelismo
│   ├── poisson_parallel_for.cpp    # Paralelización con collapse(2)
│   ├── poisson_critical.cpp        # Sincronización con sección crítica
│   ├── poisson_atomic.cpp          # Sincronización con operación atómica
│   ├── poisson_task.cpp            # Paralelización basada en tareas
│   └── utils.h                     # Cabecera matemática (condiciones y fuentes)
│
├── scripts/                        # Scripts de automatización y análisis
│   ├── benchmark.sh                # Orquesta la medición de tiempos multihilo
│   └── graficas.py                 # Genera superficies 3D analíticas vs numéricas
│
├── documents/                      # Documentación técnica (Doxygen + LaTeX)
│   └── Doxyfile                    # Archivo de configuración de Doxygen
│
├── data/                           # Resultados numéricos (.dat) generados (auto)
├── imag/                           # Gráficas de potencial y escalabilidad (auto)
├── bin/                            # Ejecutables binarios compilados (auto)
├── Makefile                        # Reglas de compilación y automatización
└── README.md                       # Este archivo

---

## ⚙️ Compilación

Compila todos los códigos fuente de la carpeta src/ e inyecta las directivas de OpenMP. Los ejecutables se alojarán en bin/:

make

o bien, explícitamente:

make all

Esto generará los cinco binarios correspondientes a cada estrategia de paralelización evaluada.

---

## ▶️ Ejecución y Benchmark

Ejecuta el entorno de pruebas automatizado que evalúa los códigos variando los tamaños de malla y el número de hilos. Los datos numéricos se guardarán en data/ y los tiempos en un archivo de log:

make run

*Nota: Este comando invoca internamente a scripts/benchmark.sh garantizando la creación previa de los directorios necesarios.*

---

## 📊 Visualización de Resultados

Para generar las comparativas gráficas en 3D de las superficies de potencial (analítica vs numérica) y las curvas de escalabilidad temporal:

make view

Esto ejecutará el script de Python encargado de procesar los archivos .dat y guardará los renders en formato .png dentro de la carpeta imag/.

---

## 🧹 Limpieza de Archivos

Para restaurar el repositorio a su estado original y limpiar el espacio de almacenamiento, elimina todos los binarios, datos pesados y renders generados:

make clean

Esto borra de forma segura el contenido de las carpetas:
bin/ data/ imag/ documents/doc_output/

---

## 📚 Documentación Técnica

Genera automáticamente la documentación técnica del código fuente utilizando Doxygen y compila el manual de referencia en PDF mediante LaTeX:

make docs

El flujo automatizado realizará lo siguiente:
1. Analiza el código con doxygen documents/Doxyfile.
2. Compila el código LaTeX resultante.
3. Exporta y abre el manual unificado en:
documents/Poisson_OpenMP.pdf

---

## 🧠 Requisitos del Sistema

- **Compilador:** g++ (con soporte para C++17 y OpenMP)
- **Herramientas:** make, bash, doxygen, pdflatex
- **Python 3 y Librerías:** matplotlib, numpy (Para la renderización de mallas 3D y análisis de datos)

---

## 🧾 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Puedes modificar y usar libremente el código con atribución adecuada.

---

© 2026 — Proyecto de Computación Paralela y Distribuida
Asignatura: Sistemas Distribuidos
Autores: Samuel Paredes y Mauricio Guevara