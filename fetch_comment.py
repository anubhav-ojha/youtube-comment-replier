import googleapiclient.discovery
import pandas as pd
import json 
from collections import defaultdict
# Debug purpose
def pretty_print(data): 

    data = data
    print(json.dumps(data, indent = 5) ) 

"""
INSERT YOUR OWN API KEY HERE
"""
api_key = ""


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = api_key

def fetch(videoId,already_replied_comments_id,maxResults = 10):
    comments = []   # Stores string of comments
    comments_id = []  # Stores the id's of comments
    # Creating the connection
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # Add parameter maxResults = [1,100] and default value is 20
    # Requesting comments from youtube video with videoID
    request = youtube.commentThreads().list(part="snippet,replies",videoId=videoId,maxResults = maxResults)

    response = request.execute()

    for i in range(maxResults):
        comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
        comments_id.append(response["items"][i]["id"])

    return comments, comments_id # May be use zip here


def save_for_sentiment(comments_id,comments,flags):
    # flags -> boolean array -> [True, False, True, True, False] -> At ith index True denotes this comment is about to be replied.
    
    framed = {"flag": flags,"comments_id": comments_id, "comments": comments}

    df = pd.DataFrame(framed)
    # Save the temporary dataframe to comments.csv
    df.to_csv("./comments.csv",index = False)



def check_repitition(about_to_reply_comments_id,already_replied_comments_id):
    length = len(about_to_reply_comments_id)
    flag = [True] * length # Currently all about to reply are not already replied.
    already_replied_comments_id_dict = defaultdict(bool)
    for i in already_replied_comments_id:
        already_replied_comments_id_dict[i] = True
    for i in range(length):
        if(already_replied_comments_id_dict[about_to_reply_comments_id[i]]):
            flag[i] = False
    return flag


