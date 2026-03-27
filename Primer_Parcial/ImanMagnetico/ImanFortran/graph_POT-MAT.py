import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("POT-MAG")

x = data[:,0]
y = data[:,1]
phi = data[:,2]

plt.figure()
contour = plt.tricontourf(x, y, phi, levels=50)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Potencial Magnético")
plt.colorbar(contour)

# Guardar imagen
plt.savefig("img_POT-MAG.png", dpi=300, bbox_inches="tight")

plt.show()