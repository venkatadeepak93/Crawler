# Crawler
Crawler Django App takes in get requests with two parameters:
1. seed_url
2. depth (default will be 0)

Run the Application and send the Get request.

Sample curl command:
curl -G https://{server:port}/image_links/ --data-urlencode "seed_url=https://paper.vc" -d"depth=4"
