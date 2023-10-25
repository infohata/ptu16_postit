import requests
import json

reqUrl = "http://localhost:8000/posts/"

headersList = {
 "Accept": "*/*",
 "User-Agent": "PTU16 browser",
 "Authorization": "Token 688c7a3f12d8480fef4d1f5d39f3bc46763e7d8e",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "title": "postinam per requests biblioteka",
  "body": "naudojant token autorizacija ir visus kitus cimbaliukus"
})

response = requests.request("POST", reqUrl, data=payload, headers=headersList)

print(response.text)
