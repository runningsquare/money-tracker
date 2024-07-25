# MONEY TRACKER
## Description:
Money Tracker is a simple web application that helps users to track their money usage.
This Final project is inspired by the money tracker mobile applications widely available.
As managing our own personal finances is important, Money Tracker will be able to help users keep track of their own expenses and income and find patterns in their spendings and savings.
Hopefully this will be able to help users plan their finances more efficiently to achieve their personal financial goals.

## templates
The web app displays 4 html to the users; register.html, login.html, index.html and history.html.
"templates" also includes html files that are only viewable by the user when an error occurs.
Below are the purpose of the following htmls:

### index.html
This is the homepage which user will first see when they log in. Here, the users will be able to record down their expenses and income for the day.
The page have 3 sections; date, income and expenses. The date is a compulsary section where the users will be prompted to fill in the missing details if they are left blank.
When the user presses the submit button, their responses will be stored in the "MoneyTracker" database's "dailyLog" table.

The form's date section allows user to choose the date where they want to record their expenses and income.
Hence, if the user suddenly remembers they had an extra expense that they had not recorded the day befre, they are able to select the previous day's date and input the amount in the expenses accordingly.

### history.html
This page displays the user's total funds as well as their income and expenses for each day, in descending order according to the latest date.
The user's "funds" are cauculated by the total income the user inputs minus the total expenses that the user input.
Meanwhile, the "expenses" are cauculated by the sum of all the different types of expenses's amount the user inputted and the "income" are cauculated by the sum of all the different types of income's amount the user inputted

### apology.html
Users will be redirected to this page when they fail to input the required information. A message will appear, letting the user know which detail is missing or which detail has a unaccetable input. apology.html is for when users fail to give correct information in the login and register page.

### apology2.html
Users will be redirected to this page when they fail to input the required information. A message will appear, letting the user know which detail is missing or which detail has a unaccetable input. apology2.html is for when users fail to give correct information in the index or history page.

### layout.html
The head of the layout template includes tags needed for responsive mobile site. It also includes the javascript for side navigation bar's open and close function.
The body of layout templates includes 2 html paths, one for users who are not logged in and another for logged in users.

## helpers.py
helpers.py includes functions such as login_required, usd and check_input.
login_required: Ensures that users are logged in to visit the html page requested.
usd: Displays numbers in usd format.
check_input: Check whether expenses and salary inputs submitted in the index page are postitive integers or floats.

## MoneyTracker.db
This is the database used in the web application. It consists of 2 tables; users and dailyLog.
users: Stores user's username, hash password and funds.
dailyLog: Stores each user's input into the index page.

## Getting Started
### Prerequisites
We need pip3 to install our dependencies. Install pip3 if you haven't:
<br>
https://pip.pypa.io/en/stable/installation/

Install the following dependencies for the app:
- cs50
```
pip3 install cs50
```
- flask
```
pip3 install flask
```
- flask_session
```
pip3 install flask_session
```

### Installation / Running the App
Run the following commands to get started:
```
git clone https://github.com/runningsquare/money-tracker.git
```
```
cd your-project/
```
```
flask --app application run
```