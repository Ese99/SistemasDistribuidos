#!/bin/bash

# Configuración de los parámetros
MALLAS=(125 250 500 1000 1500 2000)
ITERACIONES=10000
FLAGS=("" "-O0" "-O1" "-O2" "-O3") # Niveles de optimización
LOG_FILE="Tiempos_Benchmark_Final.txt"

# Crear carpetas de resultados para los archivos .dat finales
mkdir -p Resultados_SOR
mkdir -p Resultados_GS
mkdir -p Resultados_Jacobi

# Cabecera del reporte
echo "REPORT DE RENDIMIENTO Y OPTIMIZACIÓN - PROYECTO MAGNETISMO" > $LOG_FILE
echo "Samuel - Ejecución en Clúster" >> $LOG_FILE
echo "Iteraciones fijas: $ITERACIONES" >> $LOG_FILE
echo "==========================================================" >> $LOG_FILE

# Formato de tiempo: solo el valor real en segundos
TIMEFORMAT="%R"

for flag in "${FLAGS[@]}"; do
    # Nombre visual para el log (si está vacío es "Sin Bandera")
    FLAG_LABEL=$flag
    if [ -z "$flag" ]; then FLAG_LABEL="Default (Sin flag)"; fi
    
    echo "----------------------------------------------------------"
    echo "PROBANDO OPTIMIZACIÓN: $FLAG_LABEL"
    echo "----------------------------------------------------------"
    
    echo "" >> $LOG_FILE
    echo "##########################################################" >> $LOG_FILE
    echo "NIVEL DE OPTIMIZACIÓN: $FLAG_LABEL" >> $LOG_FILE
    echo "##########################################################" >> $LOG_FILE

    # 1. Compilación con la bandera actual
    echo "Compilando con $flag..."
    g++ $flag Iman_SOR.cpp -o exec_SOR
    g++ $flag Iman_GS.cpp -o exec_GS
    g++ $flag Iman_Jacobi.cpp -o exec_Jacobi

    for malla in "${MALLAS[@]}"; do
        echo "Ejecutando Malla ${malla}x${malla}..."
        
        echo "" >> $LOG_FILE
        echo "--- Malla: ${malla}x${malla} ---" >> $LOG_FILE
        
        # Ejecutar y medir SOR
        echo -n "SOR          : " >> $LOG_FILE
        T_SOR=$({ time ./exec_SOR $malla $ITERACIONES "SOR_M${malla}" ; } 2>&1)
        echo "$T_SOR segundos" >> $LOG_FILE
        mv *_SOR_M${malla}.dat Resultados_SOR/ 2>/dev/null

        # Ejecutar y medir Gauss-Seidel
        echo -n "Gauss-Seidel : " >> $LOG_FILE
        T_GS=$({ time ./exec_GS $malla $ITERACIONES "GS_M${malla}" ; } 2>&1)
        echo "$T_GS segundos" >> $LOG_FILE
        mv *_GS_M${malla}.dat Resultados_GS/ 2>/dev/null

        # Ejecutar y medir Jacobi
        echo -n "Jacobi       : " >> $LOG_FILE
        T_JACOBI=$({ time ./exec_Jacobi $malla $ITERACIONES "Jacobi_M${malla}" ; } 2>&1)
        echo "$T_JACOBI segundos" >> $LOG_FILE
        mv *_Jacobi_M${malla}.dat Resultados_Jacobi/ 2>/dev/null
    done
done

# Limpieza de binarios
rm exec_SOR exec_GS exec_Jacobi

echo "=========================================================="
echo "BENCHMARK COMPLETADO."
echo "Los tiempos de todas las banderas y mallas están en: $LOG_FILE"