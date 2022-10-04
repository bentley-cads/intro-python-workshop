# Python Practice Exercises
# -------------------------
# 
# Thanks to Luke Cherveny for creating these Python exercises.
# 
# Data file
# ---------
# 
# The file senate_2022.csv contains data on the 100 current members
# of the United States Senate. It is a cleaned copy/paste from Wikipedia:
# https://en.wikipedia.org/wiki/List_of_current_United_States_senators
#
# Variables include:
# 
#  * Name: Senator name
#  * State: State the senator represents
#  * Party: Official political affiliation 
#  * BirthDate: Date of Birth (along with age)
#  * Occupation: Declared occupation(s), separated by commas
#  * PreviousOffice: Previously held elected offices, separated by commas
#  * Education: College/University and degree, separated by commas
#  * AssumedOffice: Date senate seat assumed
#  * Election: Year the senator's seat is up for election
#  * Residence: Senator official city of residence (in the state they represent)

# ## Question 1
# 
# Load the .csv as a pandas DataFrame

# Solution to Question 1

import pandas as pd
df = pd.read_csv( 'senate_2022.csv' )
# print( df ) # uncomment this line to see the dataset printed


# ## Question 2
# 
# Make a list of the states that have Senate elections this year.

# Solution to Question 2

answer2 = df[df.Election == 2022].State.unique()
# print( answer2 ) # uncomment this line to see the answer printed


# ## Question 3
# 
# What is the political make up of the US Senate?

# Solution to Question 3

answer3 = df.Party.value_counts()
# print( answer3 ) # uncomment this line to see the answer printed


# ## Question 4
# 
# Which senators have a JD?

# Solution to Question 4 (assuming no school contains the initials "JD" in it...)

answer4 = df[df.Education.str.contains( 'JD' )]
# print( answer4 ) # uncomment this line to see the answer printed


# ## Question 5
# 
# Which senator names have more than two words?

# Solution to Question 5

name_parts = df.Name.str.split()
num_parts = name_parts.apply( len )
answer5 = df[num_parts > 2].Name
# print( answer5 ) # uncomment this line to see the answer printed


# ## Question 6
# 
# Change each senator's hometown to include the state, e.g. "Cambridge" becomes "Cambridge, Massachusetts".

# Solution to Question 6

df.Residence = df.Residence + ', ' + df.State
# print( df[['Name','Residence']] ) # uncomment this line to see the results


# ## Question 7
# 
# Make a new variable for just the age of each senator and sort the senators by age.

# Solution to Question 7

df['Age'] = df.BirthDate.str[-3:-1].astype( int )
df = df.sort_values( by='Age' )
# print( df ) # uncomment this line to see the results


# ## Question 8
# 
# Make a new variable for whether a senator was in the U.S. House.

# Solution to Question 8

df['WasInHouse'] = df.PreviousOffice.str.contains( 'U.S. House' )
# print( df ) # uncomment this line to see the results


# ## Question 9
# 
# Which senator has the most declared occupations?

# Solution to Question 9

df['NumOccupations'] = df.Occupation.str.split( ',' ).apply( len )
answer9 = df.sort_values( by='NumOccupations', ascending=False ).head()
# print( answer9 ) # uncomment this line to see the answer printed


# ## Question 10
# 
# In which states are both seats in the Senate controlled by the same party?

# Solution to Question 10

def has_only_one_party ( state_name ):
    return len( df[df.State == state_name].Party.unique() ) == 1
answer10 = [ state for state in df.State.unique() if has_only_one_party( state ) ]
# print( answer10 ) # uncomment this line to see the answer printed


# ## Question 11
# 
# Make a histogram of senator ages.

# Solution to Question 11
# NOTE: Only the df.Age.plot.hist() line is strictly necessary.
#       The rest just make the plot readable.
import matplotlib.pyplot as plt
df.Age.plot.hist()
plt.title( 'Distribution of Senator Ages' )
plt.xlabel( 'Age' )
# plt.show() # uncomment this line to show the plot in a popup


# ## Question 12
# 
# How does average age for republican senators compare to average age for democratic senators?
# 
# Challenge: Make side-by-side box plots to compare the age distribution by party.

# Solution to Question 12 (challenge solution is further below)

answer12 = df.groupby( 'Party' )['Age'].mean()
# print( answer12 ) # uncomment this line to see the answer printed

# Solution to Question 12's Challenge

# df.boxplot( column='Age', by='Party' ) # uncomment this line to see the plot in a popup


# ## Question 13
# 
# Which senator has been in the senate the longest?
# 
# (Hint: You don't *need* to use datetimes, but the solution is cleaner if you do.)

# Solution to Question 13

import datetime
# Convert "AssumedOffice" column into Python datetime objects for use in computation:
df.AssumedOffice = pd.to_datetime( df.AssumedOffice )
# Subtract each "AssumedOffice" time from now, to find the total time in office so far:
now = datetime.datetime.now()
df['TimeInOffice'] = now - df.AssumedOffice
# Show the table sorted by that value, decreasing:
answer13 = df.sort_values( by='TimeInOffice', ascending=False ).head()
# print( answer13 ) # uncomment this line to see the answer printed


# ## Question 14 - Challenge
# 
# Which senator was the oldest when they assumed office?
# 
# (Hint: You definitely need datetimes for this one.)

# Solution to Question 14

# Convert the BirthDate column into a Python datetime, for use in computations:
# (Note that we have to drop the end of each BirthDate, where it has the age.)
df['BirthDatetime'] = pd.to_datetime( df.BirthDate.str[:-9] )
# Compute the Senator's age when they assumed office:
df['AgeWhenAssumedOffice'] = df.AssumedOffice - df.BirthDatetime
# Show the table sorted by that value, decreasing:
answer14 = df.sort_values( by='AgeWhenAssumedOffice', ascending=False ).head()
# print( answer14 ) # uncomment this line to see the answer printed


# ## Question 15 - Challenge
# 
# Which college/university granted the most degrees to Senate members?
# 
# (Hint: You probably need regular expressions for this one.)

# Solution to Question 15

# NOTE: To help the reader understand this solution, I suggest running each line separately,
#       in a cell on its own, to see the value of its output alone.
# Break each Senator's education up at the commas:
education_parts = df.Education.str.split( ', ' )
# Flatten all those results into one big list for all Senators:
schools_and_more = [ text for parts in education_parts for text in parts ]
# Drop little bits that don't contain any school names:
without_junk = [ text for text in schools_and_more if '(' in text ]
# Erase the degree from the end of each piece of text, leaving only the school name:
just_schools = [ text[:text.index( '(' )] for text in without_junk ]
# Build a frequency table from that list of school names:
answer15 = pd.Series( just_schools ).value_counts()
# print( answer15 ) # uncomment this line to see the answer printed

