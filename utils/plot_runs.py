import re
from pathlib import Path

import matplotlib.pyplot as plt

times = []
# folder = "short_runs_v2"
folder = "medium_runs_v2"
folder = "large_runs"

for filename in sorted(Path(folder).glob("*")):
    with open(filename, encoding="utf-8") as f:
        reg = re.compile(r"primitive calls\) in ([^ seconds]*)")
        for _ in f:
            time = float(reg.findall(f.read())[0])
            times.append(time)

plt.title("100 simulations of standard game")
plt.xlabel("Commit")
plt.ylabel("Seconds")
plt.plot(list(range(len(times))), times)
plt.show()
