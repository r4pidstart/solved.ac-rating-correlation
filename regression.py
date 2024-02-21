import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data_path = './output_cf.csv'
data = pd.read_csv(data_path)
data = data[data['rating2'] > 200]

std_dev_x=data['rating2'].std()
data = data[abs(data.iloc[:,3] - data.iloc[:,3].mean()) < 3 * std_dev_x]
print(f'var-{data["rating2"].var()}')

x = data['rating2']
y = data['rating1'] 

x_train, x_test, y_train, y_test = train_test_split(x.to_frame(), y.to_frame(), test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print(f'mse: {mean_squared_error(y_test, y_pred)}')

plt.figure(figsize=(12, 6))
plt.scatter(x_test['rating1'], y_test, color='black')
plt.plot(x_test['rating1'], y_pred, color='red', linewidth=2)

# cf
plt.xlabel('codeforces rating')
plt.axvline(2100, 0, 1, color='orange', linestyle='solid')
plt.axvline(1900, 0, 1, color='purple', linestyle='solid')
plt.axvline(1600, 0, 1, color='blue', linestyle='solid')
plt.axvline(1400, 0, 1, color='turquoise', linestyle='solid')
plt.axvline(1200, 0, 1, color='green', linestyle='solid')

# at 
# plt.xlabel('atcoder rating')
# plt.axvline(2400, 0, 1, color='orange', linestyle='solid')
# plt.axvline(2000, 0, 1, color='yellow', linestyle='solid')
# plt.axvline(1600, 0, 1, color='blue', linestyle='solid')
# plt.axvline(1200, 0, 1, color='turquoise', linestyle='solid')
# plt.axvline(800, 0, 1, color='green', linestyle='solid')
# plt.axvline(400, 0, 1, color='saddlebrown', linestyle='solid')

plt.ylabel('solved.ac rating')
# plt.axhline(800, 0, 1, color='gold', linestyle='solid')
plt.axhline(1600, 0, 1, color='lawngreen', linestyle='solid')
plt.axhline(2200, 0, 1, color='deepskyblue', linestyle='solid')
plt.axhline(2700, 0, 1, color='deeppink', linestyle='solid')
plt.axhline(3000, 0, 1, color='slategray', linestyle='solid')

plt.title(f'{model.coef_}x+{model.intercept_}')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
