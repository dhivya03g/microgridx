import numpy as np
from sklearn.linear_model import LinearRegression

# sample historical solar data (example)
days = np.array([1,2,3,4,5]).reshape(-1,1)
solar_output = np.array([400,420,390,450,470])

model = LinearRegression()
model.fit(days,solar_output)

def predict_solar():

    next_day = np.array([[6]])

    prediction = model.predict(next_day)

    return round(float(prediction[0]),2)