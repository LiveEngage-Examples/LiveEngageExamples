/*
 Web call needed to discover baseURI needed to call Users API for individual LiveEngage accounts for Accounts:
 This URL is for app keys that have Read/Write enabled on the API
 https://api.liveperson.net/api/account/{YOUR ACCOUNT NUMBER}/service/accountConfigReadWrite/baseURI.json?version=1.0
 This URL is for app keys that have Read Only enabled on the API 
 https://api.liveperson.net/api/account/{YOUR ACCOUNT NUMBER}/service/accountConfigReadOnly/baseURI.json?version=1.0
 Expected response example:
{
 "service":"accountConfigReadOnly",
 "account":"56072331",
 "baseURI":"va-a.acr.liveperson.net"
}
*/

// To run this example, you will need to install the Request module. 
// run -  npm install request

var request = require('request');

var oauth = {
        consumer_key: '530abebef7814b23bc314d9abe511465',
        consumer_secret: '3b48e7f644017990',
        token: 'bb52851835ad4e7ca70251c30afc696e',
        token_secret: '746275fd0cf02e1e'
    };

// Get a list of all the skills
// Example URL: https://va-a.ac.liveperson.net/api/account/56072331/configuration/le-users/skills?v=1
var url = 'https://{YOUR BASE URI}/api/account/{YOUR ACCOUNT NUMBER}/configuration/le-users/skills?v=1';
request.get({
    url: url,
    oauth: oauth,
    json: true,
    headers: {
        'Content-Type': 'application/json'
    }
}, function (e, r, b) {
    console.log(JSON.stringify(b));
});

// Get all of the information for a single skill
// Example URL: https://va-a.ac.liveperson.net/api/account/56072331/configuration/le-users/skills/2?v=1
url = 'https://{YOUR BASE URI}/api/account/{YOUR ACCOUNT NUMBER}/configuration/le-users/skills/{SKILL ID}?v=1';
request.get({
    url: url,
    oauth: oauth,
    json: true,
    headers: {
        'Content-Type': 'application/json'
    }
}, function (e, r, b) {
    console.log(JSON.stringify(b));
});