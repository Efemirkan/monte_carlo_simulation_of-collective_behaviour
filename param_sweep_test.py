import a as ef
import numpy as np

means = np.linspace(4, 6, num=11)

returned = []
for m in means:
    returned.append(ef.runIt(m))

print(returned)