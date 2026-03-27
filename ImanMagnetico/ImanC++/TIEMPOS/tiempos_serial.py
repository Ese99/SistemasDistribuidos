import matplotlib.pyplot as plt
import os

# Datos estructurados desde tu benchmark (comas cambiadas a puntos para Python)
datos = {
    "Default_Sin_Flag": {
        "titulo": "Optimización: Default (Sin flag)",
        "mallas": [125, 250, 500, 1000, 1500, 2000],
        "SOR": [3.340, 13.700, 56.793, 229.821, 504.178, 888.883],
        "GS": [2.979, 11.971, 50.101, 202.532, 469.291, 819.974],
        "Jacobi": [2.965, 12.954, 51.883, 215.203, 453.586, 830.007]
    },
    "O0": {
        "titulo": "Optimización: -O0",
        "mallas": [125, 250, 500, 1000, 1500, 2000],
        "SOR": [3.325, 14.796, 55.448, 221.407, 498.987, 905.794],
        "GS": [2.977, 12.263, 51.711, 196.500, 458.653, 821.567],
        "Jacobi": [2.961, 13.170, 50.924, 198.837, 465.601, 821.004]
    },
    "O1": {
        "titulo": "Optimización: -O1",
        "mallas": [125, 250, 500, 1000, 1500, 2000],
        "SOR": [0.853, 3.479, 14.053, 56.666, 128.650, 227.974],
        "GS": [0.528, 2.134, 8.641, 34.694, 78.990, 140.530],
        "Jacobi": [0.526, 2.144, 8.656, 34.690, 79.075, 140.564]
    },
    "O2": {
        "titulo": "Optimización: -O2",
        "mallas": [125, 250, 500, 1000, 1500, 2000],
        "SOR": [0.856, 3.519, 14.183, 57.157, 129.387, 230.444],
        "GS": [0.530, 2.177, 8.753, 35.425, 80.365, 142.961],
        "Jacobi": [0.531, 2.176, 8.816, 35.248, 79.699, 142.416]
    },
    "O3": {
        "titulo": "Optimización: -O3",
        "mallas": [125, 250, 500, 1000, 1500, 2000],
        "SOR": [0.850, 3.499, 14.454, 57.136, 129.330, 230.158],
        "GS": [0.532, 2.167, 8.822, 35.489, 79.889, 142.114],
        "Jacobi": [0.532, 2.178, 8.752, 35.249, 79.840, 142.626]
    }
}

print("Generando gráficas de rendimiento...")
os.makedirs('images', exist_ok=True)

for clave, info in datos.items():
    mallas = info["mallas"]
    
    plt.figure(figsize=(10, 6))
    
    # Graficar las 3 líneas por cada método
    plt.plot(mallas, info["SOR"], marker='o', linewidth=2, markersize=6, color='darkred', label="SOR")
    plt.plot(mallas, info["GS"], marker='s', linewidth=2, markersize=6, color='teal', label="Gauss-Seidel")
    plt.plot(mallas, info["Jacobi"], marker='^', linewidth=2, markersize=6, color='navy', label="Jacobi")
    
    # Estilos
    plt.title(info["titulo"], fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Tamaño de la Malla (N x N)", fontsize=13)
    plt.ylabel("Tiempo de Ejecución (segundos)", fontsize=13)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # Guardar gráfica
    nombre_archivo = f"images/Rendimiento_{clave}.png"
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f" -> Creado: {nombre_archivo}")

print("¡Todas las gráficas han sido creadas exitosamente!")