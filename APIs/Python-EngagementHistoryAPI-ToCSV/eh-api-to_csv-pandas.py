import requests
import json
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import time
import pandas

# Grab the time when the script starts.
start_time_epoch = time.time()

accountNum = 'xxxxxxxxx'
domain = 'xxxxxxxx.liveperson.net'
engHistoryURI = 'https://' + domain + '/interaction_history/api/account/' + accountNum + '/interactions/search?'

# oauth stuff
consumer_key = 'xxxxxx'
consumer_secret = 'xxxxxxx'
access_token = 'xxxxxxx'
access_token_secret = 'xxxxxxx'
oauth = OAuth1(consumer_key,
			   client_secret=consumer_secret,
			   resource_owner_key=access_token,
			   resource_owner_secret=access_token_secret,
			   signature_method='HMAC-SHA1',
			   signature_type='auth_header')

client = requests.session()
postheader = {'content-type': 'application/json'}

# Construct our dataframe
df_ = pandas.DataFrame(columns=["startTime", "endTime", "skillId", "agentId", "sdes", "transcriptLines"])

count = 1 # Count is the total num of records in the response
offset = 0 # offset is to keep track of the amount difference between what we've pulled so far and what the total is.
numRecords = 0
while(offset <= count + 1): # Grab the data incrementally because can only pull 100 at a time.
	
	# Complete the Requests.session POST
	params={'offset':offset, 'limit':'100', 'start':'des'} # Prob shouldn't change offset and limit 
	engHistoryResponse = client.post(url=engHistoryURI, headers=postheader, data=json.dumps(body), auth=oauth, params=params)
	engHistoryDecoded = engHistoryResponse.content.decode() # content.decode() converts Response to String
	engHistoryResults = (json.loads(engHistoryDecoded)) # json.loads converts JSON String to Python Dictionary.

	# Fill our dataframe 
	for record in engHistoryResults['interactionHistoryRecords']:
		# Update numRecords
		numRecords += 1
		engagementId = record['info']['engagementId']
		df_.set_value(engagementId, "startTime", record['info']['startTime'])
		df_.set_value(engagementId, "endTime", record['info']['endTime'])
		df_.set_value(engagementId, "skillId", record['info']['skillId'])
		df_.set_value(engagementId, "agentId", record['info']['agentId'])
		df_.set_value(engagementId, "transcriptLines", record['transcript']['lines'])
		# This is a good way to grab a value that may not exist
		try:
			df_.set_value(engagementId, "sdes", record['sdes']['events'])
		except KeyError:
			df_.set_value(engagementId, "sdes", "N/A")
	
	# Update count, offset
	count = engHistoryResults['_metadata']['count']
	offset += 100 # Our limit is set to 100 in our query params 
	# print the status of the aggregation 
	print(str(offset) + "<=" + str(count))	   

print("num records processed = " + str(numRecords))

#########################
### Output DataFrame ####
#########################

outfile = 'new_test.csv'

with open(outfile, 'w', encoding='utf-8') as f:
    df_.to_csv(f, sep='|', encoding='utf-8')

print("Output file: " + outfile)
print("--- %s seconds to complete script." % (time.time() - start_time_epoch))
