import requests
import json

url = "http://localhost/process-feature"  
headers = {'Content-type': 'application/json'}

updated_data = []

for i in range(df.shape[0]):
    data = dict(df.iloc[i])
    response = requests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        data.update(response.json())
    else:
        print("Error:", response.status_code)
        print("Response:", response.text)
    updated_data.append(data)
    
res = pd.DataFrame(updated_data)
res.to_csv('data_with_new_features.csv', index = False)