import requests
import json

url = "https://us-east-1.aws.data.mongodb-api.com/app/data-ciszpbd/endpoint/data/v1/action/find"

payload = json.dumps(
    {
        "collection": "users",
        "database": "sample_mflix",
        "dataSource": "HedgeCluster",
        # "projection": {
        #     "_id": 1
        # }
    }
)
headers = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": "8gspnrEF5v9UOEmOPtEeSsYxDRvt77xW4tC469gxvmcP0NcydBA39PIxtbngJkxS",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
