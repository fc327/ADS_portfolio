
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# In[2]:


# to work with these files, they have been converted to csv files, which is the file format 
# that was practiced with throughout this course 

athfile = 'athletes.xlsx'
athletes = pd.read_excel(athfile)
athletes.to_csv('athletes.csv', sep = ',', index = None, header=True)
coachfile = 'Coaches.xlsx'
coaches = pd.read_excel(coachfile)
coaches.to_csv('coaches.csv', sep = ',', index = None, header=True)
gendfile = 'EntriesGender.xlsx'
gender = pd.read_excel(gendfile)
gender.to_csv('gender.csv', sep = ',', index = None, header=True)
medalfile = 'Medals.xlsx'
medals = pd.read_excel(medalfile)
medals.to_csv('medals.csv', sep = ',', index = None, header=True)
teamsfile = 'Teams.xlsx'
teams = pd.read_excel(teamsfile)
teams.to_csv('teams.csv', sep = ',', index = None, header=True)


# # These dataframes need to be merged into one larger dataframe after some columns are dropped and the rest of the columns are renamed to make merging them easier 

# In[3]:


# To take a look at all the athletes, search the athletes data frame under the 'Name' column 
# Here, the names are listed as LAST NAME, first name (last name is in all caps for some reason)
athletes['Name']


# # To standardize some of the column names, the following will be used: instead of NOC, it will be "Olympic Committee Name"; Discipline will be "Sport"; Name in the teams dataframe will be renamed "Country"

# In[4]:


# Quick look at the different athletes, before renaming columns and doing any other cleaning
athletes.head()


# In[5]:


# Quick look at the number of female and male athletes per discipline aka sport 
gender.head()


# In[6]:


# This is the total number of sports in the gender data frame 
gender['Discipline'].count()


# In[7]:


gender.columns =['Sport', 'Female', 'Male', 'Total per Sport']


# In[8]:


print(round(gender['Female'].mean()))
print(round(gender['Male'].mean()))


# In[9]:


medals.head()
# 1. drop the Rank column (first column in this dataframe)
# 2. use the sorted keyword to alphabetize this dataframe 
# 3. Team/NOC will be renamed 'Country'
# 4. Rank by Total will be renamed 'Olympic Ranking'


# In[10]:


# Code demonstrating the data preparation steps listed above 
medals = medals.drop(['Rank'], axis = 1)
medals.columns =['Olympic Committee Name', 'Gold', 'Silver', 'Bronze', 'Total Medals', 'Rank by Total']


# In[11]:


# Something to note here is that the medals data frame only shows the aggregate total of each medal type and the overall total per country
# as opposed to per athlete, so this will not help to identify which athletes won the type and amount of medals
medals


# In[12]:


print('The most number of medals won by a country is', medals['Total Medals'].max())
print('The least number of medals won by a country is', medals['Total Medals'].min())


# In[13]:


# This code shows the total number of teams that won a total of 1 medal 
sum(medals['Total Medals']== 1)


# In[14]:


# This should list all 17 teams that won 1 medal total, since the code in the above code block
# indicates that there are 17 teams total with that value in the 'Total Medals' column
medals.loc[medals['Total Medals']== 1]


# In[15]:


# This code shows the total number of teams that won 50 or more medals 
sum(medals['Total Medals']>=50)


# In[16]:


# This is the result of the above code showing the specific teams that won 50 or more total medals 
medals.loc[medals['Total Medals']>=50]


# In[17]:


# Another example using 'Ghana' in the Olympic Committee name column 
medals.loc[medals['Olympic Committee Name']== 'Ghana']


# In[18]:


# An example code to show the row from the medals data frame to only show 'Japan'
# This also confirms that there is only one record in the data frame under the 
# 'Olympic Committee Name' with the value 'Japan'
medals.loc[medals['Olympic Committee Name']== 'Japan']


# In[19]:


# The renamed column names in the athletes data frame are as follows: 
athletes.columns=['Name', 'Olympic Committee Name', 'Sport']


# In[20]:


athletes.drop_duplicates()
athletes


# In[21]:


# This code shows all the different sports the athletes compete in 
# These will not be changed, as these are recognized as different events 
# For example, artistic swimming and swimming are two separate events which have different athletes competing in them
athletes['Sport'].unique()


# In[22]:


# This reveals the different values under 'Event', to decipher what the values pertain to 
# The 'Event' should really be 'Gender', as both men and women are some of the values here 

coaches['Event'].unique()


# In[23]:


# The renamed column names in the coaches data frame are as follows
coaches.columns =['Name', 'Olympic Committee Name', 'Sport', 'Gender']


# In[24]:


# showing the renamed columns in the coaches data frame 

coaches


# In[25]:


coaches['Gender'].unique()
coaches = coaches.dropna()


# In[26]:


# The different countries that the coaches represented (not unique values because there are several coaches representing the same country)
coaches['Olympic Committee Name']


# In[27]:


# This code shows all the different sports that the coaches coach the athletes in 
coaches['Sport'].unique()


# In[28]:


# An example to identify coaches from Egypt 
egyptcoaches = coaches.loc[coaches['Olympic Committee Name']== 'Egypt']
egyptcoaches


# In[29]:


# In the above egyptcoaches data frame, there are duplicate values under the 'Name' column 
# There are two examples where the coach and sport are identical (rows 56/57 and rows 92/93)
# The code below removes duplicate values 
egyptcoaches.drop_duplicates()


# In[30]:


# Showing the same analysis with a different country (South Africa, in this example)
sacoaches = coaches.loc[coaches['Olympic Committee Name']== 'South Africa']
sacoaches.drop_duplicates()
sacoaches


# In[31]:


# In this code block, the drop_duplicates() command is attempted for the entire coaches data frame 
# The number of rows decreased from 394 to 381 (which means 13 rows were removed)
coaches = coaches.drop_duplicates()


# In[32]:


# Quick look at the teams data frame 
teams.head()


# In[33]:


# The renamed column names in the teams data frame are as follows 
# Event was renamed to Gender because that is what the Event denotes 
teams.columns = ['Country', 'Sport', 'Olympic Committee Name', 'Gender']


# In[34]:


# This code shows the different values under the 'Gender' column in the teams data frame 
# This is a crucial finding in the analysis, since the Gender is specified for certain sports 
# but there are basically only two genders in this data: men and women
teams['Gender'].unique()


# In[35]:


# Here, it appears that the data differentiates "Women's Team" and "Women"
# as two different values, when they are the same in essence 
teams.loc[teams['Gender']== 'Women\'s Team']


# In[36]:


teams.loc[teams['Gender']== 'Men']


# In[37]:


# In the previous code block, the gender values is 'Men'
# Here, the value is 'Men's Team'

teams.loc[teams['Gender']== 'Men\'s Team']


# In[38]:


teams.loc[teams['Gender']== 'Women']


# In[39]:


# The value 'Women's Team Sprint' is specific to the sport 'Cycling Track'
# However, to reduce confusion and redundancy, the value under this column should be 'Women'
teams.loc[teams['Gender']== 'Women\'s Team Sprint']


# In[40]:


# Another example demonstrating the specificity (although unnecessary) of the gender 
# This pertains to the sport 'Swimming', and the gender here should be 'Women'
teams.loc[teams['Gender']== 'Women\'s 4 x 100m Freestyle Relay']


# In[41]:


# This is a critical problem in the data. 
# There are several individuals or groups of people that are designated as countries 
# when they are in fact not countries, so this is extremely incorrect. 

teams['Country'].unique()


# In[42]:


# The different values under 'Gender', for reference
#(['Men', 'Women', "Men's Team", 'Mixed Team', "Women's Team", 'Duet',
#       'Team', "Women's 4 x 400m Relay", '4 x 400m Relay Mixed',
#       "Men's 4 x 400m Relay", "Men's 4 x 100m Relay",
#       "Women's 4 x 100m Relay", 'Softball', 'Baseball', "Men's Madison",
#       "Men's Team Pursuit", "Men's Team Sprint", "Women's Madison",
#       "Women's Team Pursuit", "Women's Team Sprint", "Men's Foil Team",
#       "Women's Foil Team", "Men's Épée Team", "Women's Épée Team",
#      "Men's 4 x 100m Freestyle Relay", "Men's 4 x 100m Medley Relay",
#       "Men's 4 x 200m Freestyle Relay", 'Mixed 4 x 100m Medley Relay',
#       "Women's 4 x 100m Freestyle Relay",
#       "Women's 4 x 100m Medley Relay",
#       "Women's 4 x 200m Freestyle Relay", 'Mixed Doubles', 'Mixed Relay'],
#       dtype=object)


# In[43]:


# This code is a crucial step in the cleaning and preparation process for this analysis. 
# This is repeated in the following two code blocks
# The pd.DataFrame.replace() function will be used to change all the different values under 'Gender'
# to only Men, Women, and Other, in an effort to make the data from uniform and easier to do analysis on 
# 'Other' needs to be included as a value in this data frame because of values such as 
# 'Mixed', 'Duet', 'Group all around' and 'softball'/'baseball' 
# in which the gender cannot be identified properly 

teams = teams.replace(to_replace=['Women\'s Team', 'Women\'s 4 x 400m Relay', 'Women\'s 4 x 100m Relay',
                        'Women\'s Madison', 'Women\'s Team Pursuit', 'Women\'s Team Sprint',
                        'Women\'s Foil Team', 'Women\'s Épée Team', 'Women\'s Sabre Team',
                        'Women\'s 4 x 100m Freestyle Relay','Women\'s 4 x 100m Medley Relay', 'Women\'s 4 x 200m Freestyle Relay'], value = 'Women')


# In[44]:


# Replacing all values containing 'Men's' in the value with 'Men'
teams = teams.replace(to_replace=['Men\'s Team', 'Men\'s 4 x 400m Relay', 'Men\'s 4 x 100m Relay',
                         'Men\'s Madison', 'Men\'s Foil Team', 'Men\'s Épée Team',
                         'Men\'s Sabre Team', 'Men\'s 4 x 100m Freestyle Relay','Men\'s 4 x 100m Medley Relay',
                         'Men\'s 4 x 200m Freestyle Relay', 'Men\'s Team Pursuit','Men\'s Team Sprint'], value = 'Men')


# In[45]:


# Replacing all values not specifying gender with 'Other '
teams = teams.replace(to_replace=['Mixed Team', 'Duet', 'Team',
                         'Softball', 'Baseball', 'Group All-Around',
                         'Mixed Doubles', 'Mixed Relay','Mixed 4 x 100m Medley Relay',
                                 '4 x 400m Relay Mixed'], value = 'Other')


# In[46]:


# This code checks that the replacement actually worked and to catch any existing values 
# that need to be changed in the data frame 
teams['Gender'].unique()


# In[47]:


teams['Sport'].unique()


# In[48]:


# This uses the 'Gold' column in the medals data frame to 
# create a smaller data frame with just the data from that column
# This code demonstrates the values in the 'Gold' column that are greater than 10, and it uses
# the .loc[] function on the main medals data frame  and passes through the 
# new smaller goldmedaldata data frame. The results are in the goldvalues object 

goldmedaldata = ['Gold']
goldvalues = medals.loc[medals['Gold']>10,goldmedaldata]
goldvalues


# In[49]:


# This is useful, but it is unknown from this data frame 
# which countries these values belong to 
silvermedaldata = ['Silver']
silvervalues = medals.loc[medals['Silver']>10,silvermedaldata]
silvervalues


# In[50]:


athletes.loc[athletes['Name']== 'BILES Simone']


# In[51]:


# Showing all the athletes who compete in 'Artistic Gymnastics'
athletes.loc[athletes['Sport']=='Artistic Gymnastics']


# In[52]:


# There are no common column names with the medals and the newly created atdf1 data frames. 
# So the append function is appropriate here. However, not all the columns from the medals data frame will be needed
# A new data frame with only the olympic committee names, the total medals and rank by total will be created 

totalmedals = medals[['Olympic Committee Name', 'Total Medals', 'Rank by Total']]
totalmedals


# In[53]:


# Average number of medals won during the games 
round(totalmedals['Total Medals'].mean())


# In[54]:


# The total medals and teams data frames will be merged in this code block 
# Naming convention explained: m to signify totalmedals, t to signify teams, df to signify data frame 
mtdf = pd.merge(teams,totalmedals, how = 'inner')


# In[55]:


mtdf['Country'].unique()


# In[56]:


mtdf = mtdf.dropna()


# In[57]:


mtdf.loc[mtdf['Country']== 'United States']


# In[58]:


len(mtdf['Country'].unique())


# In[59]:


mtdf['Sport'].unique()


# In[60]:


# This was one of the values under "Country" 
# mtdf.loc[mtdf['Country']== 'Wang/X.Y.Xia']


# In[61]:


# The Rank by Total should not be an integer, thus the type is changed to string 
# so that these values cannot be calculated over. 
mtdf['Rank by Total'] = mtdf['Rank by Total'].astype(str)


# In[62]:


# Average number of medals won in each sport 
mtdf.groupby(['Sport']).mean().head()


# In[125]:


# Total number of medals won in each sport 
sportgrouped = mtdf.groupby(['Sport']).sum()
sportgrouped.sort_values(by='Total Medals', ascending = False)


# In[65]:


# Total number of medals won per gender (including other, which means that the gender is unknown)
mtdf.groupby(['Gender']).sum()


# In[120]:


# This code reveals all the values under 'Country' that are not actual countries
mtdf.groupby(['Country']).sum()


# In[84]:


gender.groupby(['Sport']).sum()


# In[135]:


# combining the athletes data frame with the merged mtdf 
# as a reminder mtdf merged the total medals and teams data frames 
# The Olympic Committe Name column was duplicated (x and y were created)
# so the 'Olympic Committee Name_y' column was removed from this data frame 

amtdf = pd.merge(athletes, mtdf, how = 'inner')


# In[137]:


# Too many additional rows generated after merging the data frames and dropping duplicate values
amtdf=amtdf.drop_duplicates()
amtdf

