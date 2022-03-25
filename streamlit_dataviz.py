#### IMPORT LIBRAIRIES ####
from site import check_enableusersite
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
#from io import BytesIO


#### DATA IMPORT ####
data = pd.read_csv('./data/HR_Data_cleaned.csv')
data.drop('Unnamed: 0', axis = 1, inplace=True)


#### CATEGORICAL COLUMNS ORDERING ####
cats_education_level = ['Primary School', 'High School', 'Graduate', 'Masters', 'Phd', 'Unknown']
data.education_level = pd.Categorical(data.education_level, ordered = True, categories = cats_education_level)

cats_enrolled_university = ['No enrollment', 'Part time course', 'Full time course', 'Unknown']
data.enrolled_university = pd.Categorical(data.enrolled_university, ordered=True, categories=cats_enrolled_university)

cats_company_size = ['0-10', '10-49', '50-99', '100-500', '500-999', '1000-4999', '5000-9999', '10000+', 'Unknown']
data.company_size = pd.Categorical(data.company_size, ordered=True, categories=cats_company_size)

# The order of below categories is artificial (e.g. no <> relationship between Male and Female)
# and based on cardinality
# but it enables us to put 'Other' and 'Unknown' at the very right

cats_gender = ['Male', 'Female', 'Other', 'Unknown']
data.gender = pd.Categorical(data.gender, ordered=True, categories=cats_gender)

cats_major_discipline = ['STEM', 'Humanities', 'Business Degree', 'Arts', 'Other', 'No Major', 'Unknown']
data.major_discipline = pd.Categorical(data.major_discipline, ordered=True, categories=cats_major_discipline)

cats_company_type = ['Pvt Ltd', 'Public Sector', 'Funded Startup', 'Early Stage Startup', 'NGO', 'Other', 'Unknown']
data.company_type = pd.Categorical(data.company_type, ordered=True, categories=cats_company_type)


#### GLOBAL STREAMLIT LAYOUT ####
st.set_page_config(layout="wide")
st.title('HR ANALYTICS: PEOPLE LOOKING FOR A NEW JOB')

sns.set_theme(palette='muted')

cat_colors = sns.color_palette('muted')
cont_colors = sns.color_palette('crest')

figsize_std = (10,8)
figs=[plt.figure(figsize=figsize_std) for _ in range(0,12)] # 12 figures

# SELECTORS
genders = ['Male', 'Female']
gender_selection = st.sidebar.selectbox('Gender', genders)


# 1.1 PIE CHART
ax = figs[0].add_subplot(1,1,1)
dist = pd.DataFrame(data["gender"].value_counts())
ax.pie(dist.gender, labels=dist.index, colors=cat_colors, autopct='%1.1f%%', textprops={'fontsize': 10, 'fontweight' : 10, 'color' : 'Black'})

# 1. 2
ax = figs[1].add_subplot(1,1,1)
data_subset = data.loc[data['gender'] == gender_selection]
sns.histplot(data=data_subset, x="relevant_experience", multiple="dodge", shrink=0.5, ax = ax)
ax.set(ylabel='Number of people', xlabel='')


# 1.3
ax = figs[2].add_subplot(1,1,1)
sns.heatmap(pd.crosstab(data.major_discipline, data.education_level, normalize='index'), cmap=cont_colors, annot=True, ax=ax, fmt=".1%")
ax.set(xlabel = 'Education level', ylabel = 'Major')

# 1. 4
ax = figs[3].add_subplot(1,1,1)
sns.histplot(data.training_hours, ax = ax)
ax.set(xlabel = 'Number of training hours', ylabel = 'Number of people')

#
ax = figs[4].add_subplot(1,1,1)
sns.histplot(data.city_development_index, ax=ax)
ax.set(xlabel = 'City development index', ylabel = 'Number of people')

#
data['current_job_in_career'] = data.last_new_job / data.experience
ax = figs[5].add_subplot(1,1,1)
sns.histplot(data = data, x='current_job_in_career', alpha = 0.7, ax=ax)
ax.set(xlabel = 'Time in Current job relative to Total years of experience', ylabel = 'Number of people')


#
ax = figs[6].add_subplot(1,1,1)
sns.heatmap(pd.crosstab(data.company_size, data.company_type, normalize = True, margins=True), cmap=cont_colors, annot = True, fmt=".1%", ax = ax, vmin = 0.01, vmax = 0.25)
ax.set(xlabel = 'Company type', ylabel = 'Company size')

#
ax = figs[7].add_subplot(1,1,1)
sns.stripplot(x = "city_development_index", y="education_level", data = data, dodge=True, alpha=.25, ax = ax)
ax.set(xlabel = 'City development index', ylabel = 'Education level')

#
ax = figs[8].add_subplot(1,1,1)
sns.boxplot(x="last_new_job", y="experience", hue='target', data=data, palette='deep', ax =ax).set(title="", xlabel="Years at current position", ylabel="Experience")

#
ax = figs[9].add_subplot(1,1,1)

d1 = pd.DataFrame(data["target"].value_counts())
ax.pie(d1.target, labels=['Not looking', 'Looking'], colors=sns.color_palette("muted"), autopct='%1.1f%%', textprops={'fontsize': 10, 'fontweight' : 10, 'color' : 'Black'})


#
ax = figs[10].add_subplot(1,1,1)
sns.histplot(data = data.loc[data['target'] == 1], x='experience', stat = 'probability', ax=ax, color='red', kde=True, alpha = 0.5, bins = 21)
sns.histplot(data = data.loc[data['target'] == 0], x='experience', stat = 'probability', ax=ax, color='green', kde=True, alpha = 0.5, bins = 21)
ax.set(xlabel = 'Experience', ylabel = 'Probability')


#
ax = figs[11].add_subplot(1,1,1)
cols = data.select_dtypes(include=['category'])
dct = {}
for col in cols:
    l_subsets = []
    for cat in data[col].cat.categories:
        l_subsets.append(data.loc[data[col] == cat])
    fvalue, pvalue =stats.f_oneway(*[subset.target for subset in l_subsets])
    #print(data.groupby(by=col).target.mean())
    #print(pvalue)
    #print('-----------')
    dct[col] = pvalue

names = list(dct.keys())
values = list(dct.values())

sns.barplot(x = names, y = values, ax = ax)



##### FINAL LAYOUT ####

st.header('What does our dataset look like?')
container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        st.subheader('Gender distribution')
        st.write(figs[0])
    with col2:
        st.subheader('Number of people with relevant experience')
        st.write(figs[1])
        #buf = BytesIO()
        #figs[1].savefig(buf, format="png")
        #st.image(buf)

container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        st.subheader('Frequency of Education level by Major discipline.')
        st.write(figs[2])
    with col4:
        st.subheader('Distribution of training hours')
        st.write(figs[3])

container3 = st.container()
col5, col6 = st.columns(2)

with container3:
    with col5:
        st.subheader('Distribution of City development index')
        st.write(figs[4])
    with col6:
        st.subheader('Distribution of Time in Current job relative to Total years of experience')
        st.write(figs[5])

container4 = st.container()
col7, col8 = st.columns(2)

with container4:
    with col7:
        st.subheader('Relative distribution by Company type and size')
        st.write(figs[6])
    with col8:
        st.subheader('Level of education by City development index')
        st.write(figs[7])

st.markdown('''---''')

st.header('How likely is somebody to look for a new job?')
container5 = st.container()
col9, col10 = st.columns(2)

with container5:
    with col9:
        st.subheader('Proportion of people looking for a new job')
        st.write(figs[9])
    with col10:
        st.subheader('Likeliness to look for a job by Experience and Years at current position')
        st.write(figs[8])

container6 = st.container()
col11, col12 = st.columns(2)

with container6:
    with col11:
        st.subheader('Probability to look for a new job by Years of experience')
        st.write(figs[10])
    with col12:
        st.subheader('Histogram: Training hours')
        st.write(figs[11])