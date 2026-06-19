import numpy as np
import matplotlib.pyplot as plt

# Sample values (replace later with real predictions)
actual = [0.82, 0.85, 0.88, 0.90, 0.87, 0.92, 0.95]
predicted = [0.80, 0.84, 0.86, 0.91, 0.89, 0.93, 0.94]

plt.figure(figsize=(8,5))
plt.plot(actual, label="Actual Demand")
plt.plot(predicted, label="Predicted Demand")

plt.title("Actual vs Predicted Demand")
plt.xlabel("Time")
plt.ylabel("Power (kW)")
plt.legend()

plt.savefig("actual_vs_predicted.png")
print("Graph Saved Successfully!")