#!/bin/bash

# Arreglo de iteraciones (4 etapas clave de convergencia)
ITERACIONES=(200 2000 10000 30000)
LOG_FILE="Tiempos_Ejecucion.txt"

# 1. Crear directorios para los resultados
echo "Creando directorios..."
mkdir -p Resultados_SOR
mkdir -p Resultados_GS
mkdir -p Resultados_Jacobi

# Formato limpio para el archivo de texto
echo "Reporte de Tiempos de Ejecución - Benchmark Magnético" > $LOG_FILE
echo "====================================================" >> $LOG_FILE

# 2. Compilar los archivos C++ con banderas de optimización máxima
echo "Compilando códigos (-O3)..."
g++ -O3 Iman_SOR.cpp -o exec_SOR
g++ -O3 Iman_GS.cpp -o exec_GS
g++ -O3 Iman_Jacobi.cpp -o exec_Jacobi

if [ $? -ne 0 ]; then
    echo "Error en la compilación. Verifica tus archivos C++."
    exit 1
fi

# Configurar el formato del comando 'time' de Bash (solo segundos)
TIMEFORMAT="%R segundos"

# 3. Ejecutar benchmark
echo "Iniciando benchmark..."

for iter in "${ITERACIONES[@]}"; do
    echo "----------------------------------------"
    echo "Ejecutando para $iter iteraciones..."
    
    echo "" >> $LOG_FILE
    echo "--- $iter Iteraciones ---" >> $LOG_FILE
    
    # Ejecutar SOR
    echo "-> Ejecutando SOR..."
    echo -n "SOR          : " >> $LOG_FILE
    { time ./exec_SOR $iter "SOR_${iter}" ; } 2>> $LOG_FILE
    mv *_SOR_${iter}.dat Resultados_SOR/
    
    # Ejecutar Gauss-Seidel
    echo "-> Ejecutando Gauss-Seidel..."
    echo -n "Gauss-Seidel : " >> $LOG_FILE
    { time ./exec_GS $iter "GS_${iter}" ; } 2>> $LOG_FILE
    mv *_GS_${iter}.dat Resultados_GS/
    
    # Ejecutar Jacobi
    echo "-> Ejecutando Jacobi..."
    echo -n "Jacobi       : " >> $LOG_FILE
    { time ./exec_Jacobi $iter "Jacobi_${iter}" ; } 2>> $LOG_FILE
    mv *_Jacobi_${iter}.dat Resultados_Jacobi/
done

echo "----------------------------------------"
echo "Benchmark completado. Revisa el archivo $LOG_FILE."

# Limpiar binarios
rm exec_SOR exec_GS exec_Jacobi