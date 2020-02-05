import pandas as pd
import numpy as np
import tensorflow as tf
from keras.utils import to_categorical
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import Dense
from numpy import argmax

def getResult(lat:float,lng:float,type:str):

	data = pd.read_csv("yelp_data_clean.csv")

	specific_data = data.loc[data['categories']== type]
	X = specific_data[['latitude', 'longitude']].to_numpy()
	y_price_temp = specific_data['price'].to_numpy()
	y_price_temp = y_price_temp.reshape(-1,1)
	y_rating_temp = specific_data['rating'].to_numpy()
	y_rating_temp = y_rating_temp.reshape(-1, 1)

	m = len(y_price_temp)
	empty = np.empty(m)
	for i in range(m):
	    empty[i] = len(y_price_temp[i][0])

	y_price = empty
	y_price = to_categorical(y_price)

	size = y_price.shape[1]
	
	X_train, X_test, y_train, y_test = train_test_split(X, y_price, random_state=1)
	
	X_scaler = StandardScaler().fit(X_train)

	X_train_scaled = X_scaler.transform(X_train)
	X_test_scaled = X_scaler.transform(X_test)	

	model = Sequential()
	
	model.add(Dense(units=3, activation='relu', input_dim=2))
	model.add(Dense(units=4, activation='relu'))
	model.add(Dense(units=size, activation='softmax'))

	model.compile(optimizer='adam',
	              loss='categorical_crossentropy',
	              metrics=['accuracy'])

	model.fit(
	    X_train_scaled,
	    y_train,
	    epochs=50,
	    shuffle=True,
	    verbose=2
	)
	inputCord = np.array([lat,lng])
	inputCord = inputCord.reshape(1,-1)
	inputCord = X_scaler.transform(inputCord)
	resultPrice = model.predict(inputCord).round(2)
	resultPriceRev = argmax(resultPrice)
	resultPriceInt = int(resultPriceRev)
	resultPriceList = resultPrice.tolist()[0]
	model_loss, modelAccuracyPrice = model.evaluate(X_test_scaled, y_test, verbose=2)
	
	m = len(y_rating_temp)
	empty = np.empty(m)

	for i in range(m):
		empty[i] = y_rating_temp[i][0]

	y_rating = empty
	y_rating = to_categorical(y_rating)
	size = y_rating.shape[1]


	X_train, X_test, y_train, y_test = train_test_split(X, y_rating, random_state=1)
	X_scaler = StandardScaler().fit(X_train)
	X_train_scaled = X_scaler.transform(X_train)
	X_test_scaled = X_scaler.transform(X_test)

	model = Sequential()

	model.add(Dense(units=3, activation='relu', input_dim=2))
	model.add(Dense(units=4, activation='relu'))
	model.add(Dense(units=size, activation='softmax'))

	model.compile(optimizer='adam',
	              loss='categorical_crossentropy',
	              metrics=['accuracy'])

	model.fit(
	    X_train_scaled,
	    y_train,
	    epochs=50,
	    shuffle=True,
	    verbose=2
	)

	model_loss, modelAccuracyRating = model.evaluate(X_test_scaled, y_test, verbose=2)

	resultRating = model.predict(inputCord).round(2)
	resultRatingRev = argmax(resultRating)
	resultRatingInt = int(resultRatingRev)
	resultRatingList = resultRating.tolist()[0]

	highest = max(resultPriceList)
	k = resultPriceList.index(highest)
	s = len(resultPriceList)
	score = resultPriceInt
	resultPriceWeightedList = []

	for i in range(0,s):
	    d = k-i
	    scorei = score - d
	    calculated = resultPriceList[i]*scorei
	    # print(calculated)
	    resultPriceWeightedList.append(calculated)

	resultPriceWeighedSum = sum(resultPriceWeightedList)

	highest = max(resultRatingList)
	k = resultRatingList.index(highest)
	s = len(resultRatingList)
	score = resultRatingInt
	resultRatingWeightedList = []

	for i in range(0,s):
	    d = k-i
	    scorei = score - 0.5*d
	    calculated = resultRatingList[i]*scorei
	    # print(calculated)
	    resultRatingWeightedList.append(calculated)

	resultRatingWeighedSum = sum(resultRatingWeightedList)





	return [resultPriceInt, resultPriceList, resultPriceWeighedSum, modelAccuracyPrice, resultRatingInt, resultRatingList, resultRatingWeighedSum, modelAccuracyRating]