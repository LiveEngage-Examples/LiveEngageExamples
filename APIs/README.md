# Java - Engagement History API
This is a basic example of how to connect to the Engagement History API in Java by using Scribe. In order to run the example you will need to update the EngagementHistory.java file with your Engagement History API credentials.

# Java - Transcript Send Email Example
This example uses the Engagement History API to access the chat transcripts for the previous day, parse the data, and then send out an individual email for each chat that occurred. The email contains all of the meta data tied to that chat and the chat transcript. 

This example also uses the Skill API and the Agent API to get the skill name, the name of the agent, and the email of the agent, and then adds that data to the email.

To send the email, this example uses a Gmail account to send out the emails.

### Run The Example
In order to run the example, you will need to have a Gmail account that you can use for sending out the emails, and you will need to have API keys for the Engagement History API. 

You will need to update the following files:
* SendEmailSingleChat.java - with your Gmail credentials
* AgentList.java - with your Engagement History API credentials
* SkillList.java - with your Engagement History API credentials
* IndividualChat.java  with your Engagement History API credentials

# Python - Engagement History API Example
This is a basic example of how to connect to the Engagement History API in Python by using the requests_oauthlib. In order to run this example you will need to update the ehapiExample.py file with your Engagement History API credentials.

# R - Engagement History API Example
This is a basic example of how to connect to the Engagement History API in R by using the httr library. In order to run this example you will need to update the rEngagementHistory.R file with your Engagement History API credentials.