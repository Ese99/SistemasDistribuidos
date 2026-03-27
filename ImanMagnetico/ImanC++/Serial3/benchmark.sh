#!/bin/bash

# Tamaños de malla válidos y la cantidad fija de iteraciones que quieres probar (ej. 2000)
MALLAS=(125 250 500)
ITERACIONES=2000
LOG_FILE="Tiempos_Ejecucion.txt"

echo "Creando directorios..."
mkdir -p Resultados_SOR
mkdir -p Resultados_GS
mkdir -p Resultados_Jacobi

echo "Reporte de Tiempos" > $LOG_FILE
echo "==================" >> $LOG_FILE

echo "Compilando códigos..."
g++ -O3 Iman_SOR.cpp -o exec_SOR
g++ -O3 Iman_GS.cpp -o exec_GS
g++ -O3 Iman_Jacobi.cpp -o exec_Jacobi

TIMEFORMAT="%R segundos"

for malla in "${MALLAS[@]}"; do
    echo "----------------------------------------"
    echo "Ejecutando para Malla de $malla x $malla ($ITERACIONES iteraciones)..."
    
    echo "" >> $LOG_FILE
    echo "--- Malla: $malla x $malla ---" >> $LOG_FILE
    
    echo "-> Ejecutando SOR..."
    echo -n "SOR          : " >> $LOG_FILE
    { time ./exec_SOR $malla $ITERACIONES "SOR_M${malla}" ; } 2>> $LOG_FILE
    mv *_SOR_M${malla}.dat Resultados_SOR/
    
    echo "-> Ejecutando Gauss-Seidel..."
    echo -n "Gauss-Seidel : " >> $LOG_FILE
    { time ./exec_GS $malla $ITERACIONES "GS_M${malla}" ; } 2>> $LOG_FILE
    mv *_GS_M${malla}.dat Resultados_GS/
    
    echo "-> Ejecutando Jacobi..."
    echo -n "Jacobi       : " >> $LOG_FILE
    { time ./exec_Jacobi $malla $ITERACIONES "Jacobi_M${malla}" ; } 2>> $LOG_FILE
    mv *_Jacobi_M${malla}.dat Resultados_Jacobi/
done

echo "Benchmark completado."
rm exec_SOR exec_GS exec_Jacobi