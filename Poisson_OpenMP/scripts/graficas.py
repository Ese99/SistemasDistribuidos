import os
import numpy as np
import matplotlib.pyplot as plt
import glob

# Diccionario de soluciones analíticas según el ejemplo
def sol_analitica(ex, x, y):
    if ex == 1: return np.exp(x * y)
    if ex == 2: return np.log(x**2 + y**2)
    if ex == 3: return (x - y)**2
    if ex == 4: return x * y * np.log(x * y)
    return x*0

def plot_comparative_3d(filename, output_name):
    try:
        data = np.loadtxt(filename)
        if data.size == 0: return
        
        # Identificar qué ejemplo es leyendo el nombre del archivo ("_Ej1.dat", etc.)
        ex_num = 1
        for i in range(1, 5):
            if f"Ej{i}" in filename: ex_num = i
            
        x = data[:, 0]; y = data[:, 1]; z = data[:, 2]
        M = len(np.unique(x)); N = len(np.unique(y))
        X = x.reshape((M, N)); Y = y.reshape((M, N)); Z_num = z.reshape((M, N))

        # Generar superficie analítica exacta
        Z_ana = sol_analitica(ex_num, X, Y)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Malla negra para la solución analítica
        ax.plot_wireframe(X, Y, Z_ana, color='black', label='Solución analítica', linewidth=1)
        
        # Puntos/Superficie roja para la solución numérica
        ax.scatter(X, Y, Z_num, color='red', s=5, label='Solución numérica', alpha=0.8)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Potencial')
        ax.set_title(f'Ecuación de Poisson - Ejemplo {ex_num}')
        ax.legend()

        plt.savefig(output_name, dpi=300)
        plt.close()
        print(f"Gráfica guardada: {output_name}")
    except Exception as e:
        print(f"Error procesando {filename}: {e}")

if __name__ == '__main__':
    os.makedirs('imag', exist_ok=True)
    archivos = glob.glob('data/*.dat')
    for arc in archivos:
        salida = os.path.join('imag', os.path.basename(arc).replace('.dat', '.png'))
        plot_comparative_3d(arc, salida)