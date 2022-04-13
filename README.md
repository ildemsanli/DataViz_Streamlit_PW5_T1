<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Data visualization on Streamlit

*Ildem Sanli & Eric Martinet*

**Data Analytics bootcamp @IronHack Paris, Feb-Apr 22**

## Content
- [Project Description](#project-description)
- [Tools](#tools)
- [Challenges and Highlights](#challenges-highlights)
- [Repo structure](#repo-structure)
- [Links](#links)

## Project description

The goal of this project is to conduct a complete analytics pipeline from data preparation to data vizualisation to data interpretation.

In our case, we worked on a HR Analytics dataset that provides information about people looking for a job.

## Tools

We used Python as the programming language and we used the following tools:

- Planification: Jira (kanban)
- Git repo: Github
- Data cleaning and preparation: Jupyter Notebook
- App framework: Streamlit
- App deployment: Heroku

## Challenges & Highlights

Considering that we had a limited dataset both in terms of records (about 2,000) and variables (a dozen), the **data cleaning & preparation part was relatively straightforward**.

However, we feel that we ended up **short of providing meaningful insights from this dataset**, as our analyses (correlation, Student's t-tests, ANOVA tests, etc.) pointed out to the same conclusion: if there is a reason for people to look for a new job, it is not captured in the variables provided in the dataset!

Also since, since the dataset's variables are **mostly categorical**, the number of graph types we can use in a relevant way is quickly limited. We created 12 charts:

- The first 8 charts give insights about the data we have.
- The last 4 charts show our analysis about likeliness of people to look for a new job.

Finally, this is our first project using **Streamlit**. While the tool is very convenient and easy to use, it still has some limitations that can only be overcome with complex workarounds. For instance, **you cannot really control the size of the figures** (an issue for pie charts in particular), as they automatically extend to the width of their container/column (and you cannot control this width as well). A workaround is to save each figure as an image in the buffer memory, and then render the image, but this is computationally expensive for limited benefits.

## Repo structure

Our repo is organised as follows:

- [data](./data): Original and cleaned datasets in CSV format
- [EDA](./EDA): 'Exploratory Data Analysis', with data cleaning and data vizualisation experiments
- [streamlit_dataviz.py](./streamlit_dataviz.py): Main app file

## Links

- [Original repository](https://github.com/eric-martinet/DataViz_Streamlit_PW5_T1)
- [App on Heroku] (https://dashboard.heroku.com/apps/ironhack-hranalytics)
