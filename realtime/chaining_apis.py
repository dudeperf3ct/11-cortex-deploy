from pprint import pprint

import requests

# https://docs.cortex.dev/workloads/realtime/containers#chaining-apis

# make a request to an Realtime API
response = requests.post(
    "http://ingressgateway-apis.istio-system.svc.cluster.local/sentiment/classify",
    json={"input_text": "i like you"},
)

pprint(response)
