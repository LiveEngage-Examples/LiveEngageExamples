library(httr)

key <- '{YOUR API KEY}'
secret <- '{Your API Secret}'
tokenURL <- 'null'
accessTokenURL <- 'null'
authorizeURL <- 'null'

fbr <- oauth_app('fitbitR',key,secret)

sig <- sign_oauth1.0(fbr,
                     token="{YOUR API SECRET}",
                     token_secret="{YOUR TOKEN SECRET}"
)

body <- '{"start":{"from":1433140200000,"to":1435645800000}}'
test <- POST("https://{YOUR BASE URI}/interaction_history/api/account/{YOUR ACCOUNT NUMBER}/interactions/search?offset=0&limit=10",sig, body = body,add_headers("Content-Type"="application/json"))
content(test, "parsed")
myTest <- content(test,"parsed")
myTest$interactionHistoryRecords
