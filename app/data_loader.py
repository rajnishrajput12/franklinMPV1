import pandas as pd

def load_app_data():
    return pd.read_csv("./Data/googleplaystore.csv")

def load_reviews():
    return pd.read_csv("./Data/googleplaystore_user_reviews.csv")