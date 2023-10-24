import http.client
import json

conn = http.client.HTTPConnection("localhost", 8000)

headersList = {
 "Accept": "*/*",
 "User-Agent": "PTU16 browser",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "title": "postinam per python",
  "body": "dar paprasciau, arba ne...",
  "user": 1
})

conn.request("POST", "/posts/", payload, headersList)
response = conn.getresponse()
result = json.loads(response.read().decode("utf-8"))

print(result)
