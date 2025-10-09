# COMPLETE AudioBook: tmp570y6i1_

**Source**: tmp570y6i1_.pdf
**Generated**: 2025-10-09 00:24:56
**System**: Hybrid (Gemini + LM Studio)
**Quality Score**: 0.65/1.0
**Enhancement Ratio**: 1.0x

---

--- Page 1 Text ---

AP23110010750 Implement polynomial Regression (2nd degree) using the following data
1. Now, Obtain the line of equation.
2. Now, Plot the regression line.
3. Now, Find the value of Y for given X.
4. Now.. Moreover, Calculate RMSE and R- squared error.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Given data
data = {
   "Temperature (x)": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
   "Yield (y)":       [5, 9, 14, 20, 27, 33, 37, 39, 38, 34]
}
df = pd.DataFrame(data)
X = df["Temperature (x)"].values
y = df["Yield (y)"].values
X_poly = np.column_stack((np.ones(len(X)), X, np.square(X)))
theta = np.dot(np.linalg.inv(np.dot(X_poly.T, X_poly)) , np.dot(X_poly.T, y))
a, b, c = theta
print(f"Equation: y = {a:.2f} + {b:.2f}x + {c:.3f}x²")
print(theta)
Equation: y = -53.84 + 6.85x + -0.129x²
[-53.83636364   6.85151515  -0.12878788]
y_pred = X_poly @ theta
plt.scatter(X, y, color="blue", label="Data points")
plt.plot(X, y_pred, color="red", label="Polynomial Regression (deg 2)")
plt.xlabel("Temperature (x)")
plt.ylabel("Yield (y)")
plt.title("Polynomial Regression (2nd Degree)")
plt.legend()
plt.show()
spark
9/24/25, 3:25 PM
polynomial.ipynb - Colab
https://colab.research.google.com/drive/1R5grTjv4Rtf7LOBP6Ym7oZdc3hnpRbQS#scrollTo=QMoP6d4NEVL4&printMode=true
1/2


--- Page 2 Text ---

x_new = 32
# a,b,c are the values in theta matrix
y_new = a + b*x_new + c*(x_new**2)
print(f"Predicted Y for X=32: {y_new:.2f}")
Predicted Y for X=32: 33.53
# RMSE
rmse = np.sqrt(np.mean((y - y_pred)**2))
print(f"RMSE = {rmse:.2f}")
# R-squared
ss_total = np.sum((y - np.mean(y))**2)
ss_res = np.sum((y - y_pred)**2)
r2 = 1 - (ss_res / ss_total)
print(f"R² = {r2:.3f}")
RMSE = 2.27
R² = 0.965
9/24/25, 3:25 PM
polynomial.ipynb - Colab
https://colab.research.google.com/drive/1R5grTjv4Rtf7LOBP6Ym7oZdc3hnpRbQS#scrollTo=QMoP6d4NEVL4&printMode=true
2/2