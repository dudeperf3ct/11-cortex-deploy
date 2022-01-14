import time
from pprint import pprint

import requests

start_time = time.time()

for number in range(1, 10):
    url = "http://aef8794492ec94b0bbec106d83bca5a8-fd4d5795eed99b6d.elb.us-east-1.amazonaws.com/sentiment/classify?input_text=ilikeyou"
    resp = requests.post(url)
    results = resp.json()
    pprint(results)

print("--- %s seconds ---" % (time.time() - start_time))
