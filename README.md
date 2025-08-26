# Tabbylitics

An interactive Streamlit app for analysing survey data with clarity and a dash of cattitude.

#### Video Demo:  https://youtu.be/mxdx9UozB_A

#### Description:

Tabbylitics is a lightweight, interactive analytics tool built with Streamlit that transforms survey responses into clear, actionable insights. Designed for flexibility and ease of use, Tabbylitics allows users to explore survey results dynamically through intuitive visualisations and comparative analysis.

##### Technology stack:

Python (backend)
Streamlit (UI)
Plotly (charting)
Matplotlib (math)
Pandas (data cleaning)

Tabbylitics aims to allow people wanting to understand their survey data spin up the app fairly quickly. Many of modern survey tools provide you with survey results but the result analysis may be limited or require other tools or skills.

Tabbylitics features horizontal bar charts and heatmap tables. It uses those for comparative analysis to gain insights into survey data. 

The key defining feature is the copmarisons between different dimentions of questions, not only it provides analysis on single questions, but also allows users to compare question answers on dual axes. 

It handles single-choice questions, and multiple choice questions, ensuring each individual answer is accounted for. It handles free text questions and scale questions separately so that users get the correct insights. 

Where did the name come from? It is dedicated to my awesome cat Tiddles; "Tabbylitics" = cat pun + analytics 

##### Key Features

* Dropdown to select any survey question.
* Bar chart of responses (sorted, percentages on bars).
* Heatmap-style table (counts + percentages, color coded).
* Comparative analysis across dimensions (e.g., gender vs. location).
* Support for multiple question types:
    * Single choice / multi-choice → bar chart + table
    * Scale questions → average score + % of max, optionally split by another dimension
    * Free-text → displayed as response list, optionally grouped


#### Project Structure

app.py 

This is the main entry point where the app is created and deployed. It contains streamlit logic that creates sidebars, dropdowns, charts and tables. For multiple surveys, the advice would be to have individual app files for each, ensuring it is reading the relevant source. 

/data

This is where the raw data is stored for the app. There can be multiple sources for multiple surveys. Advice: store data in csv format. The app needs clean and error free and structured data. Raw data may need to have an additional pre-step to be sorted. 

question_catalogue.py

Dictionary that maps each survey question to metadata (type: single-choice, multi-choice, scale, free-text oor additional if required). Helps the app decide how to display results, also some results are question type dependent, therefore defining the dictionary is very important for dynamic querying. 

data_loader.py 

Loads data from the data folder and assigns it to a pandas data frame. 

unified_dataset.py

used for two purposes to process survey data. 

The first one is addressing is issue with the way multiple-choice, multiple-answer questions are handled. These questions alow userts to answer with multiple choices, where in the dataset the answers are delimited with pip " | ". This particular file processes these answers and creates a new dataframe where each answer for the question is split into rows, maintaining the respondent id grouped. 

The second part to data processing in this file is the processing of remaining questions and answers into the same dataframe as above so that in the end the dataframe is sorted into "Respondent ID", "Question", "Answer" formated columns. 

#### Design Choices & Future Developments

##### Design Choices 

Why Streamlit? - Chosen for simplicity and speed of prototyping dashboards. Minimal boilerplate vs. Flask/Django.

Why Plotly for charts? - Interactivity and easy labeling made Plotly preferable to Matplotlib. Bar charts easier to read horizontally, sorted by response size.

Why heatmap tables via Pandas Styler? - Helps highlight response distribution visually. Chose percentages for comparability across groups.

Why handle question types differently? - Free-text raw display makes more sense than forcing into charts. There is future development options here with LLMs. 

Why the current data model? - Chose a tidy, respondent-question-answer format for flexibility. Enables easy pivoting, grouping, and cross-tabulations.

##### Future Developments 

1. Develop an LLM connector for Streamlit
    - Free text processing via LLM. Ability to summarise free text into a descriptive paragraph.
    - Question-Answer data description. Ability for an LLM to describe the data via a prompt. 

2. Advance visualisations. Add options to view data in different types of charts.


#### How to Run the Project

# Clone repository
git clone https://github.com/your-username/tabbylitics.git
cd tabbylitics

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py