import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from PIL import Image

df = pd.read_csv('survey.csv')
drop_cols = ['Other', 'Other.1', 'Other.2', 'Other.3', 'Other.4', 'Other.5', 'Network ID', 'Start Date (UTC)', 'Submit Date (UTC)', '#']
df.drop(columns = drop_cols, inplace=True)
st.set_option('deprecation.showPyplotGlobalUse', False)



st.title('What Do Tech Workers Think About Tech?')
st.subheader('An Analysis of A Popular Tech Twitter Survey by Sriram Krishnan + [Tyler Richards](http://tylerjrichards.com)')

st.markdown('Last week, Sriram decided to survey his many twitter followers about a large collection of world issues, from climate change to nuclear power to even if they think tech giants do good for the world. This suvey went fairly viral, getting thousands of respondents over the course of a week.')
st.markdown('   ')
st.markdown('   ')
image = Image.open('screenshot.png')
st.image(image, use_column_width=True)
st.markdown('   ')
st.markdown('   ')
st.markdown('The rest of this app is designed to showcase a brief analysis of this data. Want to just play around with the data yourself? Scroll down to the bottom for an interactive histogram.')

st.subheader('Who Took This Survey?')
st.markdown('This survey starts out by asking numerous questions about the survey respondents, from gender to occupation to college major.')
st.markdown('This group is overwhelmingly US based (82% US based, SF Bay Area at 37%), college educated (85% college grad, 33% finished grad school) with a CS major (47%),  male (73%), and in tech (92%). Two distributions are particularly interesting, the college degree distribution and the socioeconomic class that the respondents identified as growing up in.')

sns.countplot(df['How would you characterize your parents\' socioeconomic status when you were 10?'], palette='viridis', order = ['Poor', 'Working class', 'Lower middle class', 'Middle class', 'Upper middle class', 'Upper class'])
plt.title('Socioeconomic Status')
plt.xlabel('')
plt.ylabel('count')
plt.xticks(rotation=55)
st.pyplot()

st.markdown('The majority of the respondents grew up in middle class or upper middle class households, there were roughly 3x the upper middle class upbringing respondents compared to those that grew up in the working class. My guess is that this is also representative broadly of the tech industry.')

sns.countplot(df['What was your major?'], order=['CS','Liberal arts', 'Hard science', 'Economics', 'Math', 'Philosophy'], palette='viridis')
plt.title('College Major')
plt.xticks(rotation=45)
st.pyplot()

st.subheader('Which Tech Companies Do Good For The World?')
st.markdown('The next section of this survey asked which companies (Amazon, Apple, Uber, Google, Facebook, and Twitter) were doing good for the world.')
my_dict = {'Strongly agree': 2, 'Agree': 1, 'Unsure': 0, 'Disagree': -1, 'Strongly disagree':-2}
df['Amazon_good'] = df['After weighing all the pros and cons, Amazon has been good for the world.'].map(my_dict)
df['Uber_good'] = df['After weighing all the pros and cons, Uber has been good for the world.'].map(my_dict)
df['Facebook_good'] = df['After weighing all the pros and cons, Facebook has been good for the world.'].map(my_dict)
df['Google_good'] = df['After weighing all the pros and cons, Google/Alphabet has been good for the world.'].map(my_dict)
df['Apple_good'] = df['After weighing all the pros and cons, Apple has been good for the world.'].map(my_dict)
df['Twitter_good'] = df['After weighing all the pros and cons, Twitter has been good for the world.'].map(my_dict)
df_grouped_amzn = pd.DataFrame(df['Amazon_good'].value_counts(normalize=True)).reset_index()
df_grouped_amzn.columns = ['rating', 'perc']
df_grouped_amzn['company'] = 'Amazon'
col_list_remainder = ['Uber_good', 'Facebook_good', 'Apple_good', 'Twitter_good']
for i in col_list_remainder:
    df_temp = pd.DataFrame(df[i].value_counts(normalize=True)).reset_index()
    df_temp.columns = ['rating', 'perc']
    df_temp['company'] = i.split('_')[0]
    df_grouped_amzn = pd.concat([df_grouped_amzn, df_temp])
sns.barplot(x = df_grouped_amzn['rating'], y=df_grouped_amzn['perc'], hue=df_grouped_amzn['company'], palette='viridis')
plt.title('Which Companies Are Best For The World?')
plt.ylabel('Percent')
positions = (0, 1, 2, 3,4)
labels = ("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree")
plt.xticks(positions, labels)
plt.legend(loc=(1.04,0))
st.pyplot()

st.markdown('Apple and Amazon come out as the clear winners here for doing good for the world, which is rather surprising to me given the sheer amount of negativity surrounding Amazon.')

st.markdown('Twitter and Uber are in similar situations in that they both get the most responses for agreeing that they do good for the world, but significantly fewer people indicate they strongly agree to that statement. The average respondent is slightly more positive about Uber than Twitter, but not by much.')

st.markdown('The very clear loser here is Facebook, being the only one of the companies to have the majority of the respondents giving a strongly disagree or disagree to if Facebook has been good for the world. I would guess if you asked this survey on Facebook (instead of Twitter), Twitter and FB might swap positions.')

st.subheader('Worldview Questions')
st.markdown('The next section of the survey is entirely focused on how the respondents view the world around them, soliciting their opinions on Elon Musk (unsurprisingly positive and polarizing), Capitalism, and the First Amendment')
st.markdown('Here are a few of the response distributions that I found most interesting.')
sns.countplot(df['What are your thoughts on Elon Musk?'], order=['Incredible hero','Admirable figure', 'Neutral', 'Dislike him', 'Strongly dislike him'], palette='viridis')
plt.title('What are your thoughts on Elon Musk?')
plt.xticks(rotation=25)
plt.xlabel('')
st.pyplot()

st.markdown('Unsurprisingly, tech workers like Elon Musk. I was surprised to see that fewer people selected Incredible hero, but the average answer was still positive. Now what do people think of capitalism?')

sns.countplot(df['Free market capitalism is the best economic system yet discovered.'], order=['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree'], palette='viridis')
plt.title('Free market capitalism is the best economic system yet discovered')
plt.xlabel('')
st.pyplot()

st.markdown('These responses were very interesting to me given the zeitgeist surrounding capitalism vs socialism. An overwhelming support for capitalism, at least as the best system yet discovered. These next two questions were fascinating to me, social media banning hate speech and 1A.')

sns.countplot(df['How do you feel about the First Amendment of the US Constitution? (The right to free speech.)'], order = ["It's far too permissive and should definitely be revisited.", "It's excessively permissive and should probably be revisited", "Neutral / think it has meaningful pros and cons", "Supportive in most cases", "Very supportive in almost all cases"], palette='viridis')
plt.xticks(rotation=25)
plt.title('How do you feel about the First Amendement?')
positions = (0, 1, 2, 3,4)
labels = ("Far Too Permissive", "Excessively Permissive", "Neutral", "Supportive", "Very Supportive")
plt.xticks(positions, labels)
plt.xlabel('')
st.pyplot()

sns.countplot(df['Social media platforms should ban all hate speech.'], order=['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree'], palette='viridis')
plt.xticks(rotation=25)
plt.title('Social media platforms should ban all hate speech')
plt.xlabel('')
st.pyplot()

st.markdown('These, of course, do not necessarily contradict each other but are close to it. Either way, it was surprising to get such extremely different distributions to these very related questions.')

st.subheader('Inter-Question Correlations')
st.markdown('One of the first questions that I had when viewing this data is whether or not there were significant correlations between these very related questions. This is not very straightforward, as we have to turn each question answer option into a numbered response where the higher numbers signify higher agreement. For questions which had questions that could be mapped to a scale, we see that they are incredibly correlated.')
st.markdown("The graph below is a heatmap of each question and it's correlation with the rest of the questions. The questions are far too long to include on this heatmap, but the very clear point here is that these questions followed a pattern. If you thought GDPR was good for the world, you also probably liked Elon Musk and thought capitalism was great.")

mapping_dict = {'Strongly dislike him': -2, 'Dislike him': -1, 'Admirable figure': 1, 'Incredible hero': 2,
                'Much better if they pay $X in taxes.': -2, 'Net better if they pay $X in taxes.':-1, 
                'Net better if they spend $X on philanthropy.':1, 'Much better if they spend $X on philanthropy.':2,
                'Very bad': -2, 'Bad': -1, 'Good':1, 'Very good':2,
                'It is highly immoral to do so.': -2, 'It is immoral to do so.': -1, "On net, it's morally acceptable.":1,
                'There are no moral issues with doing so.':2,
                'Strong no': -2, 'No': -1, 'Neutral':0, 'Yes':1, 'Strong yes': 2,
                'Strongly agree': 2, 'Agree': 1, 'Unsure': 0, 'Disagree': -1, 'Strongly disagree':-2,
               'Definitely not': -2, 'Probably not': -1, 'Probably': 1, 'Definitely': 2, 
               'Very worried': -2, 'Slightly worried': -1, 'Not worried':0, 'Not worried/Positive':0, 'No opinion': np.nan,
               '< 20%': -2, '20% - 50%': -1, '50% - 80%': 0, '80% - 90%': 1, '> 90%':2, 
               'Unnecessarily critical': -1, 'Fair and balanced': 0, 'Not critical enough': 1, "I don't read tech coverage from these outlets": np.nan,
               'We should work to shut down the nuclear power stations we have': -2, 'We should not pursue building more nuclear power stations': -1,
                'Neutral': 0, 'We should investigate nuclear power more seriously': 1, 'We should build lots of new nuclear power stations':2,
               "It's far too permissive and should definitely be revisited.": -2, "It's excessively permissive and should probably be revisited": -1,
               'Neutral / think it has meaningful pros and cons': 0, 'Supportive in most cases': 1, 'Very supportive in almost all cases': 2,
               'We should not investigate it.': -1, 'We should seriously investigate it.': 1, 'We should almost certainly pursue it.': 2,
               'Very negative': -2, 'Negative' : -1, 'Positive': 1, 'Very positive': 2, 'The issues are little or no importance to me.': -2,
                'The issues are of slight importance to me.': -1, 'The issues are important to me.':1, 'The issues are extremely important to me.':2,
               'The world today is much worse' : -2, 'The world today is worse': -1, "They're about the same": 0, 'The world today is better':1, 'The world today is much better':2}
df_copy = df.copy()
for i in df_copy.columns[10:49]:
    df_copy[i] = df_copy[i].astype(str)
    df_copy[i].replace(mapping_dict, inplace=True)
    df_copy[i] = pd.to_numeric(df_copy[i], errors='coerce')
drop_cols_2 = ['I wish the performance management system at my company focused more on...',
             'Which climate change strategy do you think should be pursued more?', 'Of the following goals, I care most about:']
df_copy.drop(columns=drop_cols_2, inplace=True)
corr = df_copy.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(18, 14))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.7, cbar_kws={"shrink": .5}, annot_kws={"fontsize":10}, xticklabels='', yticklabels='')
plt.title('Inter-Question Heatmap')
st.pyplot()

st.markdown('For this next graph, I loosely tried to judge if a question was pro or anti tech/capitalism, and defined each answer on a scale of -2 to 2. After this, I plotted the distribution of the sum across the worldview questions discussed before. As expected, the majority of the respondents came out with a sum greater than 0, with a skewed normal distribution.')
df_copy['question_sum'] = df_copy[df_copy.columns[10:46]].sum(axis=1)
df_copy = df_copy[(df_copy['question_sum'] > -40) & (df_copy['question_sum'] < 80)]
sns.distplot(df_copy['question_sum'])
plt.title('Pro vs Anti Tech Perspective')
plt.ylabel('Density')
plt.xlabel('Sum')
st.pyplot()

st.markdown('One thing that is clear here is that there were not two distinct groups/tribes. I further tested this tribes hypothesis with PCA+clustering, and found not two tribes but a multitude of perspectives on the questions.')

st.subheader('Interactive Analysis:')
st.markdown('Want to see how people responded to each of the questions in the survey? Select the question that you are interested in, and this app will produce a histogram of the responses')
drop_cols_3 = ['Amazon_good', 'Facebook_good', 'Twitter_good', 'Uber_good', 'Google_good']
cols_for_selection = [i for i in list(df.columns) if i not in drop_cols_3]
selected_column = st.selectbox('Choose a Question to Analyze', selected_column)
sns.countplot(df[selected_column], palette='viridis')
st.pyplot()