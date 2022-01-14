import requests

# https://docs.cortex.dev/workloads/async/containers#chaining-apis

# make a request to an Async API
response = requests.post(
    "http://ingressgateway-apis.istio-system.svc.cluster.local/sentiment/",
    json={"input_text": "i like you"},
)

# retreive a result from an Async API
response = requests.get(
    "http://ingressgateway-apis.istio-system.svc.cluster.local/sentiment/<id>"
)
