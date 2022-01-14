# Cortex

[Cortex](https://www.cortex.dev) is built to deploy, manage, and scale machine learning models in production for AWS. It provides features such as

- Serverless workloads
- Automated cluster management
- CI/CD and observability integrations

Cortex supports 4 different ways to build scalable API :

1. [Realtime](https://docs.cortex.dev/workloads/realtime/example): create APIs that respond to requests in real-time.
2. [Async](https://docs.cortex.dev/workloads/async/example): create APIs that respond to requests asynchronously.
3. [Batch](https://docs.cortex.dev/workloads/batch/example): create APIs that run distributed batch jobs.
4. [Task](https://docs.cortex.dev/workloads/task/example): create APIs that run jobs on-demand.

Cortex requires only two configuration file to deploy the application. Cortex creates a cluster from `cluster.yaml` file including a s3 bucket and cloudwatch log group. The Cortex cluster runs on an EKS (Kubernetes) cluster in a dedicated VPC on your AWS account. Each individual API contains `cortex.yaml` to deploy different types of workloads.

In this exercise, transformers sentiment classifier application is deployed using Cortex two different APIs.

1. [Realtime API](realtime/realtime.md)
2. [Async API](async/async.md)

Cortex is super :rocket: With just 2 commands, 2 configuration files and right amount of patience, the application is deployed seamlessly without modifications to the application.

Further Readings:

We just barely scratch the surface by deploying a simple application. Cortex provides different features such `Traffic Splitter`, `Autoscaling`, `Update strategy`, `node groups`, etc. Cortex [cli](https://docs.cortex.dev/clients/cli) and [python client](https://docs.cortex.dev/clients/python) provides easy way to handle cortex updates/upgrades to deployments.

- Cortex Documentation : [Docs](https://docs.cortex.dev/)
