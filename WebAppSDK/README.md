# Alias Widget
This is an example widget of how you can get all of the information on the Engagement Attributes and display them. The widget has an example of how you can give an engagement attribute an alias by pulling that variable and then displaying it with a different name.

The widget is built using Bootstrap, JQuery, and the Web App SDK.

You can view a live example here:[Alias Widget](https://scottwestover.herokuapp.com/liveengageWidgets/aliasWidget/)

# Chat Starting Page Widget
This is an example widget of how you can use and Engagement Attribute to pass the chat starting page URL to a Google Spreadsheet and then use that data for a custom report.

In order to use this widget, you will need to have a Google Account, that way you can host a spreadsheet on your Google Drive. Inside the Chat Starting Page Widget folder, you will see instructions on how to set this up.

# Multi Media Widget
This is an example of widget of how you can use the Web App SDK to send html code, send images, YouTube videos (sends an image of the video through chat that the visitor can click on to be taken to the YouTube video), and file sharing by using the Google Drive API.

To use the widget, you will need to update the example3.js file with your Google Drive API client Id. You can read more about the setting up the Drive API here: [Drive API](https://developers.google.com/drive/v2/web/quickstart/js)

You can view a live example here:[Multi-Media Widget](https://scottwestover.herokuapp.com/liveengageWidgets/MultiMediaWidget/)

# SDK Sample Widget
This is an example widget that shows how you can write chat lines to the agent console, get information from the agent console, and how you can bind data from the agent console.

Note: This sample widget was not created by me. I am sharing the source code here since it is no longer available through the original link.

You can view a live example here:[Multi-Media Widget](https://scottwestover.herokuapp.com/liveengageWidgets/SDKsampleWidget/)

# Translate Widget
This is an example widget of how you can have the chat lines translated to another language. The widget uses the Bing translator widget to translate the lines. 

The widget checks what skill the current chat is assigned to, and it will then translate the visitor chat lines to the correct language. It will also allow you to translate anything the agent types into the corresponding language.

To use the widget, you will need to have 2 skill groups set up: Russian and Spanish. If the chat is unskilled, then the translator will translate English into Spanish for the visitor, and Spanish into English for the agent.

You can view a live example here:[Translate Widget](https://scottwestover.herokuapp.com/liveengageWidgets/translateWidget/)