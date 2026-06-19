import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load dataset
df = pd.read_csv(
    "dataset/household_power_consumption.txt",
    sep=";",
    low_memory=False
)

df["Global_active_power"] = pd.to_numeric(
    df["Global_active_power"],
    errors="coerce"
)

df = df.dropna()

data = df["Global_active_power"].values.reshape(-1,1)

scaler = MinMaxScaler()
data = scaler.fit_transform(data)

# Last 24 readings
last_24 = data[-24:]

X = np.array([last_24])

# Load model
model = load_model("model/demand_lstm.keras")

prediction = model.predict(X)

predicted_value = scaler.inverse_transform(prediction)

print("\nPredicted Future Demand:")
print(predicted_value[0][0], "kW")