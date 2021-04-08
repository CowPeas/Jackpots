# Importing the libraries
import numpy as np
from sklearn.preprocessing import StandardScaler
#import matplotlib.pyplot as plt
import pandas as pd
import pickle

dat = pd.read_csv("/home/odin/flask-model/Deployment-flask/jkpot.csv")

dat.columns = ["H","D","A","TLP","W"]
X = dat.iloc[:,:4]
Y = dat.iloc[:,-1]

#standardizer = StandardScaler()
#X_std = standardizer.fit_transform(X)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1).fit(X, Y)
#new = None
#knn.predict(new)
#Converting words to integer values
#def convert_to_int(word):
 #   word_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8,
  #              'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'zero':0, 0: 0}
   # return word_dict[word]

#X['W'] = X['W'].apply(lambda x : convert_to_int(x))

#y = dataset.columns["W"]

#Splitting Training and Test Set
#Since we have a very small dataset, we will train our model with all availabe data.

#from sklearn.linear_model import LinearRegression
#regressor = LinearRegression()

#Fitting model with trainig data
#regressor.fit(X, Y)

# Saving model to disk
#pickle.dump(KNeighborsClassifier, open('model.pkl','wb'))

# Loading model to compare the results
#model = pickle.load(open('model.pkl','rb'))
#new = [[2.89,1.97,3.25,1.0666]]

#nm =knn.predict(new)
#print(nm)  
pickle.dump(knn, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
