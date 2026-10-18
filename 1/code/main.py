#importing the data and the libraries

import seaborn as sea
import pandas as panda
from random import randint as rando
import matplotlib.pyplot as libby
from sklearn.linear_model import PoissonRegressor, LinearRegression

train = panda.read_csv('C:/Users/Hayoo/Downloads/CS156/Portfolio/1/data/training-data.csv')
valid = panda.read_csv('C:/Users/Hayoo/Downloads/CS156/Portfolio/1/data/validation-data.csv')

#preprocessing the data 

train['time'] = panda.to_datetime(train['time'], format='%H:%M').dt.floor('30min').dt.strftime('%H:%M')
train = train.groupby(['line','station', 'day', 'time']).size().reset_index(name='inspections')
train['incident'] = (train['line'] + ' ' +
                    train['station'] + ' ' +
                    train['day'] + ' ' +
                    train['time'].astype(str))


#visualizing the data

sea.histplot(train.nlargest(75, 'inspections'), x='incident', y='inspections', hue = 'day', multiple='stack', shrink=0.85, discrete=False)
libby.xticks(rotation=75)
libby.show()


#fitting the data to the Poisson Regressor model
X = panda.get_dummies(train[['line','station','day','time']])
y = train['inspections']

model = LinearRegress()
model.fit(X, y)

#processing the validation data

valid['time'] = panda.to_datetime(valid['time'], format='%H:%M').dt.floor('30min').dt.strftime('%H:%M')
valid = valid.groupby(['line','station', 'day', 'time']).size().reset_index(name='inspections')
valid['incident'] = (valid['line'] + ' ' +
                    valid['station'] + ' ' +
                    valid['day'] + ' ' +
                    valid['time'].astype(str))

#validating the Poisson Regressor model

for i in range(10):
    report = valid.iloc[rando(0, len(valid))]
    incident = panda.DataFrame([{"line": report['line'], 
                                "station": report['station'],
                                "day": report['day'], 
                                "time": report['time']}])

    prediction = model.predict(panda.get_dummies(incident).reindex(columns=X.columns, fill_value=0))

    print('Incident:', report['incident'])
    print('Predict:', prediction[0])
    print('Actual:', report['inspections'])

squared_error = ((model.predict(X) - y) ** 2).mean()
print('Mean Squared Error:', squared_error)

