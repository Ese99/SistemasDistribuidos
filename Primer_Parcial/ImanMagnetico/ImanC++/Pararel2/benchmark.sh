#!/bin/bash

MALLAS=(125 250 500 1000 1500 2000 5000 10000 20000)
HILOS=(12 24 48 64)
ITERACIONES=10000
LOG_FILE="Tiempos_Ejecucion_OpenMP.txt"

mkdir -p Resultados_SOR Resultados_GS Resultados_Jacobi

echo "REPORTE DE TIEMPOS OPENMP - Samuel" > $LOG_FILE
echo "==================================" >> $LOG_FILE

# Compilación crítica con -fopenmp
echo "Compilando códigos con OpenMP y O3..."
g++ -O3 -fopenmp Iman_SOR.cpp -o exec_SOR
g++ -O3 -fopenmp Iman_GS.cpp -o exec_GS
g++ -O3 -fopenmp Iman_Jacobi.cpp -o exec_Jacobi

TIMEFORMAT="%R"

for malla in "${MALLAS[@]}"; do
    echo "----------------------------------------"
    echo "Procesando Malla $malla x $malla..."
    echo "" >> $LOG_FILE
    echo "--- Malla: $malla x $malla ---" >> $LOG_FILE

    for h in "${HILOS[@]}"; do
        echo " -> Ejecutando con $h hilos..."
        echo -n "Threads $h | " >> $LOG_FILE
        
        # Ejecución y medición
        echo -n "SOR: " >> $LOG_FILE
        T_SOR=$({ time ./exec_SOR $malla $ITERACIONES $h "SOR_M${malla}" ; } 2>&1)
        echo -n "$T_SOR s | " >> $LOG_FILE
        
        echo -n "GS: " >> $LOG_FILE
        T_GS=$({ time ./exec_GS $malla $ITERACIONES $h "GS_M${malla}" ; } 2>&1)
        echo -n "$T_GS s | " >> $LOG_FILE
        
        echo -n "Jacobi: " >> $LOG_FILE
        T_JAC=$({ time ./exec_Jacobi $malla $ITERACIONES $h "Jacobi_M${malla}" ; } 2>&1)
        echo "$T_JAC s" >> $LOG_FILE

        # Gestión de archivos: Solo guardamos los de 64 hilos
        if [ "$h" -eq 64 ]; then
            mv POT-MAG_SOR_M${malla}.dat Resultados_SOR/ 2>/dev/null
            mv CAMPO-H_SOR_M${malla}.dat Resultados_SOR/ 2>/dev/null
            mv CAMPO-B_SOR_M${malla}.dat Resultados_SOR/ 2>/dev/null
            
            mv POT-MAG_GS_M${malla}.dat Resultados_GS/ 2>/dev/null
            mv CAMPO-H_GS_M${malla}.dat Resultados_GS/ 2>/dev/null
            mv CAMPO-B_GS_M${malla}.dat Resultados_GS/ 2>/dev/null
            
            mv POT-MAG_Jacobi_M${malla}.dat Resultados_Jacobi/ 2>/dev/null
            mv CAMPO-H_Jacobi_M${malla}.dat Resultados_Jacobi/ 2>/dev/null
            mv CAMPO-B_Jacobi_M${malla}.dat Resultados_Jacobi/ 2>/dev/null
        else
            rm *.dat 2>/dev/null
        fi
    done
done

rm exec_SOR exec_GS exec_Jacobi
echo "Benchmark finalizado. Revisa $LOG_FILE."