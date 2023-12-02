import requests

# List of videos

def getVideoslist():

    url = "https://video.bunnycdn.com/library/150210/videos"

    headers = {
        "accept": "application/json",
        "AccessKey": "dff41e25-1feb-40ce-b529ea55f1d2-a914-46b2"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    return response.text


# List of libraries 
   
def getLibrarylist():

    url = "https://api.bunny.net/videolibrary?includeAccessKey=false"

    headers = {
        "accept": "application/json",
        "AccessKey": "b66f4744-e8f6-441b-9f5f-c95f6c479470e4cd8d3a-05ab-4a3e-b57b-afe402e03cb2"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    return response.text


# Add Video Library

def addVideolibrary():

    url = "https://api.bunny.net/videolibrary"

    payload = { "Name": "Carnatic Vocal" }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AccessKey": "15178ba0-992b-4561-a7a7-d41a002e0a01324ba389-c99d-4e9d-889f-f79cfc652d11"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return response.text


# Get single video

def getVideo():
    
    url = "https://video.bunnycdn.com/library/163068/videos/7f127be7-0218-4fd7-8f5b-31d2f8db0224"

    headers = {
        "accept": "application/json",
        "AccessKey": "f73e6a63-f4a9-45e7-a03cf65070cc-0112-4830"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    return response.text
