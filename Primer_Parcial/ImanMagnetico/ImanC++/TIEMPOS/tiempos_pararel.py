import matplotlib.pyplot as plt
import os

# Datos de rendimiento extraídos del clúster (comas convertidas a puntos)
datos = {
    125: {
        "hilos": [12, 24, 48, 64],
        "SOR": [0.181, 0.215, 0.334, 0.404],
        "GS": [0.177, 0.214, 0.336, 0.424],
        "Jacobi": [0.174, 0.215, 0.345, 0.414]
    },
    250: {
        "hilos": [12, 24, 48, 64],
        "SOR": [0.461, 0.435, 0.550, 0.711],
        "GS": [0.438, 0.415, 0.589, 0.701],
        "Jacobi": [0.432, 0.418, 0.562, 0.703]
    },
    500: {
        "hilos": [12, 24, 48, 64],
        "SOR": [1.518, 1.280, 1.342, 1.554],
        "GS": [1.384, 1.205, 1.327, 1.627],
        "Jacobi": [1.403, 1.227, 1.336, 1.533]
    },
    1000: {
        "hilos": [12, 24, 48, 64],
        "SOR": [5.836, 3.729, 3.403, 3.615],
        "GS": [4.421, 3.464, 3.248, 3.804],
        "Jacobi": [4.417, 3.446, 3.234, 3.433]
    },
    1500: {
        "hilos": [12, 24, 48, 64],
        "SOR": [10.860, 7.863, 6.988, 7.596],
        "GS": [9.825, 7.355, 6.636, 7.181],
        "Jacobi": [9.815, 7.387, 6.584, 6.957]
    },
    2000: {
        "hilos": [12, 24, 48, 64],
        "SOR": [19.243, 13.769, 11.919, 12.612],
        "GS": [17.372, 12.784, 11.183, 11.997],
        "Jacobi": [17.300, 12.729, 11.295, 12.043]
    }
}

print("Generando gráficas de escalabilidad multihilo (OpenMP)...")
os.makedirs('images', exist_ok=True)

for malla, info in datos.items():
    plt.figure(figsize=(8, 5))
    
    # Graficar líneas
    plt.plot(info["hilos"], info["SOR"], marker='o', linewidth=2.5, markersize=8, color='darkred', label="SOR")
    plt.plot(info["hilos"], info["GS"], marker='s', linewidth=2.5, markersize=8, color='teal', label="Gauss-Seidel")
    plt.plot(info["hilos"], info["Jacobi"], marker='^', linewidth=2.5, markersize=8, color='navy', label="Jacobi")
    
    # Estilos y etiquetas
    plt.title(f"Escalabilidad OpenMP - Malla {malla}x{malla}", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("Número de Hilos", fontsize=13)
    plt.ylabel("Tiempo de Ejecución (segundos)", fontsize=13)
    
    # Forzar que el eje X solo muestre los hilos exactos que usamos
    plt.xticks(info["hilos"])
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    
    # Guardar gráfica
    nombre_archivo = f"images/Rendimiento_OpenMP_M{malla}.png"
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f" -> Creado: {nombre_archivo}")

print("¡Todas las gráficas han sido creadas exitosamente!")