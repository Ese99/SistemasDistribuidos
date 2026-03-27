import matplotlib.pyplot as plt
import csv
import os
import io
from collections import defaultdict

def graficar_tiempos_hardcoded():
    # Se han añadido los datos de N=1000 al final del string
    csv_data = """Metodo,Hilos,N,Tiempo(s)
poisson_serial,1,100,2.737648997
poisson_parallel_for,12,100,.505469839
poisson_critical,12,100,.512016342
poisson_atomic,12,100,.500770551
poisson_task,12,100,15.525832645
poisson_parallel_for,24,100,.438406597
poisson_critical,24,100,.436118024
poisson_atomic,24,100,.449617546
poisson_task,24,100,16.916983691
poisson_parallel_for,48,100,.589222806
poisson_critical,48,100,.594588312
poisson_atomic,48,100,.595306463
poisson_task,48,100,24.550679180
poisson_parallel_for,64,100,.832466947
poisson_critical,64,100,.821935051
poisson_atomic,64,100,.838251500
poisson_task,64,100,25.915233335
poisson_serial,1,250,88.602264807
poisson_parallel_for,12,250,10.581020420
poisson_critical,12,250,10.543512190
poisson_atomic,12,250,10.546040854
poisson_task,12,250,56.378928792
poisson_parallel_for,24,250,6.206897166
poisson_critical,24,250,6.216835519
poisson_atomic,24,250,6.303083373
poisson_task,24,250,90.235320938
poisson_parallel_for,48,250,5.225713142
poisson_critical,48,250,5.143553161
poisson_atomic,48,250,5.259835879
poisson_task,48,250,99.308026586
poisson_parallel_for,64,250,6.377108453
poisson_critical,64,250,6.400283866
poisson_atomic,64,250,6.197764303
poisson_task,64,250,145.167215368
poisson_serial,1,500,1174.406932885
poisson_parallel_for,12,500,127.125559222
poisson_critical,12,500,127.722884337
poisson_atomic,12,500,127.869620208
poisson_task,12,500,204.960369394
poisson_parallel_for,24,500,68.989365733
poisson_critical,24,500,69.557331807
poisson_atomic,24,500,69.009359336
poisson_task,24,500,215.552429837
poisson_parallel_for,48,500,42.904749823
poisson_critical,48,500,43.712492107
poisson_atomic,48,500,43.522225690
poisson_task,48,500,296.563848953
poisson_parallel_for,64,500,41.552824391
poisson_critical,64,500,42.663463365
poisson_atomic,64,500,42.678421490
poisson_task,64,500,607.532393938
poisson_serial,1,750,5233.619429388
poisson_parallel_for,12,750,561.133411600
poisson_critical,12,750,561.122293472
poisson_atomic,12,750,561.365895477
poisson_task,12,750,824.367793044
poisson_parallel_for,24,750,294.853068906
poisson_critical,24,750,295.549616902
poisson_atomic,24,750,295.646571502
poisson_task,24,750,552.540443583
poisson_parallel_for,48,750,174.093928135
poisson_critical,48,750,172.747399298
poisson_atomic,48,750,172.786560807
poisson_task,48,750,666.047250450
poisson_parallel_for,64,750,154.568766260
poisson_critical,64,750,154.216781987
poisson_atomic,64,750,158.354872225
poisson_task,64,750,1146.707521635
"""

    f = io.StringIO(csv_data.strip())
    datos = defaultdict(lambda: defaultdict(lambda: {'hilos': [], 'tiempos': []}))
    tiempos_serial = {}

    reader = csv.reader(f)
    next(reader) 
    
    for row in reader:
        if not row or len(row) < 4: continue
        metodo = row[0].strip()
        hilos = int(row[1].strip())
        n = int(row[2].strip())
        tiempo = float(row[3].strip())

        if metodo == "poisson_serial":
            tiempos_serial[n] = tiempo
        else:
            datos[n][metodo]['hilos'].append(hilos)
            datos[n][metodo]['tiempos'].append(tiempo)

    os.makedirs('imag', exist_ok=True)

    colores = {
        'poisson_parallel_for': 'teal', 
        'poisson_critical': 'darkred',
        'poisson_atomic': 'navy', 
        'poisson_task': 'darkorange'
    }
    marcadores = {
        'poisson_parallel_for': 'o', 
        'poisson_critical': 's',
        'poisson_atomic': '^', 
        'poisson_task': 'D'
    }

    for n, metodos in datos.items():
        plt.figure(figsize=(10, 6))

        for metodo, valores in metodos.items():
            if not valores['hilos']: continue
            hilos_ordenados, tiempos_ordenados = zip(*sorted(zip(valores['hilos'], valores['tiempos'])))
            
            plt.plot(hilos_ordenados, tiempos_ordenados, 
                     marker=marcadores.get(metodo, 'o'), 
                     linewidth=2.5, markersize=8,
                     label=metodo.replace('poisson_', ''), 
                     color=colores.get(metodo, 'black'))

        if n in tiempos_serial:
            plt.axhline(y=tiempos_serial[n], color='gray', linestyle='--', linewidth=2,
                        label=f'Serial Base ({tiempos_serial[n]:.3f} s)')

        plt.title(f'Rendimiento OpenMP - Malla {n}x{n}', fontsize=16, fontweight='bold', pad=15)
        plt.xlabel('Número de Hilos', fontsize=13)
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=13)
        
        todos_los_hilos = set()
        for v in metodos.values(): todos_los_hilos.update(v['hilos'])
        if todos_los_hilos:
            plt.xticks(sorted(list(todos_los_hilos)))

        # Ajuste para usar escala logarítmica en el eje Y para la malla masiva si es necesario,
        # pero la escala lineal mostrará mejor la brecha con el serial.
        
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)

        nombre_salida = f'imag/Rendimiento_Tiempos_N{n}.png'
        plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfica generada: {nombre_salida}")

if __name__ == "__main__":
    graficar_tiempos_hardcoded()