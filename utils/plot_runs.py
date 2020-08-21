import os
import re

import matplotlib.pyplot as plt

times = []
# folder = "short_runs_v2"
folder = "medium_runs_v2"
folder = "large_runs"

for filename in sorted(os.listdir(folder)):
    with open(os.path.join(folder, filename)) as f:
        reg = re.compile(r"primitive calls\) in ([^ seconds]*)")
        for line in f:
            time = float(reg.findall(f.read())[0])
            times.append(time)

plt.title("100 simulations of standard game")
plt.xlabel("Commit")
plt.ylabel("Seconds")
plt.plot(list(range(len(times))), times)
plt.show()
