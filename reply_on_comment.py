

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def reply(comments,comments_id,flags):
    api_service_name = "youtube"
    api_version = "v3"
    # Change this later
    client_secrets_file = "C:\\Users\\hp\\Desktop\\client_secret_599729676410-89h63ku4ej32t4pc4565oo9hni1fgfcl.apps.googleusercontent.com.json"
    #client_secret_599729676410-89h63ku4ej32t4pc4565oo9hni1fgfcl.apps.googleusercontent.com
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    converse = {0: "Apology", 4: "Thanks"}
    for i in range(len(flags)):
        
        if(flags[i]):
            printer = converse[comments[i]]
            request = youtube.comments().insert(
                part="snippet",
                body={
                  "snippet": {
                    "parentId": f"{comments_id[i]}",
                    "textOriginal": f"{printer}"
                  }
                }
            )
            response = request.execute()
    print(f"Replied successfully on {flags.count(True)} comments.")

    
