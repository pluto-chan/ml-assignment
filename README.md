# ml-assignment

This repository contains a test assignment. 

You can create and run the docker image with the following commands: 
```cmd
docker build -t space-ml-test .
docker run -d --name spacemlcontainer -p 80:80 space-ml-test
```

In this case the server will run on localhost. 

PUT method on /process-feature can be called to process the features.

It accepts JSON of this format: 

```json
{
  "id": 0, 
  "application_date": "string",
  "contracts": "string"
}
```

Contracts should contain a raw JSON string.

process_features_from_csv.py is an example where I've processed the data provided with the task. You can find the results in data_with_new_features.csv.



