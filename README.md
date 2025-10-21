# STRING ANALYZER

## Overview

String Analyzer is a small utility that inspects and summarizes text input. It reports common string metrics (length, word count, unique characters, character frequency), detects palindromes, and provides filter-supporting, rate-limited views to the analyzed strings.


## Installation

* Clone the repository:
```bash
git clone https://github.com/Tha-Orakkle/hng-task-1-string-analyzer.git
cd hng-task-1-string-analyzer
```
* Create and activate virtual env
```bash
python3 -m venv venv
source venv/bin/activate # Linux/MacOs
venv\bin\activate.bat # Windows
```
* Install dependencies
```bash
pip install -r requirements.txt
```
* set environmnet variables

Add the following variables to your `.env` file
```bash
SECRET_KEY='your_secret_key'
DEBUG=True
```
* Run server
```bash
python manage.py runserver
```


## Endpoints
* **POST** `/strings` - Creates/Analyze a string

* **GET** `/strings/{string_value}/` - Get Specific String

* **DELETE** `/strings/{string_value}` - Delete Specific String

* **GET** `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a` - Get All Strings with Filtering

* **GET** `/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings` - Natural Language Filtering

**For response formats for each endpoint, visit the documentation page `http://127.0.0.1/docs/`**

## API Documentation
Visit `http://127.0.0.1/` for documentation.


## Author
username: tha_orakkle <br>
email: adegbiranayinoluwa.paul@yahoo.com