# fit linear model with sklearn
from sklearn.linear_model import LinearRegression
reg = LinearRegression()

from sklearn.model_selection import train_test_split
X = final.drop(['btcPrice', 'Date', 'Sentiment'], axis = 1)
y = final['btcPrice']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg.fit(X_train, y_train)

reg.score(X_train,y_train)

reg.score(X_test,y_test)
