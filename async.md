# Async

[Async APIs](https://docs.cortex.dev/workloads/async) are designed for asynchronous workloads in which the user submits an asynchronous request and retrieves the result later (either by polling or through a webhook). Async APIs are a good fit for users who want to submit longer workloads (such as video, audio or document processing), and do not need the result immediately or synchronously.

Key features

- asynchronously process requests
- retrieve status and response via HTTP endpoint
- autoscale based on request length
- avoid cold starts
- scale to zero
- perform rolling updates
- automatically recover from failures and spot instance termination

## Configuration

```yaml
- name: <string> # name of the API (required)
  kind: AsyncAPI # must be "AsyncAPI" for async APIs (required)
  pod: # pod configuration (required)
    port: <int> # port to which requests will be sent (default: 8080; exported as $CORTEX_PORT)
    max_concurrency: <int> # maximum number of requests that will be concurrently sent into the container (default: 1, max allowed: 100)
    containers: # configurations for the containers to run (at least one constainer must be provided)
      - name: <string> # name of the container (required)
        image: <string> # docker image to use for the container (required)
        command: <list[string]> # entrypoint (not executed within a shell); env vars can be used with e.g. $(CORTEX_PORT) (default: the docker image's ENTRYPOINT)
        args: <list[string]> # arguments to the entrypoint; env vars can be used with e.g. $(CORTEX_PORT) (default: the docker image's CMD)
        env: <map[string:string]> # dictionary of environment variables to set in the container (optional)
        compute: # compute resource requests (default: see below)
          cpu: <string|int|float> # CPU request for the container; one unit of CPU corresponds to one virtual CPU; fractional requests are allowed, and can be specified as a floating point number or via the "m" suffix (default: 200m)
          gpu: <int> # GPU request for the container; one unit of GPU corresponds to one virtual GPU (default: 0)
          inf: <int> # Inferentia request for the container; one unit of inf corresponds to one virtual Inferentia chip (default: 0)
          mem: <string> # memory request for the container; one unit of memory is one byte and can be expressed as an integer or by using one of these suffixes: K, M, G, T (or their power-of two counterparts: Ki, Mi, Gi, Ti) (default: Null)
          shm: <string> # size of shared memory (/dev/shm) for sharing data between multiple processes, e.g. 64Mi or 1Gi (default: Null)
        readiness_probe: # periodic probe of container readiness; traffic will not be sent into the pod unless all containers' readiness probes are succeeding (optional)
          http_get: # specifies an http endpoint which must respond with status code 200 (only one of http_get, tcp_socket, and exec may be specified)
            port: <int|string> # the port to access on the container (required)
            path: <string> # the path to access on the HTTP server (default: /)
          tcp_socket: # specifies a port which must be ready to receive traffic (only one of http_get, tcp_socket, and exec may be specified)
            port: <int|string> # the port to access on the container (required)
          initial_delay_seconds: <int> # number of seconds after the container has started before the probe is initiated (default: 0)
          timeout_seconds: <int> # number of seconds until the probe times out (default: 1)
          period_seconds: <int> # how often (in seconds) to perform the probe (default: 10)
          success_threshold: <int> # minimum consecutive successes for the probe to be considered successful after having failed (default: 1)
          failure_threshold: <int> # minimum consecutive failures for the probe to be considered failed after having succeeded (default: 3)
        liveness_probe: # periodic probe of container liveness; container will be restarted if the probe fails (optional)
          http_get: # specifies an http endpoint which must respond with status code 200 (only one of http_get, tcp_socket, and exec may be specified)
            port: <int|string> # the port to access on the container (required)
            path: <string> # the path to access on the HTTP server (default: /)
          tcp_socket: # specifies a port which must be ready to receive traffic (only one of http_get, tcp_socket, and exec may be specified)
            port: <int|string> # the port to access on the container (required)
          exec: # specifies a command to run which must exit with code 0 (only one of http_get, tcp_socket, and exec may be specified)
            command: <list[string]> # the command to execute inside the container, which is exec'd (not run inside a shell); the working directory is root ('/') in the container's filesystem (required)
          initial_delay_seconds: <int> # number of seconds after the container has started before the probe is initiated (default: 0)
          timeout_seconds: <int> # number of seconds until the probe times out (default: 1)
          period_seconds: <int> # how often (in seconds) to perform the probe (default: 10)
          success_threshold: <int> # minimum consecutive successes for the probe to be considered successful after having failed (default: 1)
          failure_threshold: <int> # minimum consecutive failures for the probe to be considered failed after having succeeded (default: 3)
        pre_stop: # a pre-stop lifecycle hook for the container; will be executed before container termination (optional)
          http_get: # specifies an http endpoint to send a request to (only one of http_get, tcp_socket, and exec may be specified)
            port: <int|string> # the port to access on the container (required)
            path: <string> # the path to access on the HTTP server (default: /)
          exec: # specifies a command to run (only one of http_get, tcp_socket, and exec may be specified)
            command: <list[string]> # the command to execute inside the container, which is exec'd (not run inside a shell); the working directory is root ('/') in the container's filesystem (required)
  autoscaling: # autoscaling configuration (default: see below)
    min_replicas: <int> # minimum number of replicas (default: 1; min value: 0)
    max_replicas: <int> # maximum number of replicas (default: 100)
    init_replicas: <int> # initial number of replicas (default: <min_replicas>)
    target_in_flight: <float> # desired number of in-flight requests per replica (including requests actively being processed as well as queued), which the autoscaler tries to maintain (default: <max_concurrency>)
    window: <duration> # duration over which to average the API's in-flight requests per replica (default: 60s)
    downscale_stabilization_period: <duration> # the API will not scale below the highest recommendation made during this period (default: 5m)
    upscale_stabilization_period: <duration> # the API will not scale above the lowest recommendation made during this period (default: 1m)
    max_downscale_factor: <float> # maximum factor by which to scale down the API on a single scaling event (default: 0.75)
    max_upscale_factor: <float> # maximum factor by which to scale up the API on a single scaling event (default: 1.5)
    downscale_tolerance: <float> # any recommendation falling within this factor below the current number of replicas will not trigger a scale down event (default: 0.05)
    upscale_tolerance: <float> # any recommendation falling within this factor above the current number of replicas will not trigger a scale-up event (default: 0.05)
  node_groups: <list[string]> # a list of node groups on which this API can run (default: all node groups are eligible)
  update_strategy: # deployment strategy to use when replacing existing replicas with new ones (default: see below)
    max_surge: <string|int> # maximum number of replicas that can be scheduled above the desired number of replicas during an update; can be an absolute number, e.g. 5, or a percentage of desired replicas, e.g. 10% (default: 25%) (set to 0 to disable rolling updates)
    max_unavailable: <string|int> # maximum number of replicas that can be unavailable during an update; can be an absolute number, e.g. 5, or a percentage of desired replicas, e.g. 10% (default: 25%)
  networking: # networking configuration (default: see below)
    endpoint: <string> # endpoint for the API (default: <api_name>)
```

### Run

Locally

Test the sentiment classifier model

```bash
docker build -t sentiment -f project/sentiment/Dockerfile.sentiment project/sentiment/
docker run --rm -it sentiment
```

Build a docker image and test the application

```bash
docker build -t sentiment .
docker run -p 8000:8000 -e ENABLE_METRICS=true sentiment
```

```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/classify?input_text=i%20like%20you' \
  -H 'accept: application/json' \
  -d ''
```

Run tests using pytest (Replace line number 5 and 7 in `project/Dockerfile` with `requirements-test.txt` instead of `requirements.txt`)

```bash
docker run -p 8000:8000 -it -v $(pwd):/app --entrypoint bash -e ENABLE_METRICS=true sentiment
pytest --cov
```

Push the docker image to Docker Hub

```bash
docker login
docker build -t <docker-username>/sentiment:0.1 .
docker push <docker-username>/sentiment:0.1
```

Configure a Cortex deployment (using the configuration above create `cortex.yaml`).

```yaml
- name: sentiment # name of the API (required)
  kind: AsyncAPI # must be "AsyncAPI" for async APIs (required)
  pod: # pod configuration (required)
    port: 8000 # port to which requests will be sent (default: 8080; exported as $CORTEX_PORT)
    max_concurrency: 1 # maximum number of requests that will be concurrently sent into the container (default: 1)
    containers: # configurations for the containers to run (at least one constainer must be provided)
      - name: sentiment-api # name of the container (required)
        image: dudeperf3ct7/sentiment:0.1 # docker image to use for the container (required)
        env: # dictionary of environment variables to set in the container (optional)
          ENABLE_METRICS: "true"
          METRICS_NAMESPACE: fastapi
          METRICS_SUBSYSTEM: model
        readiness_probe: # periodic probe of container readiness; traffic will not be sent into the pod unless all containers' readiness probes are succeeding (optional)
          http_get: # specifies an http endpoint which must respond with status code 200 (only one of http_get, tcp_socket, and exec may be specified)
            port: 8000 # the port to access on the container (required)
            path: /healthcheck # the path to access on the HTTP server (default: /)
        liveness_probe: # periodic probe of container liveness; container will be restarted if the probe fails (optional)
          http_get: # specifies an http endpoint which must respond with status code 200 (only one of http_get, tcp_socket, and exec may be specified)
            port: 8000 # the port to access on the container (required)
            path: /healthcheck # the path to access on the HTTP server (default: /)
```

Pre-requisities

- AWS cli
- Create an IAM user with AdministratorAccess and programmatic access.

### Cortex Deployment

- Create a cluster on AWS Account using `cluster.yaml` configuration.

  ```bash
  cortex cluster up cluster.yaml --configure-env prod
  ```

- Create a Cortex deployment on above created cluster

  ```bash
  cortex deploy --env prod
  ```

- Wait for API to be ready

  ```bash
  cortex get --watch
  ```

- Get API endpoint

  ```bash
  cortex get <name-of-API>           # in this case sentiment
  cortex describe <name-of-API>      # in this case sentiment
  ```

- Logs of API

  ```bash
  cortex logs <name-of-API>          # in this case sentiment
  ```

  Here there will be a metrics dashboard and endpoint url with prometheus and grafana integrated by default (how cool is that). Definitions of different metrics on dashboard: [metrics](https://docs.cortex.dev/workloads/realtime/metrics#metrics-in-the-dashboard)

- Test the endpoint

  ```bash
  curl -i -X POST \
    '<endpoint>/classify?input_text=i%20like%20you' \
    -H 'accept: application/json' \
    -d ''
  ```

  or

  ```bash
  python async_requests.py
  ```

- Delete the API

  ```bash
  cortex delete <name-of-API>         # in this case sentiment
  ```

- Delete the cluster on AWS

  The contents of Cortex's S3 bucket, the EBS volumes (used by Cortex's Prometheus and Grafana instances), and the log group are deleted by default when running `cortex cluster down`.

  ```bash
  cortex cluster down
  ```
