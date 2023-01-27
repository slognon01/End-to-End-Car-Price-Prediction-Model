from flask import Flask, render_template, request
#import jsonify
import requests
import pickle
import joblib
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression.pkl', 'rb'))
km_driven_mean = 66014.13
no_year_mean = 9.88
km_driven_std = 46905.39
no_year_std = 4.21
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Kms_Driven=int(request.form['Kms_Driven'])
        Year = int(request.form['Year'])
        Kms_Driven=(Kms_Driven-km_driven_mean)/km_driven_std
        Year=2020-Year
        Year=(Year-no_year_mean)/no_year_std
        Fuel_Type=request.form['Fuel_Type']
        if(Fuel_Type=='Diesel'):
                Fuel_Type_Diesel=1
                Fuel_Type_Electric=0
                Fuel_Type_LPG=0
                Fuel_Type_Petrol=0     
        elif(Fuel_Type=='Electric'):
                Fuel_Type_Diesel=0
                Fuel_Type_Electric=1
                Fuel_Type_LPG=0
                Fuel_Type_Petrol=0      
        elif(Fuel_Type=='LPG'):
                Fuel_Type_Diesel=0
                Fuel_Type_Electric=0
                Fuel_Type_LPG=1
                Fuel_Type_Petrol=0    
        elif(Fuel_Type=='Petrol'):
                Fuel_Type_Diesel=0
                Fuel_Type_Electric=0
                Fuel_Type_LPG=0
                Fuel_Type_Petrol=1
        else:
                Fuel_Type_Diesel=0
                Fuel_Type_Electric=0
                Fuel_Type_LPG=0
                Fuel_Type_Petrol=0                     

        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        elif(Seller_Type=='Individual'):
            Seller_Type_Individual=0	
            Seller_Type_Trustmark_Dealer=1
        else:
            Seller_Type_Individual=0	
            Seller_Type_Trustmark_Dealer=0            
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual Car'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        Owner=request.form['Owner']
        if(Owner=='Fourth_Above_Owner'):
                owner_Fourth_Above_Owner=1
                owner_Second_Owner=0
                owner_Test_Drive_Car=0
                owner_Third_Owner=0     
        elif(Owner=='Second_Owner'):
                owner_Fourth_Above_Owner=0
                owner_Second_Owner=1
                owner_Test_Drive_Car=0
                owner_Third_Owner=0   
        elif(Owner=='Test_drive_Owner'):
                owner_Fourth_Above_Owner=0
                owner_Second_Owner=0
                owner_Test_Drive_Car=1
                owner_Third_Owner=0   
        elif(Owner=='Third_Owner'):
                owner_Fourth_Above_Owner=0
                owner_Second_Owner=0
                owner_Test_Drive_Car=0
                owner_Third_Owner=1
        else:
                owner_Fourth_Above_Owner=0
                owner_Second_Owner=0
                owner_Test_Drive_Car=0
                owner_Third_Owner=0      
                
        prediction=model.predict([[Kms_Driven,Year,Fuel_Type_Diesel,Fuel_Type_Electric,Fuel_Type_LPG,Fuel_Type_Petrol,
        Seller_Type_Individual,Seller_Type_Trustmark_Dealer,Transmission_Mannual,owner_Fourth_Above_Owner,owner_Second_Owner,
        owner_Test_Drive_Car,owner_Third_Owner]])
        
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

