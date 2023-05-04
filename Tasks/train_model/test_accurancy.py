import json
from pathlib import Path
import matplotlib.pyplot as plt
file_path = Path(__file__).resolve().parent
with open(file_path/'model/0504.json', 'r') as f:
    history_dict = json.load(f)

plt.plot(history_dict["categorical_accuracy"],
         c="r", label="train_accuracy")
plt.plot(
    history_dict["val_categorical_accuracy"], c="b", label="test_accuracy")
plt.legend(loc="upper left")
plt.show()
