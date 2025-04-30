from django.shortcuts import render, redirect
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from .models import HousePrediction

def home(request):
    return render(request, "home.html")

def predict(request):
    if request.method == 'POST':
        # Retrieve form values
        var1 = request.POST.get('n1')
        var2 = request.POST.get('n2')
        var3 = request.POST.get('n3')
        var4 = request.POST.get('n4')
        var5 = request.POST.get('n5')
        
        # Check if all fields are filled
        if not all([var1, var2, var3, var4, var5]):
            return render(request, "home.html", {"error_message": "Please fill in all fields."})
        
        # Convert form values to floats
        try:
            var1 = float(var1)
            var2 = float(var2)
            var3 = float(var3)
            var4 = float(var4)
            var5 = float(var5)
        except ValueError:
            return render(request, "home.html", {"error_message": "Invalid input. Please enter valid numbers."})
        
        # Load dataset
        data = pd.read_csv(r"C:\Users\DELL\Desktop\HousePricePrediction\USA_Housing.csv")
        data = data.drop(['Address'], axis=1)
        
        # Define features (X) and target (Y)
        X = data.drop('Price', axis=1)
        Y = data['Price']
        
        # Split data into training and testing sets
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)
        
        # Default to Linear Regression model
        model = LinearRegression()
        
        # Train the model
        model.fit(X_train, Y_train)
        
        # Make prediction
        pred = model.predict(np.array([var1, var2, var3, var4, var5]).reshape(1, -1))
        pred = round(pred[0])
        price = "Predicted price is $" + str(pred)

        # Save data in the database
        prediction = HousePrediction.objects.create(
            avg_area_income=var1, 
            avg_house_age=var2, 
            avg_area_rooms=var3, 
            avg_area_bedrooms=var4, 
            avg_area_population=var5, 
            predicted_price=pred
        )
        prediction.save()
        
        return render(request, "predict.html", {"result2": price})
    else:
        return render(request, "predict.html")
