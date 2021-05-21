#Copyright © 2021 LouisMin2

__author__ = 'LouisMin2'
__version__ = "1.0.1"
__maintainer__ = "LouisMin2"
__email__ = "louismineopersonalprojects@gmail.com"
__status__ = "Production"

import json

with open('Keys.json') as json_file:
    keys = json.load(json_file) #keys['Genius_Key']


#Choosing a Song
ChartsList=['hot-100',
    'billboard-global-excl-us',
    'billboard-global-200'
    ]


from random import *
randomnum = randint(0, len(ChartsList)-1)  # Pick a random index number from the ChartDF.
ChosenChart=ChartsList[randomnum]
print(ChosenChart)
    


#going to billboard #https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3
#
import bs4
import requests
url = "https://www.billboard.com/charts/"+ChosenChart
content = requests.get(url)
soup = bs4.BeautifulSoup(content.text,'html.parser')

#print(url)
#print("=========Text Result==========")

chartTable = soup.find_all('span',class_={"chart-element__information__song text--truncate color--primary","chart-element__information__artist text--truncate color--secondary"},recursive=True)

songs = []
for i in range(0,len(chartTable),2):
  song=chartTable[i].get_text()+" by "+chartTable[i+1].get_text()
  songs.append(song)

randNum=randint(0, len(songs)-1)
chosenSong=songs[randNum]
print(randNum)
print(chosenSong)

song_artist = chosenSong.split(" by ")
print(song_artist)

#using Genius.com instead
import lyricsgenius #https://pypi.org/project/lyricsgenius/
genius = lyricsgenius.Genius(keys['Genius_Key'])

#Parameters
genius.verbose = True # Turn off status messages
genius.remove_section_headers = False # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = True # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)","(Traduction Française)"] # Exclude songs with these words in their title


song = genius.search_song(song_artist[0], song_artist[1])
song.lyrics

#Create DF with lyric, song name and artist
import pandas as pd
song_lyrics = song.lyrics.split("\n")
Lyrics_df = pd.DataFrame(data = song_lyrics , columns=['Lyrics']) 
Lyrics_df

import re
#loop thru rows to assign the song element to the individual lines
element = ""
Lyrics_df['Element'] = ""
for x in range(len(Lyrics_df)):
#Copyright © 2019 LouisMin2
    
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
Lyrics_df['Song_Title'] = song_artist[0]
Lyrics_df['Artist'] = song_artist[1]

#add Line Number
Lyrics_df['Line_No'] = Lyrics_df.index + 1
print(Lyrics_df)





#choose a random element from the song
#Copyright © 2019 LouisMin2
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
#Copyright © 2019 LouisMin2





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


#Copyright © 2019 LouisMin2
import tweepy as tp
consumer_key = keys['Twitter_Consumer_Key']
consumer_secret = keys['Twitter_Consumer_Secret']
access_token = keys['Twitter_Access_Token']
access_secret = keys['Twitter_Access_Secret']
auth = tp.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tp.API(auth)
api.update_status(Tweet)

