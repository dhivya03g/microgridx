import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

print("Loading Dataset...")

df = pd.read_csv(
    "dataset/household_power_consumption.txt",
    sep=";",
    low_memory=False
)

# Convert power column
df["Global_active_power"] = pd.to_numeric(
    df["Global_active_power"],
    errors="coerce"
)

df = df.dropna()

print("Rows Loaded:", len(df))

# Use only power consumption
data = df["Global_active_power"].values

# Scale
scaler = MinMaxScaler()
data = scaler.fit_transform(
    data.reshape(-1, 1)
)

# Create sequences
X = []
y = []

window_size = 24

for i in range(window_size, len(data)):
    X.append(data[i-window_size:i])
    y.append(data[i])

X = np.array(X)
y = np.array(y)

print("Shape:", X.shape)

# Split data
split = int(len(X) * 0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

# Build LSTM
model = Sequential([
    LSTM(64, input_shape=(24,1)),
    Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse"
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

print("Training Started...")

model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=10,
    batch_size=128,
    callbacks=[early_stop]
)

model.save(
    "model/demand_lstm.keras"
)

print("Model Saved Successfully!")