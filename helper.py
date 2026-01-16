import pandas as pd
import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending = False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Silver'].astype(int)
    medal_tally['Total']  = medal_tally['Total'].astype(int)

    return medal_tally

def year_country(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    years

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    country

    return years , country



def fetch_medal_tally(df,year,country):
  flag = 0
  medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  if year == 'Overall' and country == 'Overall':
    temp_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  if year != 'Overall' and country == 'Overall':
    temp_df = medal_df[medal_df['Year'] == int(year)]
  if year == 'Overall' and country != 'Overall':
    flag = 1
    temp_df = medal_df[medal_df['region'] == country]
  if year != 'Overall' and country != 'Overall':
    temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    
  if flag == 1: 
    x = temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year').reset_index()
  else:
     x = temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending = False).reset_index()
     

  x['Total'] = x['Gold'] +x['Silver'] + x['Bronze']

  return x


def participation_over_time(df):
    participating_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    participating_over_time.rename(columns = {'Year':'Edition','count':'No of Countries'},inplace = True)
    return participating_over_time


def event_over_time(df):
  events_over_time = df.drop_duplicates(['Year','Event'])
  events_over_time = events_over_time.groupby('Year')['Event'].count().reset_index()
  events_over_time.rename(columns = {'Year':'Year','Event':'No of Events'},inplace = True)
  return events_over_time

def athlete_over_time(df):
   athletes_over_time = df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values(by='Year')
   athletes_over_time.rename(columns = {'Year':'Year','count':'No of Athletes'},inplace = True)
   return athletes_over_time


def most_successful(df,sport):
  temp_df = df.dropna(subset = ['Medal'])

  if sport != 'Overall':
    temp_df = temp_df[temp_df['Sport'] == sport]
  x = temp_df['Name'].value_counts().reset_index(name='Medals').rename(columns={'index':'Name'}).head(15).merge(df, on='Name')[['Name','Medals','region']].drop_duplicates('Name')

  return x


def yearwise_medal_tally(df,country):

  temp_df = df.dropna(subset = ['Medal'])
  temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
  new_df = temp_df[temp_df['region'] == country]
  final_df = new_df.groupby('Year')['Medal'].count().reset_index().sort_values(by = 'Year')

  return final_df

def year_wise_sport(df,country):
  temp_df = df.dropna(subset = ['Medal'])
  temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
  new_df = temp_df[temp_df['region']==country]
  pt = new_df.pivot_table(index = 'Sport',columns = 'Year' , values = 'Medal',aggfunc = 'count').fillna(0)
  return pt

def most_successful_athlete(df,country):
  temp_df = df.dropna(subset = ['Medal'])
  temp_df = temp_df[temp_df['region'] == country]
  x = temp_df['Name'].value_counts().reset_index(name='Medals').rename(columns={'index':'Name'}).head(10).merge(df, on='Name')[['Name','Medals','Sport']].drop_duplicates('Name')

  return x