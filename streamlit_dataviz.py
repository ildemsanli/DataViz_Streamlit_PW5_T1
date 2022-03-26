#### IMPORT LIBRAIRIES ####
from site import check_enableusersite
from turtle import forward
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


#### DATA IMPORT ####
data_import = pd.read_csv('./data/HR_Data_cleaned.csv')
data_import.drop('Unnamed: 0', axis = 1, inplace=True)


#### CATEGORICAL COLUMNS ORDERING ####
cats_education_level = ['Primary School', 'High School', 'Graduate', 'Masters', 'Phd', 'Unknown']
data_import.education_level = pd.Categorical(data_import.education_level, ordered = True, categories = cats_education_level)

cats_enrolled_university = ['No enrollment', 'Part time course', 'Full time course', 'Unknown']
data_import.enrolled_university = pd.Categorical(data_import.enrolled_university, ordered=True, categories=cats_enrolled_university)

cats_company_size = ['0-10', '10-49', '50-99', '100-500', '500-999', '1000-4999', '5000-9999', '10000+', 'Unknown']
data_import.company_size = pd.Categorical(data_import.company_size, ordered=True, categories=cats_company_size)

# The order of below categories is artificial (e.g. no <> relationship between Male and Female)
# and based on cardinality but it enables us to consistently place 'Other' and 'Unknown'

cats_gender = ['Male', 'Female', 'Other', 'Unknown']
data_import.gender = pd.Categorical(data_import.gender, ordered=True, categories=cats_gender)

cats_major_discipline = ['STEM', 'Humanities', 'Business Degree', 'Arts', 'Other', 'No Major', 'Unknown']
data_import.major_discipline = pd.Categorical(data_import.major_discipline, ordered=True, categories=cats_major_discipline)

cats_company_type = ['Pvt Ltd', 'Public Sector', 'Funded Startup', 'Early Stage Startup', 'NGO', 'Other', 'Unknown']
data_import.company_type = pd.Categorical(data_import.company_type, ordered=True, categories=cats_company_type)


#### GLOBAL STREAMLIT LAYOUT ####
st.set_page_config(layout="wide")
st.title('HR ANALYTICS: PEOPLE LOOKING FOR A NEW JOB')

sns.set_theme(palette='pastel', style = 'ticks')
sns.set_style({'axes.grid': True,'grid.color': 'lightgrey', 'grid.linestyle': ':', 'axes.spines.right': False,
 'axes.spines.top': False})

cat_colors = sns.color_palette('pastel')
cont_colors = sns.color_palette('crest')

figsize_std = (6,4)
figs=[plt.figure(figsize=figsize_std) for _ in range(0,12)] # 12 figures

# SIDE BAR SELECTORS
st.sidebar.header('Axes selector')

selector_gender = st.sidebar.multiselect('Gender', list(data_import.gender.cat.categories), default=list(data_import.gender.cat.categories))
selector_relevant_experience = st.sidebar.multiselect('Relevant experience', list(data_import.relevant_experience.unique()), default=list(data_import.relevant_experience.unique()))
selector_enrolled_university = st.sidebar.multiselect('At university?', list(data_import.enrolled_university.cat.categories), default=list(data_import.enrolled_university.cat.categories))
selector_education_level = st.sidebar.multiselect('Education level', list(data_import.education_level.cat.categories), default=list(data_import.education_level.cat.categories))
selector_major_discipline = st.sidebar.multiselect('Major discipline', list(data_import.major_discipline.cat.categories), default=list(data_import.major_discipline.cat.categories))
selector_company_size = st.sidebar.multiselect('Company size', list(data_import.company_size.cat.categories), default=list(data_import.company_size.cat.categories))
selector_company_type = st.sidebar.multiselect('Company type', list(data_import.company_type.cat.categories), default=list(data_import.company_type.cat.categories))

mask_gender = data_import.gender.isin(selector_gender)
mask_relevant_experience = data_import.relevant_experience.isin(selector_relevant_experience)
mask_enrolled_university = data_import.enrolled_university.isin(selector_enrolled_university)
mask_education_level = data_import.education_level.isin(selector_education_level)
mask_major_discipline = data_import.major_discipline.isin(selector_major_discipline)
mask_company_size = data_import.company_size.isin(selector_company_size)
mask_company_type = data_import.company_type.isin(selector_company_type)

mask = mask_gender * mask_relevant_experience * mask_enrolled_university * mask_education_level * mask_major_discipline * mask_company_size * mask_company_type

if np.any(mask):
    data = data_import.loc[mask].copy()
else:
    data = data_import.copy()

# 1.1 GENDER
ax = figs[0].add_subplot(1,1,1)
dist = pd.DataFrame(data["gender"].value_counts())
ax.pie(dist.gender, labels=dist.index, colors=cat_colors, autopct='%1.1f%%')

# 1.2 RELEVANT EXPERIENCE
ax = figs[1].add_subplot(1,1,1)
sns.countplot(data=data, x="relevant_experience", ax = ax)
ax.set(ylabel='Number of people', xlabel='')

# 1.3 BYEDUCATION LEVEL AND MAJOR DISCIPLINE
ax = figs[2].add_subplot(1,1,1)
sns.heatmap(pd.crosstab(data.major_discipline, data.education_level, normalize=True, margins = True), cmap=cont_colors, annot=True, ax=ax, fmt=".1%", vmin = 0.01, vmax = 0.25)
ax.set(xlabel = 'Education level', ylabel = 'Major')

# 1.4 TRAINING HOURS
ax = figs[3].add_subplot(1,1,1)
sns.histplot(data.training_hours, ax = ax, alpha = 1, binwidth=10, binrange=(0, max(data.training_hours)))
ax.set(xlabel = 'Number of training hours', ylabel = 'Number of people', xlim = (0, None))

# 1.5 CITY DEVELOPMENT INDEX
ax = figs[4].add_subplot(1,1,1)
sns.histplot(data.city_development_index, ax=ax, alpha = 1, binwidth=0.05, binrange=(0.5, 1))
ax.set(xlabel = 'City development index', ylabel = 'Number of people', xlim = (0.5,1))

#1.6 CURRENT JOB AS % OF TOTAL CAREER
data['current_job_in_career'] = data.last_new_job / data.experience
ax = figs[5].add_subplot(1,1,1)
sns.histplot(data = data, x='current_job_in_career', alpha = 1, ax=ax, binwidth=0.05, binrange=(0, 1))
ax.set(xlabel = 'Time in Current job as % of Total years of experience', ylabel = 'Number of people', xlim=(0,1))

# 1.7 FREQUENCY BY COMPANY TYPE & SIZE
ax = figs[6].add_subplot(1,1,1)
sns.heatmap(pd.crosstab(data.company_size, data.company_type, normalize = True, margins=True), cmap=cont_colors, annot = True, fmt=".1%", ax = ax, vmin = 0.01, vmax = 0.25)
ax.set(xlabel = 'Company type', ylabel = 'Company size')

# 1.8 LEVEL OF EDUCATION BY CITY DEVELOPMENT INDEX
ax = figs[7].add_subplot(1,1,1)
sns.stripplot(x = "city_development_index", y="education_level", data = data, dodge=True, alpha=.25, ax = ax)
ax.set(xlabel = 'City development index', ylabel = 'Education level')

# 2.1 PROPORTION OF PEOPLE LOOKING FOR A NEW JOB
ax = figs[8].add_subplot(1,1,1)
d1 = pd.DataFrame(data["target"].value_counts())
ax.pie(d1.target, labels=['Not looking', 'Looking'], autopct='%1.1f%%')

# 2.2 EXPERIENCE VS. YEARS IN CURRENT POSITION VS. NEW JOB SEEKER
ax = figs[9].add_subplot(1,1,1)
sns.boxplot(x="last_new_job", y="experience", hue='target', data=data, ax =ax)
ax.set(xlabel="Years at current position", ylabel="Experience")

# 2.3 PROBABILITY TO LOOK FOR A NEW JOB BY YEARS OF EXPERIENCE
ax = figs[10].add_subplot(1,1,1)
sns.lineplot(data = data, x='experience', y='target', ax=ax, color = cat_colors[1] )
ax.set(xlabel = 'Years of Experience', ylabel = 'Probability', xlim = (0, 21))


# 2.4 ANOVA TEST: P-VALUE BY VARIABLES
ax = figs[11].add_subplot(1,1,1)
cat_cols = data.select_dtypes(include=['category'])
dct_anova = {}
for col in cat_cols:
    l_subsets = []
    for cat in data[col].cat.categories:
        l_subsets.append(data.loc[data[col] == cat])
    fvalue, pvalue =stats.f_oneway(*[subset.target for subset in l_subsets])
    dct_anova[col] = pvalue

names = [key.replace('_', ' ').capitalize() for key in dct_anova.keys()]
values = list(dct_anova.values())

sns.barplot(x = names, y = values, ax = ax, color = cat_colors[0])
ax.set_xticklabels(names, rotation= 60)
sns.lineplot(x = names, y=0.05, ax = ax, color = 'red')



##### FINAL LAYOUT ####

st.header('What does our dataset look like?')
container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        st.subheader('By Gender')
        st.write(figs[0])
        st.write('Comments')
    with col2:
        st.subheader('By Relevant experience')
        st.write(figs[1])
        st.write('Comments')

container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        st.subheader('By Education level and Major discipline')
        st.write(figs[2])
        st.write('Comments')
    with col4:
        st.subheader('By Training hours')
        st.write(figs[3])
        st.write('Comments')

container3 = st.container()
col5, col6 = st.columns(2)

with container3:
    with col5:
        st.subheader('By City development index')
        st.write(figs[4])
        st.write('Comments')
    with col6:
        st.subheader('By Relative duration in current job')
        st.write(figs[5])
        st.write('Comments')

container4 = st.container()
col7, col8 = st.columns(2)

with container4:
    with col7:
        st.subheader('By Company type and size')
        st.write(figs[6])
        st.write('Comments')
    with col8:
        st.subheader('By Level of education and City development index')
        st.write(figs[7])
        st.write('Comments')

st.markdown('''---''')

st.header('How likely is somebody to look for a new job?')
container5 = st.container()
col9, col10 = st.columns(2)

with container5:
    with col9:
        st.subheader('Proportion of people looking for a new job')
        st.write(figs[8])
        st.write('Comments')
    with col10:
        st.subheader('By Experience and Years at current position')
        st.write(figs[9])
        st.write('Comments')

container6 = st.container()
col11, col12 = st.columns(2)

with container6:
    with col11:
        st.subheader('By Years of Experience')
        st.write(figs[10])
        st.write('Comments')
    with col12:
        st.subheader('ANOVA test: p-values by variables')
        st.write(figs[11])
        st.write('All p-values are much higher than 0.05, so none of these variables can explain the likeliness to look for a new job.')