# Basic imports that will use later in this notebook

from unicodedata import name
from flask import Flask
import numpy as np
import pandas as pd
import datetime


# initialize an app
app = Flask(__name__)

# define what will run in this app
@app.route('/')

# define a function that will run in this app in this case I'm using simple hello world function
def hello_world():
    # geranate some random number using numpy
    #ran_num = np.random.randint(3, 99, size=34, end="\n")
    My_str = f"Hello I've start learning Flask with Api \nThe time is {datetime.datetime.now()}"
    #my_dict = {"String": My_str,
                #"Random_Number": ran_num}
    
    # return the dict
    return My_str


# Let's run this app
if __name__=="__main__":
    app.debug = True
    app.run()

