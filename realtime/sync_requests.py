import time
from pprint import pprint

import requests

start_time = time.time()

for number in range(1, 10):
    url = "<endpoint>/classify?input_text=ilikeyou"
    resp = requests.post(url)
    results = resp.json()
    pprint(results)

print("--- %s seconds ---" % (time.time() - start_time))
