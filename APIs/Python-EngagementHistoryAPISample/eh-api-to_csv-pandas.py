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
#                https://<domain>/interaction_history/api/account/{accountID}/interactions/search?<url_parameters>
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

# Customize the body for what you want 
body={
	'interactive':'true',
	'ended':'true',
	'start':{
		# http://www.epochconverter.com/ - grab the millisecond version
		'from':'1451606399000', #Dec 31 2015
		'to':'1453334399000' #jan 15 2016
	},
	'skillIds': [
		# Skill ID is found in the URL when you click on a skill in LiveEngage
		12, 13, 14, # All English Sales 
		15, 16, 17 # All English Service
	]
}

# Fill our interactionRecords incrementally because can only pull 100 at a time.
count = 1
offset = 0
interactionRecords = []
while(offset <= count + 1):
	params={'offset':offset, 'limit':'100', 'start':'des'} # Prob shouldn't change offset and limit 
	engHistoryResponse = client.post(url=engHistoryURI, headers=postheader, data=json.dumps(body), auth=oauth, params=params)
	# content.decode() converts Response to String
	engHistoryDecoded = engHistoryResponse.content.decode()
	# json.loads converts JSON String to Python Dictionary.
	engHistoryResults = (json.loads(engHistoryDecoded))
	# Update count, offset, and records
	for record in engHistoryResults['interactionHistoryRecords']:
		interactionRecords.append(record)
	count = engHistoryResults['_metadata']['count']
	offset += 100 # Our limit is set to 100 in our query params 
	# print the status of the aggregation
	print(str(offset) + "<=" + str(count))

# Construct our dataframe
df_ = pandas.DataFrame(columns=["startTime", "endTime", "skillId", "agentId", "sdes", "transcriptLines"])			   

numRecords = 0
# Fill our dataframe 
for record in interactionRecords:
	numRecords += 1
	engagementId = record['info']['engagementId']
	df_.set_value(engagementId, "startTime", record['info']['startTime'])
	df_.set_value(engagementId, "endTime", record['info']['endTime'])
	df_.set_value(engagementId, "skillId", record['info']['skillId'])
	df_.set_value(engagementId, "agentId", record['info']['agentId'])
	df_.set_value(engagementId, "transcriptLines", record['transcript']['lines'])
	try:
		df_.set_value(engagementId, "sdes", record['sdes']['events'])
	except KeyError:
		df_.set_value(engagementId, "sdes", "N/A")
print("num records processed = " + str(numRecords))

#########################
### Output DataFrame ####
#########################

outfile = 'new_test.csv'

with open(outfile, 'w', encoding='utf-8') as f:
	# We could write the date and timeframe to the header, or just put it in the table itself. I think putting it in the table may be the better choice.
	#f.write('Date: ' + str(myDate) + '\nTimeframe: ' + myTime15Before + ' - ' + myTimeNow + '\n\n')
	# Add dataframe to output file
	df_.to_csv(f, sep='|', encoding='utf-8')

print("Output file: " + outfile)
print("--- %s seconds to complete script." % (time.time() - start_time_epoch))
