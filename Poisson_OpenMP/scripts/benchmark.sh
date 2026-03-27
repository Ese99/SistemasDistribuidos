#!/bin/bash

METODOS=("poisson_serial" "poisson_parallel_for" "poisson_critical" "poisson_atomic" "poisson_task")
TAMANOS=(50 250 500) # Para el clúster puedes cambiar a: (1000 2000 5000)
HILOS=(12 24 48 64)
LOG="benchmark_cluster_resultados.txt"

echo "Metodo,Hilos,N,Tiempo(s)" > $LOG

echo "Iniciando Benchmark Multihilo..."

# Limpiamos binarios previos
mkdir -p bin data imag
rm -f bin/*

for n in "${TAMANOS[@]}"; do
    echo "=========================================="
    echo "  Compilando para tamaño de Malla N=$n"
    echo "=========================================="
    
    # 1. Compilar todo con el nuevo tamaño inyectado por preprocesador
    for m in "${METODOS[@]}"; do
        g++ -std=c++17 -O3 -Wall -Wextra -fopenmp -Isrc -DVALOR_M=$n -DVALOR_N=$n "src/$m.cpp" -o "bin/$m"
    done

    # 2. Ejecutar variando el número de hilos
    for h in "${HILOS[@]}"; do
        export OMP_NUM_THREADS=$h
        echo "--- Probando con $h Hilos ---"
        
        for m in "${METODOS[@]}"; do
            # El método serial ignora OMP_NUM_THREADS, solo lo corremos 1 vez por tamaño
            if [[ "$m" == "poisson_serial" && "$h" != "${HILOS[0]}" ]]; then
                continue 
            fi

            echo -n "  Ejecutando $m ... "
            
            START=$(date +%s.%N)
            ./bin/$m
            END=$(date +%s.%N)
            
            DURACION=$(echo "$END - $START" | bc)
            echo "Hecho en $DURACION s"
            
            # Formato CSV final
            if [[ "$m" == "poisson_serial" ]]; then
                echo "$m,1,$n,$DURACION" >> $LOG
            else
                echo "$m,$h,$n,$DURACION" >> $LOG
            fi
        done
    done
done

echo "Benchmark completado. Revisa $LOG"