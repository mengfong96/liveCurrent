from flask import Flask, render_template, Response
from flask import request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("fyp_demo.csv")
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
df = df.set_index("Datetime")
log_reg1 = pickle.load(open("log_reg1(ML).pkl", "rb"))
log_reg2 = pickle.load(open("log_reg2(ML).pkl", "rb"))
log_reg3 = pickle.load(open("log_reg3(ML).pkl", "rb"))
scaler,onehot = pickle.load(open("preprocessor(ML).pkl", "rb"))

def get_prediction(matched_row):
    s1 = log_reg1.predict(matched_row)
    s2 = log_reg2.predict(matched_row)
    s3 = log_reg3.predict(matched_row)
    return s1, s2, s3

def get_matched_row(user_time):
    user_time = pd.date_range('17-12-2006', periods = 720, freq ='T') 
    index_user_time = df.loc[user_time]
    
    features = index_user_time[["Power Factor", "Voltage", "Current"]].values
#   features = features.reshape(1,-1)
    features = scaler.transform(features)
    
    rp = onehot.transform(index_user_time["Real Power"].values.reshape(-1, 1))
    features = np.concatenate([features, rp[:, 1:]], axis=-1)
    return features

# def get_real_power():
#     user_time = pd.date_range('17-12-2006', periods = 720, freq ='T') 
#     index_user_time = df.loc[user_time]
    
#     power_feature = index_user_time[["Real Power"]].values
#     return power_feature

def get_cursor_point(x_point):
    user_time = pd.date_range('17-12-2006', periods = 720, freq ='T') 
    index_user_time = df.loc[user_time]
    power_feature = index_user_time[["Real Power"]].values
    power_feature = power_feature.reshape(-1,)
    
    features_for_ML = get_matched_row(user_time)
    s1, s2, s3 = get_prediction(features_for_ML)
    #toCSV(s1,s2,s3)
    #print(s1.shape, power_feature.shape)
    cursor_point = np.concatenate([power_feature, s1, s2, s3], axis=-1)
    cursor_point_value = cursor_point

    return cursor_point_value

def toCSV(s1,s2,s3): 
    np.savetxt("s1.csv", s1, fmt="%d", delimiter=",")
    np.savetxt("s2.csv", s2, fmt="%d", delimiter=",")
    np.savetxt("s3.csv", s3, fmt="%d", delimiter=",")

@app.route('/')
def html_table():
    return render_template('energy_consumption.html')

# @app.route('/')
# def html_table():
#     legend = 'Power Usage'
#     labels =  pd.date_range('17-12-2006', periods = 720, freq ='T')
#     values =  get_cursor_point(labels)   

#     return render_template('Energy_Consumption_Graph.html', values=values, labels=labels, legend=legend)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 