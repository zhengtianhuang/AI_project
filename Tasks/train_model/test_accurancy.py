import json
from pathlib import Path
import matplotlib.pyplot as plt

file_path = Path(__file__).resolve().parent
with open(file_path/'model/0504.json', 'r') as f:
    history_dict = json.load(f)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))

ax1.plot(history_dict["acc"], c="r", label="train_accuracy")
ax1.plot(history_dict["val_acc"],
         c="b", label="test_accuracy")
ax1.legend(loc="upper left")

ax2.plot(history_dict["loss"], c="g", label="loss")
ax2.legend(loc="upper left")

plt.show()
