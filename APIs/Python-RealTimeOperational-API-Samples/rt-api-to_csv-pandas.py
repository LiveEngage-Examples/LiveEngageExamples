import requests
import json
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import time
import datetime
import pandas

####################
### Boiler Plate ###
####################

# Grab the time when the script starts.
start_time_epoch = time.time()

# Timeframe for the Real Time API's is 15 minutes
dataTimeframe = '15'

# Client's account number
accountNumber = '12345678'

agentActivityURI = 'https://va.data.liveperson.net/operations/api/account/' + accountNumber + '/agentactivity?timeframe=' + dataTimeframe + '&skillIds=all&agentIds=all&v=1'
engActivityURI = 'https://va.data.liveperson.net/operations/api/account/' + accountNumber + '/engactivity?timeframe=' + dataTimeframe + '&v=1&skillIds=all&agentIds=all'
queueHealthURI = 'https://va.data.liveperson.net/operations/api/account/' + accountNumber + '/queuehealth?timeframe=' + dataTimeframe + '&v=1&skillIds=all'
skillURI = 'https://base.liveperson.net/api/account/' + accountNumber + '/skills?v=1'

consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxx'

client = requests.session()
postheader = {'content-type': 'application/json'}
oauth = OAuth1(consumer_key,
			   client_secret=consumer_secret,
			   resource_owner_key=access_token,
			   resource_owner_secret=access_token_secret,
			   signature_method='HMAC-SHA1',
			   signature_type='auth_header')
agentActivityResponse = client.get(url=agentActivityURI, headers=postheader, auth=oauth)
engActivityResponse = client.get(url=engActivityURI, headers=postheader, auth=oauth)
queueHealthResponse = client.get(url=queueHealthURI, headers=postheader, auth=oauth)
skillResponse = client.get(url=skillURI, headers=postheader, auth=oauth)

# content.decode() converts Response to String. json.loads converts JSON String to Python Dictionary.
agentActivityResults = json.loads(agentActivityResponse.content.decode())
engActivityResults = json.loads(engActivityResponse.content.decode())
queueHealthResults = json.loads(queueHealthResponse.content.decode())
skillResults = json.loads(skillResponse.content.decode())

# gather date and time
myDate = datetime.date.today()
myTimeNow = time.strftime('%H:%M', time.localtime(start_time_epoch))
myTime15Before = time.strftime('%H:%M', time.localtime(start_time_epoch - 900))
myTimeFrame = myTime15Before + ' - ' + myTimeNow
myTimeZone = time.strftime('%Z', time.localtime(start_time_epoch))
	
########################
## Gather KPI Data   ###
## & Build DataFrame ###
########################

# Build a list of our skills
skillIDs = []
for skill in queueHealthResults['skillsMetrics']:
	skillIDs.append(skill)

# Print skills to console, just to confirm.			
print("We're working with these skills: " + ', '.join(skillIDs))

# if there are skills active, do the below
if skillIDs:

	# Construct our dataframe. The rows are our skills. The columns are our KPI's.
	df_ = pandas.DataFrame(index=skillIDs, columns=["skill_name", "date", "timeframe", "timezone", "staff", "chats", "chats_answered", "abandoned", "average_speed_to_answer", "total_handling_time", "average_handling_time"])

	# Match skill ID to skill name. Input the skill name in our dataframe.
	for skillData in skillResults['Skill']:
		for skill in skillIDs:
			if skillData['id'] == skill:
				df_.set_value(skill, "skill_name", skillData['name'])

	# Insert our date and time info into the dataframe using our start_time_epoch
	for skill in skillIDs:
		df_.set_value(skill, "date", myDate)
		df_.set_value(skill, "timeframe", myTimeFrame)
		df_.set_value(skill, "timezone", myTimeZone)
		

	# Add Chats, ChatsAnswered, abandoned, & Average Speed to Answer to our dataframe
	for skill in queueHealthResults['skillsMetrics']:
		# Grab our values from the data. Calculate abandoned manually.
		chats = queueHealthResults['skillsMetrics'][skill]['enteredQEng']
		chatsAnswered = queueHealthResults['skillsMetrics'][skill]['connectedEng']
		abandoned = chats - chatsAnswered
		avgTimeToAnswer = queueHealthResults['skillsMetrics'][skill]["avgTimeToAnswer"]
		# Set our values in the correct spot in our dataframe.
		### dataframe.set_value(index, column, myDataToPutThere)
		if chats:
			df_.set_value(skill, "chats", chats)
		else:
			df_.set_value(skill, "chats", 0)
		if chatsAnswered:
			df_.set_value(skill, "chats_answered", chatsAnswered)
		else:
			df_.set_value(skill, "chats_answered", 0)
		df_.set_value(skill, "abandoned", abandoned)
		if avgTimeToAnswer:
			df_.set_value(skill, "average_speed_to_answer", avgTimeToAnswer)
		else:
			df_.set_value(skill, "average_speed_to_answer", 0)

	# Calculate & add Average Handling Time to our dataframe
	for skill in engActivityResults['skillsMetricsPerAgent']['metricsPerSkill']:
		# Get total handling time and put it in our data frame
		totalHandlingTime = engActivityResults['skillsMetricsPerAgent']['metricsPerSkill'][skill]['metricsTotals']['totalHandlingTime']
		if totalHandlingTime:
			df_.set_value(skill, "total_handling_time", totalHandlingTime)
		else:
			df_.set_value(skill, "total_handling_time", 0)
		# avg_handling_time = totalHandlingTime / number_of_chats
		### numChatsAnswered is already in our dataframe. We grab that data with dataframe.loc[index][column]
		numChatsAnswered = df_.loc[skill]['chats_answered']
		avg_handling_time = totalHandlingTime / numChatsAnswered
		df_.set_value(skill, "average_handling_time", avg_handling_time)

	# Determine number of interactive Staff. Input into dataframe.
	for skill in engActivityResults['skillsMetricsPerAgent']['metricsPerSkill']:
		total_active_agents = 0
		# For each agent in our data, if they have any amount of interactive handling time, add them to number of staff.
		for agent in engActivityResults['skillsMetricsPerAgent']['metricsPerSkill'][skill]['metricsPerAgent']:
			if engActivityResults['skillsMetricsPerAgent']['metricsPerSkill'][skill]['metricsPerAgent'][agent]['totalHandlingTime'] != '0':
				total_active_agents += 1
		df_.set_value(skill, "staff", total_active_agents)

#if there are no skills active, build a dummy table
else:
	null_index = ["N/A"]
	df_ = pandas.DataFrame(index=null_index, columns=["skill_name", "date", "timeframe", "timezone", "staff", "chats", "chats_answered", "abandoned", "average_speed_to_answer", "total_handling_time", "average_handling_time"])
	df_.set_value("N/A", "skill_name", "All Offline")	
	df_.set_value("N/A", "date", myDate)
	df_.set_value("N/A", "timeframe", myTimeFrame)
	df_.set_value("N/A", "timezone", myTimeZone)
	df_.set_value("N/A", "staff", 0)
	df_.set_value("N/A", "chats", 0)
	df_.set_value("N/A", "chats_answered", 0)
	df_.set_value("N/A", "abandoned", 0)
	df_.set_value("N/A", "average_speed_to_answer", 0)
	df_.set_value("N/A", "total_handling_time", 0)
	df_.set_value("N/A", "average_handling_time", 0)

#########################
### Output DataFrame ####
#########################

# Construct our output file name
outfile = 'new_test.csv'

with open(outfile, 'w') as f:
	# We could write the date and timeframe to the header, or just put it in the table itself. I think putting it in the table may be the better choice.
	#f.write('Date: ' + str(myDate) + '\nTimeframe: ' + myTime15Before + ' - ' + myTimeNow + '\n\n')
	# Add dataframe to output file
	df_.to_csv(f)

# Print to console.
print("Output file: " + outfile)
print("--- %s seconds to complete script." % (time.time() - start_time_epoch))
