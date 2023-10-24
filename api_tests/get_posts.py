import http.client
import json

connector_class = http.client.HTTPConnection

conn = connector_class("localhost", 8000)

headersList = {
 "Accept": "*/*",
 "User-Agent": "PTU16 python browser" 
}

payload = ""

conn.request("GET", "/posts/", payload, headersList)
response = conn.getresponse()
posts_json = response.read()
posts = json.loads(posts_json)

for post in posts:
    print(post['title'])
    print(post['body'])
    print(f"posted at {post['created_at']} by {post['user']}")

# print(result.decode("utf-8"))
