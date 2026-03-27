import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("CAMPO-B")

x = data[:,0]
y = data[:,1]
Bx = data[:,2]
By = data[:,3]

plt.figure(figsize=(8,8))
plt.quiver(x, y, Bx, By)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Campo Magnético B")

# Guardar imagen
plt.savefig("img_CAMPO-B.png", dpi=300, bbox_inches="tight")

plt.show()