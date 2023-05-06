import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from joblib import load
import json
import os

# Load KNN Model
knn_recommender = load('./knn/knn_model.joblib')

# Read CSV file of Success Startup Companies
startup_df = pd.read_csv('./knn/success_startup_dataset.csv', encoding = "ISO-8859-1")

X = startup_df.drop(['status_class','status','permalink','index'], axis=1)
X = X.drop(['homepage_url','market'],axis=1)
X = X.drop(['name','category_list','country_code'],axis=1)
X = X.drop(['state_code','region','city'],axis=1)
X = X.drop(['founded_at','founded_month','founded_quarter','founded_year'],axis=1)
X = X.drop(['first_funding_at','last_funding_at'],axis=1)

scaler = StandardScaler()
X = scaler.fit_transform(X)

def get_similar_companies(company_data):
    new_company_df = pd.DataFrame(transform_data(company_data), index=[0])
    new_company_data_normalized = scaler.transform(new_company_df)
    y_neighbours = knn_recommender.kneighbors([new_company_data_normalized[0]])
    dist, ind = y_neighbours
    ind_1d = ind.ravel()
    res = []
    for i in ind_1d:
        cur = {}
        cur["name"] = startup_df.loc[i, "name"]
        cur["category_list"] = startup_df.loc[i, "category_list"]
        res.append(cur)
    # json_answer = "{"
    # for i in ind_1d:
    #     json_answer = json_answer+"{\"name\": \"" + startup_df.loc[i, "name"] +"\","
    #     json_answer = json_answer+"\"category_list\": \"" + startup_df.loc[i, "category_list"] +"\"},"
    # json_answer = json_answer[:-1]
    # json_answer = json_answer + "}"
    return res

def transform_data(data):
    # parse the JSON value into a Python dictionary
    json_dict = data
    # add the "fail", "operating", "success" fields based on the "status" field
    if json_dict["status"] == "closed":
        json_dict["fail"] = 1
        json_dict["operating"] = 0
        json_dict["success"] = 0
    elif json_dict["status"] == "operating":
        json_dict["fail"] = 0
        json_dict["operating"] = 1
        json_dict["success"] = 0
    elif json_dict["status"] == "ipo":
        json_dict["fail"] = 0
        json_dict["operating"] = 0
        json_dict["success"] = 1
    # extract the needed fields
    new_json = {'funding_total_usd': json_dict["funding_total_usd"], 
                'funding_rounds': json_dict["funding_rounds"], 
                'seed': json_dict["seed"], 
                'venture': json_dict["venture"], 
                'equity_crowdfunding': json_dict["equity_crowdfunding"], 
                'undisclosed': json_dict["undisclosed"], 
                'convertible_note': json_dict["convertible_note"], 
                'debt_financing': json_dict["debt_financing"], 
                'angel': json_dict["angel"], 
                'grant': json_dict["grant"], 
                'private_equity': json_dict["private_equity"], 
                'post_ipo_equity': json_dict["post_ipo_equity"], 
                'post_ipo_debt': json_dict["post_ipo_debt"], 
                'secondary_market': json_dict["secondary_market"], 
                'product_crowdfunding': json_dict["product_crowdfunding"], 
                'round_A': json_dict["round_A"], 
                'round_B': json_dict["round_B"], 
                'round_C': json_dict["round_C"], 
                'round_D': json_dict["round_D"], 
                'round_E': json_dict["round_E"], 
                'round_F': json_dict["round_F"],
                'round_G': json_dict["round_G"], 
                'round_H': json_dict["round_H"],
                'fail': json_dict["fail"],
                'operating': json_dict["operating"], 
                'success':json_dict["success"]
                }
    return new_json


# json_val = '''
# {
#     "id": 123,
#     "permalink": "/organization/supplycart",
#     "name": "supplycart",
#     "homepage_url": "https://adam-procure.com/",
#     "description": "Procure to Pay Made Easy.",
#     "picture": "https://adam-procure.com/",
#     "category_list": "B2B|E-Commerce|Enterprise Resource Planning (ERP)|Marketplace|Procurement",
#     "market": "Software",
#     "funding_total_usd": 2500000,
#     "status": "operating",
#     "country_code": "MY",
#     "funding_rounds": 2,
#     "founded_at": "1/1/2016",
#     "first_funding_at": "1/1/2016",
#     "last_funding_at": "1/1/2019",
#     "seed": 0,
#     "venture": 0,
#     "equity_crowdfunding": 0,
#     "undisclosed": 0,
#     "convertible_note": 0,
#     "debt_financing": 0,
#     "angel": 0,
#     "grant": 0,
#     "private_equity": 0,
#     "post_ipo_equity": 0,
#     "post_ipo_debt": 0,
#     "secondary_market": 0,
#     "product_crowdfunding": 0,
#     "round_A": 0,
#     "round_B": 0,
#     "round_C": 0,
#     "round_D": 0,
#     "round_E": 0,
#     "round_F": 0,
#     "round_G": 0,
#     "round_H": 0,
#     "market size": "RM145.2 B"
# }
# '''
# new_company_data = transform_data(json_val)
# top5_company = get_similar_companies(new_company_data)
# print(top5_company)

