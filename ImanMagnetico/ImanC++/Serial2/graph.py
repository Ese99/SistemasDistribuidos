import numpy as np
import matplotlib.pyplot as plt
import os

# Tamaños de malla que ejecutaste en el benchmark
mallas = [125, 250, 500] 

metodos = [
    ("SOR", "Resultados_SOR"), 
    ("GS", "Resultados_GS"), 
    ("Jacobi", "Resultados_Jacobi")
]

# Magnitudes a graficar
magnitudes = [
    ("POT-MAG", "Potencial Magnético Escalar $\Phi$"),
    ("CAMPO-H", "Campo Magnético $\mathbf{H}$"),
    ("CAMPO-B", "Inducción Magnética $\mathbf{B}$")
]

print("Generando gráficas limpias para el escalamiento de malla...")

for m in mallas:
    for mag_archivo, mag_titulo in magnitudes:
        
        # Crear la figura (1 fila, 3 columnas)
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
        fig.suptitle(f"{mag_titulo} - Malla de {m}x{m}", fontsize=18, fontweight='bold', y=1.05)

        for col, (nombre_metodo, carpeta) in enumerate(metodos):
            # El nombre exacto que genera tu script de Bash
            archivo = f"{carpeta}/{mag_archivo}_{nombre_metodo}_M{m}.dat"
            ax = axes[col]
            
            if os.path.exists(archivo):
                try:
                    # Cargamos los datos ignorando líneas vacías
                    data = np.loadtxt(archivo)
                except Exception as e:
                    print(f"Error leyendo {archivo}: {e}")
                    continue
                
                if data.size == 0:
                    ax.set_title(f"Archivo vacío", fontsize=10)
                    ax.axis('off')
                    continue

                # 1. GRAFICAR POTENCIAL (Mapa de Calor)
                if mag_archivo == "POT-MAG":
                    cf = ax.tricontourf(data[:, 0], data[:, 1], data[:, 2], levels=50, cmap='magma')
                    if col == 2: 
                        cbar = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
                
                # 2. GRAFICAR CAMPOS VECTORIALES (H y B)
                else:
                    color_vec = 'teal' if mag_archivo == "CAMPO-H" else 'darkred'
                    # Usamos quiver puro para que auto-escale las flechas
                    ax.quiver(data[:, 0], data[:, 1], data[:, 2], data[:, 3], 
                              color=color_vec, pivot='middle')

                # Configuración estética
                ax.set_title(f"Método: {nombre_metodo}", fontsize=14)
                ax.set_aspect('equal')
                ax.set_xlabel("Nodos Eje X")
                if col == 0:
                    ax.set_ylabel("Nodos Eje Y")
            else:
                ax.set_title(f"No encontrado", fontsize=10)
                ax.axis('off')

        plt.tight_layout()
        nombre_salida = f"{mag_archivo}_M{m}.png"
        plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')
        plt.close()
        print(f" -> Guardado: {nombre_salida}")

print("Proceso completado.")