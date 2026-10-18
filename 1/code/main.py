#importing the data and the libraries

from math import e
import seaborn as sea
import pandas as panda
from random import choice as rando
import matplotlib.pyplot as libby
from sklearn.linear_model import PoissonRegressor, LinearRegression

train = panda.read_csv('C:/Users/Hayoo/Downloads/CS156/Portfolio/1/data/training-data.csv')
valid = panda.read_csv('C:/Users/Hayoo/Downloads/CS156/Portfolio/1/data/validation-data.csv')

#processing the training data 

train['time'] = panda.to_datetime(train['time'], format='%H:%M').dt.floor('15min').dt.strftime('%H:%M')
train = train.groupby(['line','station', 'day', 'time']).size().reset_index(name='inspections')

train['incident'] = (train['line'] + ' ' +
                    train['station'] + ' ' + 
                    train['day'] + ' ' +
                    train['time'].astype(str))


#visualizing the data

sea.histplot(train.nlargest(75, 'inspections'), x='incident', y='inspections')
libby.xticks(rotation=75)
libby.show()

#fitting the data to the Poisson Regressor model
X = panda.get_dummies(train[['line','station', 'day','time']])
y = train['inspections']

model = PoissonRegressor()
model.fit(X, y)

#validating the Poisson Regressor model

def predict(line, station, day, time):
    incident = panda.DataFrame([{"line": line, "station": station, "day": day, "time": time}])

    if line + ' ' + station + ' ' + day + ' ' + str(time) not in train['incident'].values:
        return 0
    
    prediction = model.predict(panda.get_dummies(incident).reindex(columns=X.columns, fill_value=0))

    return prediction[0]

def squishification(value, min, max):
    if value < min:
        return 0
    elif value > max:
        return 1
    else:
        return (e**((value - min)/(max - min)) - 1)/ (e - 1)
    

error = 0
smallest = valid.nsmallest(1,'inspections').values[0]
largest = valid.nlargest(1,'inspections').values[0]
min_predict = -0.86
max_predict = 6.75
min_actual = smallest[4]
max_actual = largest[4]

for incident in valid.values:
    prediction = predict(incident[0], incident[1], incident[2], incident[3])
    prediction = squishification(prediction, min_predict, max_predict)
    actual = squishification(incident[4], min_actual, max_actual)
    error += abs(prediction - actual)

print('Total error:', error/len(valid))
