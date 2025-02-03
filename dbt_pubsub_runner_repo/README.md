# dbt Pub/Sub Runner Helm Chart

This repository contains a Helm chart to deploy a dbt Pub/Sub runner on Google Kubernetes Engine (GKE).

## Prerequisites

1. A GCP project with BigQuery enabled.
2. A service account with `BigQuery Data Viewer` and `BigQuery Job User` roles.
3. A Kubernetes cluster on GKE.
4. `kubectl` and `helm` installed locally.

## Setup Instructions

### 1. Create BigQuery Service Account and Key
- Create a service account with the necessary roles.
- Download the key file as `service-account-key.json`.

### 2. Create Kubernetes Secret
Store the service account key in a Kubernetes secret:

```bash
kubectl create secret generic bigquery-key   --from-file=key.json=service-account-key.json
```

### 3. Deploy the Helm Chart
To deploy the chart, run:

```bash
helm install dbt-runner ./dbt-pubsub-runner   --set projectId=your-gcp-project-id   --set subscriptionName=your-subscription-name   --set image.repository=gcr.io/your-project-id/dbt-pubsub-runner
```

### 4. Verify Deployment
Check that the pod is running:

```bash
kubectl get pods
```

View logs:

```bash
kubectl logs -l app=dbt-pubsub-runner
```

### Customization
Update the `values.yaml` file to customize parameters such as image, replicas, and resource limits.

---

## Helm Parameters

| Parameter              | Description                                    | Default                          |
|------------------------|------------------------------------------------|----------------------------------|
| `replicaCount`         | Number of replicas                             | `1`                              |
| `image.repository`     | Container image repository                     | `gcr.io/your-project-id/dbt-pubsub-runner` |
| `image.tag`            | Container image tag                            | `latest`                         |
| `projectId`            | GCP project ID                                | `your-gcp-project-id`            |
| `subscriptionName`     | Pub/Sub subscription name                      | `dbt-transformations-subscription` |
| `resources.limits`     | Resource limits for the container              | `{ memory: "256Mi", cpu: "500m" }` |
| `resources.requests`   | Resource requests for the container            | `{ memory: "128Mi", cpu: "250m" }` |
| `secrets.bigqueryKeySecret` | Name of the Kubernetes secret for BigQuery | `bigquery-key`                   |

---
