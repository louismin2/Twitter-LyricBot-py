import json

with open('Keys.json') as json_file:
    keys = json.load(json_file)

import billboard as bb #https://github.com/guoguo12/billboard-charts 


ChartsList=['hot-100',
            'billboard-200',
            'streaming-songs',
            'radio-songs',
            'digital-song-sales',
            'on-demand-songs',
            'pop-digital-songs-sales']
from random import *
randomnum = randint(0, len(ChartsList)-1)  # Pick a random index number from the ChartDF.
print(randomnum)

ChosenChart=ChartsList[randomnum]

chart = bb.ChartData(ChosenChart)
chart.title

#song = chart[0]
#song.title
#song.artist

print(chart)

## listing all the charts 
#bb.charts()

#chart = bb.ChartData("radio-songs")
#chart.title

#print(chart)

#Finding the 2nd Hottest Song on the chart.
#(chart.entries[1])


import pandas as pd
nrows = len(chart.entries)
RadioSongsChart_df = pd.DataFrame(pd.np.empty((nrows, 0)) * pd.np.nan) 
RadioSongsChart_df 





import datetime
RadioSongsChart_df['Song_Title'] = ""
RadioSongsChart_df['Artists'] = ""
RadioSongsChart_df['Last_Updated_At'] = ""
Now_Time = datetime.datetime.now()
for x in range(len(chart.entries)):
    RadioSongsChart_df['Song_Title'][x] = chart.entries[x].title
    RadioSongsChart_df['Artists'][x] = chart.entries[x].artist
    RadioSongsChart_df['Last_Updated_At'][x] = Now_Time

print(RadioSongsChart_df)





from random import *
import re

randomnum = randint(0, len(RadioSongsChart_df)-1)  # Pick a random index number from the ChartDF.
print(randomnum)
Song_Name = RadioSongsChart_df['Song_Title'][randomnum]
Artist = RadioSongsChart_df['Artists'][randomnum]

print(Song_Name)
print(Artist)





#using Genius.com instead
import lyricsgenius #https://pypi.org/project/lyricsgenius/
genius = lyricsgenius.Genius(keys['Genius_Key'])

#Parameters
genius.verbose = True # Turn off status messages
genius.remove_section_headers = False # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)","(Traduction Française)"] # Exclude songs with these words in their title


song = genius.search_song(Song_Name, Artist)
song.lyrics

#Create DF with lyric, song name and artist
import pandas as pd
song_lyrics = song.lyrics.split("\n")
Lyrics_df = pd.DataFrame(data = song_lyrics , columns=['Lyrics']) 
Lyrics_df

#loop thru rows to assign the song element to the individual lines
element = ""
Lyrics_df['Element'] = ""
for x in range(len(Lyrics_df)):
    
    if '[' in Lyrics_df['Lyrics'][x] and ']' in Lyrics_df['Lyrics'][x]:
        element = Lyrics_df['Lyrics'][x] # the text contains element [xxxxx] , then element is assigned to that.  
    Lyrics_df['Element'][x] = element 
    
    #Removing the ad-libs from songs. AKA the content in the brackets like "miss you yea (yea)"
    Lyrics_df['Lyrics'][x] = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", Lyrics_df['Lyrics'][x]) #Remove charters in the brackets
    Lyrics_df['Lyrics'][x] = re.sub("[\(\[].*?[\)\]]", "", Lyrics_df['Lyrics'][x]) # Remove the Brackets after removing the chars
    
#Remove the rows where lyrics is are empty rows
Lyrics_df = Lyrics_df[Lyrics_df.Lyrics != "" ]
#Remove the rows where lyrics is are elements
Lyrics_df = Lyrics_df[~Lyrics_df.Lyrics.str.startswith('[')]
#Re order the indexes
Lyrics_df = Lyrics_df.reset_index(drop = True)

#add Artist and Song Title
Lyrics_df['Song_Title'] = Song_Name
Lyrics_df['Artist'] = Artist

#add Line Number
Lyrics_df['Line_No'] = Lyrics_df.index + 1
print(Lyrics_df)





#choose a random element from the song

from pandasql import *
pysqldf = lambda q: sqldf(query, globals())
query = """
SELECT DISTINCT Element 
FROM Lyrics_df 
ORDER BY RANDOM()
LIMIT 1  
"""
Chosen_Element ="'" + pysqldf(query)['Element'][0]+"'"





print(Chosen_Element)





query = """
SELECT Line_No, Lyrics, Element,Song_Title, Artist 
FROM Lyrics_df
Where Element LIKE """+str(Chosen_Element)+"""
"""
ChosenElement_df = pysqldf(query)
ChosenElement_df





#Randomize the rows index that are divisible by 2 (0,2,4,6,8)
import random

Random_Line_Index = random.randrange(0, len(ChosenElement_df)-1, 1)
#print("Random Number is :",Random_Line_Index)\

#Only choose rows that have more than 6 words and put them into a tweet text format
TweetText_Lyric = ""
if len(ChosenElement_df['Lyrics'][Random_Line_Index].split()) < 6    : #less than 6 words len(line.split()) > 1:
    TweetText_Lyric = ChosenElement_df['Lyrics'][Random_Line_Index]+"\n"+ChosenElement_df['Lyrics'][Random_Line_Index+1]
else: #more than 6 words
    TweetText_Lyric = ChosenElement_df['Lyrics'][Random_Line_Index]
    
#print(TweetText_Lyric)
TweetText_Element = ChosenElement_df['Element'][Random_Line_Index]
TweetText_Song_Title = ChosenElement_df['Song_Title'][Random_Line_Index]
TweetText_Artist = ChosenElement_df['Artist'][Random_Line_Index]


Tweet = TweetText_Lyric + "\n\n\n"+TweetText_Song_Title + " by " + TweetText_Artist

print(Tweet)



import tweepy as tp
consumer_key = keys['Twitter_Consumer_Key']
consumer_secret = keys['Twitter_Consumer_Secret']
access_token = keys['Twitter_Access_Token']
access_secret = keys['Twitter_Access_Secret']
auth = tp.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tp.API(auth)
api.update_status(Tweet)

