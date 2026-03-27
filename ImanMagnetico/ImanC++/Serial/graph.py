import numpy as np
import matplotlib.pyplot as plt
import os

# Parámetros del benchmark
iteraciones = [200, 2000, 10000, 30000]
metodos = [
    ("SOR", "Resultados_SOR"), 
    ("GS", "Resultados_GS"), 
    ("Jacobi", "Resultados_Jacobi")
]

# Definición de las magnitudes a graficar con sus títulos formales
magnitudes = [
    ("POT-MAG", "Potencial Magnético Escalar $\Phi$"),
    ("CAMPO-H", "Campo Magnético $\mathbf{H}$"),
    ("CAMPO-B", "Inducción Magnética $\mathbf{B}$")
]

print("Generando 12 gráficas comparativas independientes...")

for it in iteraciones:
    for mag_archivo, mag_titulo in magnitudes:
        
        # Crear una figura horizontal (1 fila, 3 columnas)
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
        fig.suptitle(f"{mag_titulo} - {it} Iteraciones", fontsize=18, fontweight='bold', y=1.05)

        for col, (nombre_metodo, carpeta) in enumerate(metodos):
            archivo = f"{carpeta}/{mag_archivo}_{nombre_metodo}_{it}.dat"
            ax = axes[col]
            
            if os.path.exists(archivo):
                data = np.loadtxt(archivo)
                
                # Graficar Mapa de Calor si es el Potencial Magnético
                if mag_archivo == "POT-MAG":
                    cf = ax.tricontourf(data[:, 0], data[:, 1], data[:, 2], levels=50, cmap='magma')
                    if col == 2: # Barra de color solo al final
                        cbar = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
                        cbar.set_label("$\Phi$", rotation=0, labelpad=15)
                
                # Graficar Vectores si son los campos H o B
                else:
                    color_vec = 'teal' if mag_archivo == "CAMPO-H" else 'darkred'
                    ax.quiver(data[:, 0], data[:, 1], data[:, 2], data[:, 3], 
                              color=color_vec, pivot='middle', scale_units='xy')

                # Configuración estética de cada subgráfico
                ax.set_title(f"Método: {nombre_metodo}", fontsize=14)
                ax.set_aspect('equal')
                ax.set_xlabel("Eje X")
                if col == 0:
                    ax.set_ylabel("Eje Y")
            else:
                ax.set_title(f"Archivo no encontrado:\n{nombre_metodo}", fontsize=10, color='red')
                ax.axis('off')

        plt.tight_layout()
        
        # Guardar archivo con nombre descriptivo (ej. CAMPO-B_10000_iter.png)
        nombre_salida = f"{mag_archivo}_{it}_iter.png"
        plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f" -> Creado: {nombre_salida}")

print("Proceso completado exitosamente.")