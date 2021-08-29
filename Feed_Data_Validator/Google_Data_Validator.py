import pandas as pd
from cerberus import Validator
import csv

feed = pd.read_csv('maniere_de_voir_us_google.csv')
#print (feed.head())

schema = {
    #'item_group_id': {'type': 'string','minlength':6 ,'maxlength': 50, 'required': True, 'empty':False},
    #'id': {'type': 'string', 'minlength':4 , 'max':50, 'required': True, 'empty':False},
    'title':{'type': 'string', 'maxlength': 150, 'empty':False},
    'description':{'type': 'string', 'maxlength': 5000, 'empty':False},
    'product_type':{'type':'string', 'required': True, 'empty':False , 'contains': '>'},
    #'google_product_category':{'type':'string', 'required': True, 'empty':False},
    'link':{'type':'string','regex':'^https|https://', 'required': True, 'empty':False},
    'image_link':{'type':'string','regex':'^https.*(.jpg|.png).*', 'required': True, 'empty':False},
    'condition':{'type':'string','required': True,'empty':False,'allowed': ['new']},
    'availability':{'type':'string','required': True,'empty':False,'allowed': ['in stock','out of stock','preorder'] },
    'price': {'type':'number','required': True,'empty':False, 'min':1,},
    'sale_price': {'type': 'number', 'required': True, 'min':1, 'empty':False},
    #'sale_price': {'type': 'number', 'required': True, 'min':1, 'dependencies': {'price'},'empty':False},
    'sale_price_effective_date': {'required': True, 'empty':True},
    'brand': {'type':'string','required': True, 'empty':False},
    #'gtin': {'type': 'string', 'required': True, 'maxlength': 14, 'empty':False},
    #'mpn': {'type': 'string', 'required': True, 'maxlength': 70, 'empty':False},
    'identifier_exists': {'type': 'boolean','required': True,'forbidden': ['FALSE'], 'empty':False},
    'gender': {'type':'string', 'required': True, 'allowed': ['female','male','unisex'],'empty':False},
    'age_group': {'type':'string', 'required': True, 'allowed': ['adult']},
    #'color': {'type':'string', 'required': True,'empty':False},
    #'size': {'type':'string', 'required': True, 'maxlength': 100,'forbidden': ['NoSize']},
    #'material':{'type':'string', 'required': True, 'maxlength': 200},
    #'pattern':{'type':'string', 'required': True, 'maxlength': 100},
    #'tax': {'type':'string', 'required': True},
    'shipping': {'type': 'string','required': True, 'regex':'^[A-Z].(::Standard).([\d]|[\d]..[\d]).[A-Z]{2,}', 'empty':False},
    #'additional_image_link': {'type':'string','regex':'^https.*(.jpg|.png).*', 'required': True, 'empty':False},
    #'mobile_link': {'type':'string','regex':'^http|https://', 'required': True, 'empty':False},
    #'size_system': {'type': 'string','required': True, 'regex':'^[A-Z]{2,}', 'empty':False},
    'size_type': {'type': 'string','required': True, 'regex':'^(regular)', 'empty':False},
    'is_bundle': {'type': 'boolean','required': True, 'regex': '^FALSE', 'empty':False}
}


v = Validator(schema)
v.allow_unknown = True
v.requir_all = True
#v.validate({'amount': 1000000})
#v.errors

df_dict = feed.to_dict(orient ='records')
#print(df_dict[:2])

df1_index_list = []
df2_errors_list = []

for idx, record in enumerate(df_dict):
    if not v.validate(record):
        print ({idx:v.errors})
        df1_index_list.append(idx+2)
        df2_errors_list.append(v.errors)


df_final = pd.DataFrame(data={"Index": df1_index_list, "Errors": df2_errors_list})

df_final.to_csv('Mismatch.csv', encoding='utf-8', sep=',',index=False)
        #print(v.validate)


#print(v.errors)

#print(len(v.errors))