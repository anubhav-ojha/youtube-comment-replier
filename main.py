import pandas as pd
import fetch_comment
from id_exists import exists
import Prediction
import reply_on_comment
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]
mycol = mydb["comments1"]

print("Video ID of this URL (https://www.youtube.com/watch?v=3rmeiTJX3mw) is '3rmeiTJX3mw'")
print("Enter Video ID: ",end = " ")

while(True):
    ID = input()
    # Check if it is valid ID
    if(exists(ID)):
        break
    print("Invalid ID. Try Again")
    print("Enter Video ID: ",end = " ")
# try:
#     # Check if this video already exists or not
#     comments_id_ = pd.read_csv(f"./videos_id/{ID}.csv")
# except:
#     # Create new folder for this video ID
#     pd.DataFrame(columns=["id"]).to_csv(f"./videos_id/{ID}.csv")
#     comments_id_ = pd.read_csv(f"./videos_id/{ID}.csv")

# change comments_id dataframe to list here
_comments_id_done = mycol.find({"video_id": ID})
comments_id_done = []
for __ in _comments_id_done:
    comments_id_done.append(__["comments_id"])
# comments_id_done = list(comments_id_["id"])  # Check here is 0 is correct or not

# Fetch comments with comments_id here
comments, comments_id = fetch_comment.fetch(ID,comments_id_done)

# Check Repitition here
flags = fetch_comment.check_repitition(comments_id, comments_id_done)


# Save here to let sentiment access comments.csv file
fetch_comment.save_for_sentiment(comments_id,comments,flags) # Saved in ./comments.csv

# ====================================================================================

# Here comes the part where we go to sentimental analysis file to bring sentiments of a comments.
# Calculate sentiments of those which have flags value == True

replies_to_be_replied = Prediction.predict()

# =====================================================================================


# =====================================================================================

# Here comes the part where we give authority to reply_on_comment.py for next operations.

reply_on_comment.reply(replies_to_be_replied,comments_id,flags)

# =====================================================================================


# Store all flags for no repitition

save_this_comment_id = []
_json = []
for i in range(len(flags)):
    if(flags[i]):
        save_this_comment_id.append(comments_id[i])
        mdict = {"video_id": ID, "comments_id": comments_id[i]}
        _json.append(mdict)

print(_json)
if(_json):
    x = mycol.insert_many(_json)
    print("Successfully Inserted In your Awesome Mongo DataBase")

# new_replied = pd.DataFrame(save_this_comment_id,columns=["id"])
# save_these_comments = pd.concat([comments_id_,new_replied],ignore_index=True)

# print(save_these_comments)
# save_these_comments.to_csv(f"./videos_id/{ID}.csv")

