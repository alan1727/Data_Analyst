import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import pandas
import statsmodels.api as sm

# 3.1
# Plot two histograms on the same axes to show hourly
# entries when raining vs. when not raining
def entries_histogram(turnstile_weather):
    plt.figure()
    turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].plot(kind='hist')
    turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].plot(kind='hist')
    return plt


# 3.2
"""
- The entries data from the previous exercise seems not normally distributed.
- We cannot run welch's T test on entries data. Because the data is not 
normally distributed and we don't know the standard deviation of population.
"""


# 3.3
# Take the means and run the Mann Whitney U-test on the 
# ENTRIESn_hourly column in the turnstile_weather dataframe.
def mann_whitney_plus_means(turnstile_weather):
    df_with_rain = turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly']
    df_withot_rain = turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly']
    with_rain_mean = np.mean(df_with_rain)
    without_rain_mean = np.mean(df_without_rain)
    results = scipy.stats.mannwhitneyu(df_with_rain, df_without_rain)
    U = results[0]
    p = results[1]
    return with_rain_mean, withou_rain_mean, U, p


# 3.4
"""
- The distribution of the number of entries is statistically different between rainy & non rainy days.
- The p-value is significantly less than 5%. Thus the null hypothesis can be rejected.
"""


# 3.5
# Implement the linear_regression() procedure
def linear_regression(features, values):
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    return intercept, params

# Select features and make predictions
def predictions(dataframe):
    # Select features
    features = dataframe[['rain','precipi','Hour']]
    
    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values
    
    # Perform linear regression
    intercept, params = linear_regression(features_array, values_array)
    
    predictions = intercept + np.dot(features_array, params)
    
    return predictions


# 3.6
# Plot a histogram of entries per hour 
def plot_residuals(turnstile_weather, prediction):
    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist()
    return plt


# 3.7
# Return the coefficient of determinaion (R^2)
def computer_r_squared(data, predictions):
    ssr = ((data - predictions)**2).sum()
    sst = ((data - np.mean(data))**2).sum()
    r_squared = 1 - ssr/sst
    return r_squared


# 3.8
# Gradient Descent
def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    ''' 
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    """ 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. Takes the means and standard deviations of the original
    features, along with the intercept and parameters computed using the normalized
    features, and returns the intercept and parameters that correspond to the original
    features.
    """ 
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    
    model = SGDRegressor()
    model.fit(features,values)
    intercept = model.intercept_
    params  = model.coef_
    return intercept, params

def predictions(dataframe):
    """
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    """
    # Select Features (try different features!)
    features = dataframe[['rain','meanwindspdi','Hour','meantempi','meanpressurei']]
    
    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values
    
    means, std_devs, normalized_features_array = normalize_features(features_array)

    # Perform gradient descent
    norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
    
    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    
    predictions = intercept + np.dot(features_array, params)
    # The following line would be equivalent:
    # predictions = norm_intercept + np.dot(normalized_features_array, norm_params)
    
    return predictions

