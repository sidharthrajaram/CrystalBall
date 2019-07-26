import pandas as pd
import numpy as np
import time

from team_scraper import getTeamStats
from basic import getTeamMetric

FORECAST_FILE = 'data/test.csv'
teams_df = pd.read_csv(FORECAST_FILE)

X = np.array(teams_df.iloc[:,23:28])
Y = np.array(teams_df['WINS'])

def predict(X, W):
    return np.dot(X, W.T)

# w0, w1, w2, w3, w4
W = np.zeros(X.shape[1])

epochs = 100000
l_rate = 0.065
m = X.shape[0]

print(X.shape[0])
print(X.shape[1])
print()

for epoch in range(epochs):
    h = predict(X, W)
    loss = h - Y
    error = np.sum(loss ** 2) / (2*m)
    print("Epoch {}, Error: {}".format(epoch, error))
    gradient = np.dot(X.T, loss) / m
    W_delta = l_rate * gradient
    print("Weight delta: {}".format(W_delta))
    W -= W_delta

print()
X_test = np.array([0.227143051, 0.564529276, 2.064157399, 0.491, 0.557])
X_test1 = np.array([0.261536336,	0.508634982,	1.625550661, 0.44, 0.5])
print(predict(X_test, W))
print(predict(X_test1, W))