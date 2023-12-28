import matplotlib.pyplot as plt
from probs import Normal, Uniform

u = Normal(mu=1.5, sigma=0.3)
u.plot()
v = Normal(mu=-0.7)
(u + v).plot()
plt.show()

u = Uniform(a=2, b=3)
u.plot()
v = Uniform()
(u + v).plot()
plt.show()
