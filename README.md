# devakademi2018

## Bid Price Estimator

It is an advertisement bid price estimator. It uses all sahibinden.com advertisement data and creates a decision tree model. 
Then, it serves a flask application to get input from user about advertisement features. After selecting features, user 
submits them and decision tree calculates getting click possibility. If user leaves a feature as "all" system makes somehow 
an id3 approach and calculates possibilities for all inputs for that feature e.g. Gender: All -> Man, Woman. System asks user
another input which is minimum (or default or worst case) bid price. Default minimum bid price is set as 100 kuruş. It uses it in a calculation: 

Estimated bid price = worst case bid price + 10 * possibility to get click for that condition

To run the application you have to run FLASK_APP=page.py flask run in your terminal. It serves flask app on 127.0.0.1:5000.

If you want to see decision tree as pdf file you can uncomment lines 24:26 in dt.py

## Example

When minimum bid price is 130 kuruş if you want to limit your ads for men which is between 30-40 years old price become 153.34 kuruş.

## Requirements
Numpy

Scikit-Learn

Graphviz

Flask
