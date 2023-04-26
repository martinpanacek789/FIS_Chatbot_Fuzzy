# FIS Chatbot
## Introduction
This repository contains a demo chatbot app for the website of the Faculty of Information Technologies and Statistics at
Prague University of Economics and Business developed as a project during one of the master courses. 

## Architecture
- The demo UI including the evaluation framework is built with [Streamlit](https://streamlit.io/), a popular, easy to use Python library for building data apps.
- The multi-language feature is implemented using the DeepL API.
- The chatbot itself is a simple rule-based decision framework with two-stage intent classification using a fuzzy string matching algorithm from [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/) package and a simple keyword-based approach.

## Possible extensions / upgrades
- Defining more intents, adding more answers.
- Using a more sophisticated intent classification model (e.g. fine-tuned BERT).
- Using named entity recognition to extract entities from user input and use them in the answers.
- Implementing a database to store the inputs and returned answers.
- Query school system API / database to get more information about the students (e.g. their grades, study progress, etc.).
- While the logic of retrieving location for classrooms is correct, it is not restricted to existing classrooms now. 
Querying a database of existing locations first would prevent it from generating non-existing locations (e.g. 9th floor, which does not exist in reality.)

## How to run the app
- The app is currently deployed on [Streamlit Cloud](https://martinpanacek789-fis-chatbot-fuzzy-fis-chatbot-mdum4m.streamlit.app/).
- To run the app locally, feel free to clone this repository, install requirements and run the app with `streamlit run FIS_Chatbot.py` 
command in the command line.
- For the multi-language feature with local deployment, a DeepL API key is required. You can get one for free [here](https://www.deepl.com/pro#developer). 
Such key needs to be added into a secrets.toml file as described [here](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)