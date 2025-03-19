# Flask Application with Redis on Kubernetes

Project demonstrates deploying a simple Flask web application with Redis caching on Kubernetes, running in both production and development environments simultaneously.

## Project Overview

This is a simple showcases of a web counter application that:
- Tracks the number of visits separately for both environments
- Connects to a shared Redis instance for data persistence
- Shows the pod hostname, environment, and visit count
- Features different visual styling based on the environment (production or development)

## Components

### 1. Flask Application (`app.py`)

The Flask application provides a simple web page that:
- Connects to Redis using environment variables
- Increments a visit counter stored in Redis
- Displays information about the current environment
- Shows distinct visual styling based on the environment (red background for production, green for development)

### 2. Kubernetes Resources

#### Flask Deployments and Services (`flask-deployment.yaml`)
- **Production Deployment (`flask-prod`)**
  - 1 replica # it can be extended for our requirements
  - Limited resources (50m CPU request, 100m CPU limit)
  - Production environment variables
  - Exposed via NodePort 30005

- **Development Deployment (`flask-dev`)**
  - 1 replica
  - More generous resources (250m CPU request, 500m CPU limit)
  - Development environment variables
  - Exposed via NodePort 30006

#### Redis Deployment (`redis-deployment.yaml`)
- Single Redis instance shared by both environments
- Limited resources to minimize cluster usage
- Internal service for pod communication

## Resource Management

Project demonstrates good standards of K8S:

- **Resource Allocation**
  - Production environment has minimal resource allocation
  - Development environment has higher resource allocation for debugging tools
  - Redis has minimal resource allocation

- **Service Organization**
  - NodePort services for external access
  - Internal service for Redis communication
  - Label-based service selection

## Setup and Deployment Instructions

### Prerequisites
- Docker installed - I mean Docker Desktop with Kubernetes enables under "Settings"
- Kubernetes cluster running (Minikube, kind, or other)
- kubectl configured to communicate with your cluster

### Deployment Steps

1. **Build the Docker image**
   docker build -t flask-app:latest .

2. **Deploy Redis**
   kubectl apply -f redis-deployment.yaml

3. **Deploy Flask application (both environments)**
   kubectl apply -f flask-deployment.yaml

4. **Access the applications**
   - Production environment: http://[cluster-ip]:30005
   - Development environment: http://[cluster-ip]:30006

### Verifying Deployment

1. **Check pod status**
   kubectl get pods

2. **Check service status**
   kubectl get services

3. **View logs**
   kubectl logs deployment/flask-prod
   kubectl logs deployment/flask-dev

## Architecture Details

### Networking
- Both environments share the same Redis instance
- Each environment has its own counter key in Redis
- Each service is exposed on a different NodePort

### Data Persistence
- Visit counts persist as long as Redis pod is running
- No permanent storage is configured (data will be lost if Redis pod restarts)

### Environment Separation
- Environments are separated using Kubernetes labels
- Different resource allocations per environment
- Visual distinction in the UI

## Learning Concepts

This project demonstrates several key Kubernetes concepts:
- Deployments and Pod management
- Service networking and exposure
- Resource requests and limits
- Environment variable configuration
- Multi-environment deployments
- Label-based selection

## Project Files

- `app.py` - Flask application code
- `requirements.txt` - Python dependencies
- `flask-deployment.yaml` - Kubernetes configuration for Flask application
- `redis-deployment.yaml` - Kubernetes configuration for Redis service
- `Dockerfile` - Docker image definition for the Flask application

### Dockerfile Details

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

The Dockerfile creates a containerized environment for the Flask application:

- Uses Python 3.9 slim as the base image to minimize size
- Sets up a dedicated working directory for the application
- Installs Python dependencies from requirements.txt
- Copies the application code
- Exposes port 5000 for web traffic
- Configures the container to run the Flask application on startup

This follows Docker best practices by installing dependencies before copying application code, which improves build caching efficiency and produces a smaller final image.
