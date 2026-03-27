import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("CAMPO-H")

x = data[:,0]
y = data[:,1]
Hx = data[:,2]
Hy = data[:,3]

plt.figure(figsize=(8,8))
plt.quiver(x, y, Hx, Hy)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Campo Magnético H")

# Guardar imagen
plt.savefig("img_CAMPO-H.png", dpi=300, bbox_inches="tight")

plt.show()