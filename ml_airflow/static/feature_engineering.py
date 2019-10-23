#####################################################################################
#
#
# 	Custom ML Airflow Feature Engineering
#  
#	Author: Sam Showalter
#	Date: October 6, 2018
#
#####################################################################################


#####################################################################################
# External Library and Module Imports
#####################################################################################

import pandas as pd

#####################################################################################
# Class and Constructor
#####################################################################################

def normalize_values(data, prefit = None):
    
    mean = None
    std = None

    if not isinstance(data, pd.Series):
        raise ValueError("Input data has more than one column")

    if prefit:
        std = prefit['std']
        mean = prefit['mean']
    else:
        std = data.std()
        mean = data.mean()

    if std == 0:
        raise ValueError("ERROR: Data is all the same value and provides not insight.\
        Please re-create dag without column included.")

    data = (data - mean) / std

    if prefit:
        return data
    else:
        prefit = {'mean': mean, 'std': std}
        return data, prefit

def mla_get_dummies(data, prefit = None):

    dummy_df = pd.get_dummies(data)

    return dummy_df

def mla_linear_transformation(data, method, prefit = None):

    if prefit:
        res, _ = method(data, prefit['lambda_c'])
        pd.Series(res, name = data.name)

    else:
        res, lambda_c = method(data)
        return pd.Series(res, name = data.name), {'lambda_c'}

    



def create_boolean_df(data, boolean_names_and_values, prefit = None):

    boolean_df = data

    if not isinstance(boolean_df, pd.Series):
        raise ValueError("Input data has more than one column")

    yes = boolean_names_and_values[data.name][0]
    no = boolean_names_and_values[data.name][1]

    boolean_df = boolean_df.replace({yes: 1,
                                  no: 0}, 
                                  inplace = False)

    boolean_df.name = boolean_df.name


    return boolean_df

def create_ordinal_df(data, ordinal_dict, prefit = None):
    
    ordinal_df = data
        

    #Make new ordinal column (suffix = "ord") by replacing values with ordinal dictionary
    ordinal_df = ordinal_df.replace(ordinal_dict, inplace = False)

    ordinal_df.name = ordinal_df.name
    
    return ordinal_df