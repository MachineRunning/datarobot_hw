from apiclient.discovery import build
## import OAuth2 authenticator
from oauth2client import client
from oauth2client.client import SignedJwtAssertionCredentials

from httplib2 import Http

import csv
import random ### used for some sampling of predictions

client_email = 'user_email@developer.gserviceaccount.com' #enter OAuth service email account
with open("My First Project-f36ba9711036.p12") as f: ## use the P12 key downloaded from the developers conole instead of a JSON key
  private_key = f.read()

### using a service email account and key create a credentials object
credentials = SignedJwtAssertionCredentials(client_email, private_key,scope=('https://www.googleapis.com/auth/prediction','https://www.googleapis.com/auth/devstorage.read_only'))

http_auth = credentials.authorize(Http()) ## using the credentials, login over http

service = build('prediction', 'v1.6',http=http_auth) ## request the prediction API v1.6

predApi=service.trainedmodels()  ## extract the trained models from the project

### (not needed for the perfect model experiment)
### read in a csv with out of sample data to test the trained model 
#with open('outOfSampleData_lags.csv', 'rb') as csvfile:
	#sampleDataReader = csv.reader(csvfile, delimiter='\n')
	#outSampleList = list(sampleDataReader)
	
## model names on cloud
## perfect_linear_model_test
##"hourly_load_prediction",
	
### due to usage quotas--sample rather than test the trained model over a year of data
#indices=random.sample(outSampleList ,k=200) ### sample just 200 hourly predictions

indices=range(1,100) ## for the perfect linear model experiment just test the first 100 indices
outList=list()
for hourIndex in indices:
	body = {'input': {'csvInstance': str(hourIndex)}} ### in my tests I was only able to request one prediction at a time
	### making one API request per prediction for my testing purposes was really inefficient
	### for example  body = {'input': {'csvInstance': [input,input,input, ...]}} or body = {'input': {'csvInstance': "input \n input \n ..."}}
	### but this does increase API usage...
	result = predApi.predict(body=body, id="hourly_load_prediction", project="teak-banner-92522").execute() ## send an input value, make a prediction using the specified trained model
	outList.append(float(result["outputValue"])) ### append the predicted value to outList
	
### write out the predictions to
with open('perfect_linear_predictions.csv', 'w') as fileHandle:
    a = csv.writer(fileHandle, delimiter=',')
    a.writerows(outList)

### (not needed for the perfect model experiment)
### save the sampled indices so verification can be retrieved
#with open('lag_model_selected_indices.csv', 'w') as fileHandle:
    #a = csv.writer(fileHandle, delimiter=',')
    #a.writerow(indices)
    
