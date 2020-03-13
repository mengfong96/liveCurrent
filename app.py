from flask import Flask, render_template
from flask import request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("fyp_demo.csv")
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
#create a column called "datetime"

df = df.set_index("Datetime")
log_reg1 = pickle.load(open("log_reg1(ML).pkl", "rb"))
#output: LogisticRegression(C=1.0,
                #    class_weight={0: 0.5447116711965692, 1: 6.091381250343048},
                #    dual=False, fit_intercept=True, intercept_scaling=1,
                #    l1_ratio=None, max_iter=100, multi_class='warn', n_jobs=None,
                #    penalty='l2', random_state=None, solver='lbfgs', tol=0.0001,
                #    verbose=0, warm_start=False)


log_reg2 = pickle.load(open("log_reg2(ML).pkl", "rb"))
#output: LogisticRegression(C=1.0,
                #    class_weight={0: 0.699465059481604, 1: 1.7533523447652073},
                #    dual=False, fit_intercept=True, intercept_scaling=1,
                #    l1_ratio=None, max_iter=100, multi_class='warn', n_jobs=None,
                #    penalty='l2', random_state=None, solver='lbfgs', tol=0.0001,
                #    verbose=0, warm_start=False)

log_reg3 = pickle.load(open("log_reg3(ML).pkl", "rb"))
#LogisticRegression(C=1.0,
                #    class_weight={0: 0.9316365506096665, 1: 1.0791909875261645},
                #    dual=False, fit_intercept=True, intercept_scaling=1,
                #    l1_ratio=None, max_iter=100, multi_class='warn', n_jobs=None,
                #    penalty='l2', random_state=None, solver='lbfgs', tol=0.0001,
                #    verbose=0, warm_start=False)

scaler,onehot = pickle.load(open("preprocessor(ML).pkl", "rb"))
#output: scaler: StandardScaler(copy=True, with_mean=True, with_std=True)
#output: onehot: OneHotEncoder(categories=None, drop=None, dtype=<class 'numpy.float64'>,
              # handle_unknown='error', sparse=False)

def get_prediction(matched_row):
    s1 = log_reg1.predict(matched_row)
    s2 = log_reg2.predict(matched_row)
    s3 = log_reg3.predict(matched_row)
    return s1, s2, s3

def get_matched_row(user_time):
    user_time = pd.date_range('17-12-2006', periods = 1440, freq ='T') 
    index_user_time = df.loc[user_time]
    
    features = index_user_time[["Power Factor", "Voltage", "Current"]].values
    # output:    [[9.89566792e-01 2.42730000e+02 8.23960800e-03]
                # [9.89687371e-01 2.42200000e+02 4.12881900e-03]
                # [9.97967305e-01 2.40140000e+02 8.32847500e-03]
                # ...
                # [9.91917451e-01 2.38530000e+02 7.54622060e-02]
                # [9.92104363e-01 2.38360000e+02 7.13206910e-02]
                # [9.91790229e-01 2.38870000e+02 7.53547950e-02]]

    features = scaler.transform(features)
    #output:    [[ 0.67664673  0.84371454 -0.49665491]
                # [ 0.67693549  0.68227863 -0.57006259]
                # [ 0.69676406  0.05481072 -0.49506798]
                # ...
                # [ 0.68227603 -0.43558896  0.70376063]
                # [ 0.68272364 -0.48737029  0.62980426]
                # [ 0.68197136 -0.3320263   0.70184255]]
    
    rp = onehot.transform(index_user_time["Real Power"].values.reshape(-1, 1))
    #output: [[0. 0. 1. ... 0. 0. 0.]
            # [0. 1. 0. ... 0. 0. 0.]
            # [0. 0. 1. ... 0. 0. 0.]
            # ...
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]]

    features = np.concatenate([features, rp[:, 1:]], axis=-1)
    #     [[ 0.67664673  0.84371454 -0.49665491 ...  0.          0.
        # 0.        ]
        # [ 0.67693549  0.68227863 -0.57006259 ...  0.          0.
        # 0.        ]
        # [ 0.69676406  0.05481072 -0.49506798 ...  0.          0.
        # 0.        ]
        # ...
        # [ 0.68227603 -0.43558896  0.70376063 ...  0.          0.
        # 0.        ]
        # [ 0.68272364 -0.48737029  0.62980426 ...  0.          0.
        # 0.        ]
        # [ 0.68197136 -0.3320263   0.70184255 ...  0.          0.
        # 0.        ]]

    return features

# def get_real_power():
#     user_time = pd.date_range('17-12-2006', periods = 720, freq ='T') 
#     index_user_time = df.loc[user_time]
    
#     power_feature = index_user_time[["Real Power"]].values
#     return power_feature

def get_cursor_point(x_point):
    user_time = pd.date_range('17-12-2006', periods = 720, freq ='T')
    #output: DatetimeIndex(['2006-12-17 00:00:00', '2006-12-17 00:01:00',
            #    '2006-12-17 00:02:00', '2006-12-17 00:03:00',
            #    '2006-12-17 00:04:00', '2006-12-17 00:05:00',
            #    '2006-12-17 00:06:00', '2006-12-17 00:07:00',
            #    '2006-12-17 00:08:00', '2006-12-17 00:09:00',
            #    ...
            #    '2006-12-17 11:50:00', '2006-12-17 11:51:00',
            #    '2006-12-17 11:52:00', '2006-12-17 11:53:00',
            #    '2006-12-17 11:54:00', '2006-12-17 11:55:00',
            #    '2006-12-17 11:56:00', '2006-12-17 11:57:00',
            #    '2006-12-17 11:58:00', '2006-12-17 11:59:00'],
            #   dtype='datetime64[ns]', length=720, freq='T')

    index_user_time = df.loc[user_time]
    #output:                           Date      Time  ... Sub_metering_2  Sub_metering_3
            # 2006-12-17 00:00:00  17-12-06   0:00:00  ...              2               0
            # 2006-12-17 00:01:00  17-12-06   0:01:00  ...              1               0
            # 2006-12-17 00:02:00  17-12-06   0:02:00  ...              2               0
            # 2006-12-17 00:03:00  17-12-06   0:03:00  ...              1               0
            # 2006-12-17 00:04:00  17-12-06   0:04:00  ...              2               0
            # ...                       ...       ...  ...            ...             ...
            # 2006-12-17 11:55:00  17-12-06  11:55:00  ...              0              18
            # 2006-12-17 11:56:00  17-12-06  11:56:00  ...              0              17
            # 2006-12-17 11:57:00  17-12-06  11:57:00  ...              0              18
            # 2006-12-17 11:58:00  17-12-06  11:58:00  ...              0              17
            # 2006-12-17 11:59:00  17-12-06  11:59:00  ...              1              17


    power_feature = index_user_time[["Real Power"]].values
    #output: array of Real Power output in vertical way 
    #[[2][1][2]...[17][18]]

    power_feature = power_feature.reshape(-1,)
    # [ 2  1  2  1  2  1  1  2  1  2  1  1  2  1  1  1  2  1  1  1  1  0  0  0
    #   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
    #   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 13 35 28 37 27 37 36 36
    #  37 35 36 36 36 36 35 36 35 36 26 24 36 36 21 28 37 28 22 36 36 17 33 36
    #  25 25 36 24 26 36 26 23 37 18 30 28 31  5 16 23 37 16  5  5  5  4  5  5
    #   5  3  1  2  1  2  1  1  2  1  1  2  1  2  1  1  0  0  1  0  0  0  0  0
    #   1  0  0  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  1  0  0  0  0
    #   0  1  0  0  0  0  0  1  0  0  0  0  0  4  4  3  4  3  4  3  4  0  0  0
    #   0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0
    #   0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  2  2  1  2  1  2
    #   1  2  2  1  2  1  2  1  2  1  2  1  2  1  2  1  1  2  1  0  0  0  0  0
    #   1  0  0  0  0  0  5 19 19 19 18 19 18 19 19 18 18 18 18 19 18 18 18 19
    #  18 19 18 18 18 18 19 19 18 18 18 18 19 17 18 19 19 18 18 18 19 17 18 18
    #  18 18 19  9  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0
    #   0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0
    #   0  0  0  1  1  1  2  2  1  2  1  2  2  1  2  1  2  1  2  1  2  1  2  1
    #   2  1  1  2  1  0  0  0  1  0  0  0  0  0  1  0  0  0  0  1  0  0  0  0
    #   0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  0  0  1  0  0
    #   0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0
    #   0  0  1  0  0  0  0  0  0  1  0  0  0  0  0  1  0  0  0  0  0  1  0  0
    #   0  0  0  1  0  0  0  0  0  1  0  0  0  0  1  0  0  0  2  1  2  1  2  1
    #   2  1  2  2  1  2  1  2  1  2  1  2  1  1  2  1  2  1  1  1  0  0  0  0
    #   0  1  0  0  0  0  0  1  0  0  1  1  1  7 38 37 37 38 37 37 38 38 37 27
    #   2 26  2  1  0  1  2  1  2  1  1  0  1  1  1  2  2  5  5  5  5  1  0  0
    #   0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
    #   0  0  0 18 18 17 18 17 16 17 18 17 17 17 17 18 17 17 18 17 17 17 18 25
    #  54 44 53 45 53 54 53 55 54 55 59 90 88 88 89 88 87 90 87 90 88 77 81 89
    #  77 47 39 54 54 43 45 69 89 76 80 88 58 36 47 47 52 31 46 43 30 26 38 21
    #  22 24 22 21 22 22 22 18 18 30 55 53 55 54 54 54 55 54 55 56 59 55 55 54
    #  28 17 18 17 17 19 18 18 18 17 18 18 18 18 17 18 17 19 17 18 17 18 17 18]

    features_for_ML = get_matched_row(user_time)
    s1, s2, s3 = get_prediction(features_for_ML)
    #toCSV(s1,s2,s3)
    #print(s1.shape, power_feature.shape)
    cursor_point = np.concatenate([power_feature, s1, s2, s3], axis=-1)
    cursor_point_value = cursor_point

    return cursor_point_value

# def toCSV(s1,s2,s3): 
#     np.savetxt("s1.csv", s1, fmt="%d", delimiter=",")
#     np.savetxt("s2.csv", s2, fmt="%d", delimiter=",")
#     np.savetxt("s3.csv", s3, fmt="%d", delimiter=",")

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