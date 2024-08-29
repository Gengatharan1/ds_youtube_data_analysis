# YouTube Data Harvesting and Warehousing using SQL and Streamlit

## Description
A Streamlit application that allows users to access and analyze data from multiple YouTube channels.

## Table of Contents
- [YouTube Data Harvesting and Warehousing using SQL and Streamlit](#youtube-data-harvesting-and-warehousing-using-sql-and-streamlit)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Softwares needed](#softwares-needed)
    - [Code](#code)
    - [Python packages](#python-packages)
    - [Environment\_variables](#environment_variables)
    - [Database Setup](#database-setup)
    - [Run App](#run-app)
  - [Workflow](#workflow)
    - [Scraping](#scraping)
    - [Migration](#migration)
    - [Ask Questions](#ask-questions)
    - [Analyse](#analyse)
  - [Contact](#contact)

## Setup
### Softwares needed
1. IDE (VS Code)
2. Python
3. Git (with git bash)

### Code

Clone this repository and ```cd``` into that directory
``` 
git clone https://github.com/Gengatharan1/youtube_data_harvesting.git
cd youtube_data_harvesting
```

### Python packages

Install all necessary packages
``` 
pip install -r requirements.txt
```

### Environment_variables
Creating ```.env``` file using template
``` 
cp env_template.txt .env
```

### Database Setup

Create a app and collection in MongoDB Atlas and add its credentials in ```.env``` file.

Create a local sql database and add its credentials in ```.env``` file

### Run App
``` 
streamlit run Intro.py
```

## Workflow
[Slides]()

### Scraping
### Migration
### Ask Questions
### Analyse

## Contact
[LinkedIn](https://www.linkedin.com/in/gengatharan007/)

---
^ [Back to table of contents](#table-of-contents)