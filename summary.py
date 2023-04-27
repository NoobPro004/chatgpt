import openai
import pandas as pd
import csv
import json
from dotenv import load_dotenv
import os

# Define OpenAI API key
load_dotenv()

openai.api_key = os.environ["OPEN_API_KEY"]
model_engine = "text-davinci-003"
headerList=['contactID','Call Transcript','Summary','Sentiment','Call_Score','Hygiene']
responseheaders=['Summary','Sentiment','Call_Score','Hygiene']
list=[]

df = pd.read_csv('call_scripts.csv')

for index, row in df.iterrows():
    nl=[]
    ques="Generate me Summary ,score, sentiment, hygine in one line for the particular transcript in Python as dict with keys in double quotes and comma seperated: \n"+row[' Transcript']
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=ques,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.2,
    )

    try:
        response = json.loads(completion.choices[0].text)
        msg={}
        for key in response:
            if key.lower()=='score':
                msg['Call_Score']=response[key]
            elif key.lower() == 'sentiment':
                msg['Sentiment'] = response[key]
            elif key.lower() =='summary':
                msg["Summary"] = response[key]
            elif key.lower() == 'hygiene':
                msg['Hygiene'] = response[key]
        
        nl.append(row['ContactID'])
        nl.append(row[' Transcript'])
        
        for key in responseheaders:
            nl.append(msg[key])

        list.append(nl)
    except:
        print(index)

f = open('demo.csv', 'w')
writer = csv.writer(f)
writer.writerow(headerList)
writer.writerows(list)
f.close()
