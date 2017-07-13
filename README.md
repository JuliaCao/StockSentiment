# Stock Sentiment

_A Python-based web app designed to give portfolio managers up-to-the minute information about the news articles that affect their holdings. Uses IBM Watson to calculate the sentiment of articles and quickly and accurately displays the information to users using a simple color schema._

## Created for the 2017 BlackRock Intern Hackathon

### To Run:

In a Mac or Linux environment, run `./app.py` in the root directory. In Windows, run `path/to/python app.py` in the root directory.

### Dependencies: 

- `watson-developer-cloud`
- `pandas`
- `requests`
- `bs4`
- `sqlite3`
- `Flask`

_Note: You may have to use a separate Watson Bluemix account to use the Watson API. The app will function without one, since a sample database is included. However, you will not be able to load newer articles_

### Screenshot:

![Screenshot](https://github.com/anandnk24/stockSentiment/blob/master/img/screenshot.png?raw=true "Screenshot")


