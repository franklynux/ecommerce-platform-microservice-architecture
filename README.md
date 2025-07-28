# E-commerce Platform Microservice Architecture

A production-ready, scalable e-commerce platform built with microservices architecture, featuring automated CI/CD, comprehensive monitoring, and cloud-native deployment on Amazon EKS.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Service Logic Overview](#service-logic-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Amazon EKS Cluster Setup](#amazon-eks-cluster-setup)
  - [Local Development Setup](#local-development-setup)
  - [Docker Compose Development](#docker-compose-development)
- [ArgoCD Installation & Configuration](#argocd-installation--configuration)
- [Microservices Deployment](#microservices-deployment)
  - [ApplicationSet Deployment](#applicationset-deployment)
  - [API Gateway Setup](#api-gateway-setup)
- [Configuration](#configuration)
  - [ROOT_PATH Environment Variable](#root_path-environment-variable)
  - [CORS Configuration](#cors-configuration)
- [Monitoring & Observability](#monitoring--observability)
  - [Prometheus & Grafana Setup](#prometheus--grafana-setup)
  - [Key Metrics](#key-metrics)
- [Logging Infrastructure](#logging-infrastructure)
  - [EFK Stack Setup](#efk-stack-setup)
  - [Kibana Dashboard Configuration](#kibana-dashboard-configuration)
- [CI/CD Pipeline](#cicd-pipeline)
  - [GitHub Actions Setup](#github-actions-setup)
  - [Workflow Configuration](#workflow-configuration)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Architecture Overview

![Architecture Diagram](images/architecture-diagram.png)

This e-commerce platform implements a cloud-native microservices architecture deployed on Amazon EKS, featuring automated CI/CD, comprehensive monitoring, and centralized logging.

### Core Components

- **Product Service**: Manages product catalog, inventory, and pricing
- **Cart Service**: Handles shopping cart operations and session management
- **Order Service**: Processes orders, manages fulfillment, and tracks status
- **API Gateway**: Routes traffic and provides unified API access
- **Monitoring Stack**: Prometheus & Grafana for metrics and alerting
- **Logging Stack**: EFK (Elasticsearch, Fluentd, Kibana) for log aggregation



## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|----------|
| **Backend** | FastAPI (Python) | RESTful API development |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Amazon EKS | Managed Kubernetes service |
| **CI/CD** | GitHub Actions + ArgoCD | Automated testing & GitOps deployment |
| **API Gateway** | Emissary-Ingress | Traffic routing & management |
| **Monitoring** | Prometheus & Grafana | Metrics collection & visualization |
| **Logging** | EFK Stack | Log aggregation & analysis |
| **Infrastructure** | eksctl | EKS cluster provisioning |

## Project Structure

```
ecommerce-platform/
├── product-service/           # Product management microservice
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   ├── test_main.py          # Unit tests
│   └── Dockerfile            # Container definition
├── cart-service/             # Shopping cart microservice
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   ├── test_main.py          # Unit tests
│   └── Dockerfile            # Container definition
├── order-service/            # Order processing microservice
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   ├── test_main.py          # Unit tests
│   └── Dockerfile            # Container definition
├── k8s/                      # Kubernetes manifests
│   ├── product-service.yaml  # Product service K8s resources
│   ├── cart-service.yaml     # Cart service K8s resources
│   ├── order-service.yaml    # Order service K8s resources
│   ├── monitoring/           # Prometheus & Grafana
│   │   ├── prometheus.yaml
│   │   ├── grafana.yaml
│   │   └── servicemonitor.yaml
│   ├── logging/              # EFK Stack for log aggregation
│   │   ├── elasticsearch.yaml
│   │   ├── fluentd-config.yaml
│   │   ├── fluentd-daemonset.yaml
│   │   └── kibana.yaml
│   ├── emissary-ingress.yaml # API Gateway Host configuration
│   ├── emissary-listener.yaml# API Gateway Listener configuration
│   └── ingress.yaml          # API Gateway Mapping rules
├── argocd/                   # ArgoCD configuration
│   ├── applicationset.yaml   # ApplicationSet for microservices
│   └── emissary-ingress-app.yaml # ArgoCD app for API Gateway
├── .github/                  # CI/CD workflows
│   └── workflows/
│       └── ci-cd.yml         # GitHub Actions pipeline
├── images/                   # Documentation screenshots
│   ├── architecture-diagram.png
│   ├── eks-cluster-setup.png
│   ├── local-development.png
│   ├── docker-compose-services.png
│   ├── argocd-ui.png
│   ├── applicationset-deployment.png
│   ├── api-gateway-access.png
│   ├── prometheus-ui.png
│   ├── grafana-dashboard.png
│   ├── kibana-dashboard.png
│   └── ci-cd-pipeline.png
├── docker-compose.yml        # Local development setup
└── run_tests.bat            # Test runner script
```

## Service Logic Overview

### Product Service
Manages the product catalog with CRUD operations:
- **Data Model**: Product ID, name, description, price, inventory count
- **Key Features**: Inventory tracking, price management, product search
- **Endpoints**: Create, read, update, delete products
- **Business Logic**: Validates product data, manages stock levels

### Cart Service
Handles shopping cart operations and user sessions:
- **Data Model**: Cart ID, user ID, items list with quantities
- **Key Features**: Add/remove items, quantity updates, cart persistence
- **Endpoints**: Create cart, manage items, clear cart
- **Business Logic**: Validates product availability, calculates totals

### Order Service
Processes orders and manages fulfillment workflow:
- **Data Model**: Order ID, user ID, items, status, timestamps
- **Key Features**: Order creation, status tracking, fulfillment management
- **Endpoints**: Create order, update status, retrieve order history
- **Business Logic**: Validates cart contents, manages order lifecycle

## Getting Started

### Prerequisites

Ensure you have the following tools installed:

| Tool | Version | Purpose |
|------|---------|----------|
| AWS CLI | 2.0+ | AWS service management |
| eksctl | 0.100+ | EKS cluster provisioning |
| kubectl | 1.20+ | Kubernetes management |
| Docker & Docker Compose | Latest | Container runtime |
| Python | 3.8+ | Running tests |
| Helm | 3.0+ | Package management |
| Git | Latest | Version control |

### Amazon EKS Cluster Setup

1. **Configure AWS CLI**:
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```

2. **Create EKS Cluster**:
   ```bash
   # Create cluster with eksctl (takes 15-20 minutes)
   eksctl create cluster \
     --name ecommerce-cluster \
     --region us-west-1 \
     --nodegroup-name ecommerce-workers \
     --node-type t3.medium \
     --nodes 2 \
     --nodes-min 1 \
     --nodes-max 3 \
     --managed
   ```
   
   ![EKS Cluster Setup](images/eks-cluster-setup.png)

3. **Verify Cluster Access**:
   ```bash
   kubectl get nodes
   kubectl get namespaces
   ```

### Local Development Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/ecommerce-platform-microservice-architecture.git
   cd ecommerce-platform-microservice-architecture
   ```

2. **Install Python Dependencies** (for testing):
   ```bash
   # For each service
   cd product-service
   pip install -r requirements.txt -r requirements-dev.txt
   cd ../cart-service
   pip install -r requirements.txt -r requirements-dev.txt
   cd ../order-service
   pip install -r requirements.txt -r requirements-dev.txt
   cd ..
   ```

### Docker Compose Development

1. **Build and Start Services**:
   ```bash
   # Build all Docker images
   docker-compose build
   
   # Start services in detached mode
   docker-compose up -d
   ```
   
   ![Docker Compose Services](images/docker-compose-services.png)

2. **Verify Services**:
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

3. **Test Services Locally**:
   - Product Service: http://localhost:8001/docs
   - Cart Service: http://localhost:8002/docs
   - Order Service: http://localhost:8003/docs
   
   ![Local Development](images/local-development.png)

4. **Run Tests**:
   ```bash
   # Run all tests
   run_tests.bat
   
   # Or test individual services
   cd product-service && pytest -v
   ```

5. **Push Images to Registry**:
   ```bash
   # Login to Docker Hub
   docker login
   
   # Push images
   docker-compose push
   ```

## ArgoCD Installation & Configuration

1. **Create ArgoCD Namespace**:
   ```bash
   kubectl create namespace argocd
   ```

2. **Install ArgoCD**:
   ```bash
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

3. **Wait for ArgoCD Pods**:
   ```bash
   kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
   ```

4. **Get Initial Admin Password**:
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
   ```

5. **Access ArgoCD UI**:
   ```bash
   # Port forward to access locally
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
   
   Access ArgoCD at: https://localhost:8080
   - Username: `admin`
   - Password: (from step 4)
   
   ![ArgoCD UI](images/argocd-ui.png)

## Microservices Deployment

### ApplicationSet Deployment

**Why ApplicationSets?**
- **Scalability**: Manage multiple applications with a single resource
- **Consistency**: Ensures uniform deployment patterns across services
- **Automation**: Automatically creates applications based on templates
- **Maintenance**: Reduces operational overhead for multi-service deployments

1. **Update Docker Registry**:
   ```bash
   # Replace placeholder with your Docker Hub username
   sed -i 's/${DOCKER_REGISTRY}/your-dockerhub-username/g' k8s/*.yaml
   ```

2. **Deploy ApplicationSet**:
   ```bash
   kubectl apply -f argocd/applicationset.yaml
   ```
   
   This creates three ArgoCD applications:
   - `product-service-app`
   - `cart-service-app` 
   - `order-service-app`
   
   ![ApplicationSet Deployment](images/applicationset-deployment.png)

3. **Verify Deployments**:
   ```bash
   # Check ArgoCD applications
   kubectl get applications -n argocd
   
   # Check service pods
   kubectl get pods -l app=product-service -n ecommerce
   kubectl get pods -l app=cart-service -n ecommerce
   kubectl get pods -l app=order-service -n ecommerce
   ```

### API Gateway Setup

1. **Install Emissary-Ingress**:
   ```bash
   # Add Helm repository
   helm repo add datawire https://app.getambassador.io
   helm repo update
   
   # Create namespace
   kubectl create namespace emissary
   
   # Install CRDs
   kubectl apply -f https://app.getambassador.io/yaml/emissary/3.7.0/emissary-crds.yaml
   kubectl wait --timeout=90s --for=condition=established crd -l app.kubernetes.io/name=emissary-ingress
   
   # Install Emissary-Ingress
   helm install emissary-ingress datawire/emissary-ingress --namespace emissary
   ```

2. **Deploy API Gateway Configuration**:
   ```bash
   kubectl apply -f argocd/emissary-ingress-app.yaml
   ```

3. **Access Services via API Gateway**:
   ```bash
   # Get external IP
   kubectl get svc -n emissary emissary-ingress
   
   # Access services (replace EXTERNAL_IP with load balancer address)
   curl http://EXTERNAL_IP/products/
   curl http://EXTERNAL_IP/carts/
   curl http://EXTERNAL_IP/orders/
   ```
   
   ![API Gateway Access](images/api-gateway-access.png)

## Configuration

### ROOT_PATH Environment Variable

The `ROOT_PATH` environment variable enables services to handle URL prefixes correctly when deployed behind an API Gateway.

**Configuration Details**:
- **Purpose**: Allows FastAPI to generate correct OpenAPI schemas and documentation URLs
- **Local Development**: Not set (services run at root path)
- **Kubernetes Deployment**: Set to match API Gateway routing

**Implementation**:
```python
# In each service's main.py
import os
from fastapi import FastAPI

root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(root_path=root_path)
```

**Kubernetes Configuration**:
```yaml
# In deployment manifests
env:
- name: ROOT_PATH
  value: "/products"  # or /carts, /orders
```

**URL Behavior**:
- **Local**: `http://localhost:8001/docs`
- **Kubernetes**: `http://EXTERNAL_IP/products/docs`

## Monitoring & Observability

### Prometheus & Grafana Setup

1. **Create Monitoring Namespace**:
   ```bash
   kubectl create namespace monitoring
   ```

2. **Deploy Prometheus**:
   ```bash
   kubectl apply -f k8s/monitoring/prometheus.yaml
   ```

3. **Deploy Grafana**:
   ```bash
   kubectl apply -f k8s/monitoring/grafana.yaml
   ```

4. **Install ServiceMonitor CRD**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
   ```

5. **Deploy ServiceMonitor** (for scraping metrics):
   ```bash
   kubectl apply -f k8s/monitoring/servicemonitor.yaml
   ```

6. **Access Prometheus UI**:
   ```bash
   # Get external IP
   kubectl get svc -n monitoring prometheus
   # Access at http://EXTERNAL_IP:9090
   ```
   
   ![Prometheus UI](images/prometheus-ui.png)

7. **Access Grafana UI**:
   ```bash
   # Get external IP
   kubectl get svc -n monitoring grafana
   # Access at http://EXTERNAL_IP:3000
   # Default credentials: admin/admin
   ```
   
   ![Grafana Dashboard](images/grafana-dashboard.png)

### Key Metrics

**HTTP Request Metrics**:
- `http_requests_total`: Total HTTP requests count
- `http_request_duration_seconds`: Request duration histogram
- `http_requests_in_progress`: Current active requests

**System Metrics**:
- `process_cpu_seconds_total`: CPU usage
- `process_resident_memory_bytes`: Memory usage
- `process_open_fds`: Open file descriptors

**Custom Business Metrics**:
- `products_created_total`: Products created counter
- `carts_active_total`: Active shopping carts
- `orders_processed_total`: Orders processed counter

**Sample Grafana Queries**:
```promql
# HTTP Request Rate
rate(http_requests_total[5m])

# CPU Usage by Service
rate(process_cpu_seconds_total[5m]) * 100

# Memory Usage
process_resident_memory_bytes / 1024 / 1024
```

**Expected Output:**
- **HTTP Request Rate**: Line chart showing request rate over time
   ![Grafana HTTP Request Rate](images/grafana-http-request-rate.png)

- **CPU Usage**: Gauge showing CPU percentage per service
   ![Grafana CPU Usage](images/grafana-cpu-usage.png)

- **Memory Usage**: Bar chart showing memory usage per service
   ![Grafana Memory Usage](images/grafana-memory-usage.png)

## Logging Infrastructure

### EFK Stack Setup

1. **Create Logging Namespace**:
   ```bash
   kubectl create namespace logging
   ```

2. **Deploy Elasticsearch**:
   ```bash
   kubectl apply -f k8s/logging/elasticsearch.yaml
   ```

3. **Deploy Fluentd DaemonSet**:
   ```bash
   kubectl apply -f k8s/logging/fluentd-config.yaml
   kubectl apply -f k8s/logging/fluentd-daemonset.yaml
   ```

4. **Deploy Kibana**:
   ```bash
   kubectl apply -f k8s/logging/kibana.yaml
   ```

5. **Verify Deployment**:
   ```bash
   kubectl get pods -n logging
   kubectl get svc -n logging
   ```

### Kibana Dashboard Configuration

1. **Access Kibana UI**:
   ```bash
   # Get external IP
   kubectl get svc -n logging kibana
   # Access at http://EXTERNAL_IP:5601
   ```

2. **Create Index Pattern**:
   - Go to **Stack Management** → **Index Patterns**
   - Create pattern: `kubernetes-*`
   - Select `@timestamp` as time field

3. **Create "E-commerce Platform Logs Monitor" Dashboard**:
   
   **Log Volume by Namespace**:
   - Visualization Type: Line Chart
   - Metrics: Count
   - Buckets: Date Histogram on @timestamp
   - Split Series: Terms on kubernetes.namespace_name
   
   **Logs per Service**:
   - Visualization Type: Pie Chart
   - Metrics: Count
   - Buckets: Terms on kubernetes.container_name
   
   **Pod Activity Heat Map**:
   - Visualization Type: Heat Map
   - Metrics: Count
   - X-Axis: Date Histogram on @timestamp
   - Y-Axis: Terms on kubernetes.pod_name
   
   ![Kibana Dashboard](images/kibana-dashboard.png)

4. **Useful Log Queries**:
   ```
   # Filter by service
   kubernetes.container_name: "product-service"
   
   # Filter by log level
   log: "ERROR"
   
   # Filter by namespace
   kubernetes.namespace_name: "default"
   ```

## CI/CD Pipeline

### GitHub Actions Setup

**Why CI/CD is Essential**:
- **Quality Assurance**: Automated testing prevents bugs in production
- **Consistency**: Standardized build and deployment processes
- **Speed**: Faster delivery cycles with automated workflows
- **Reliability**: Reduces human error in deployments
- **Traceability**: Complete audit trail of changes

### Workflow Configuration

1. **Configure Repository Secrets**:
   
   Navigate to: GitHub Repository → Settings → Secrets and Variables → Actions
   
   Add these secrets:
   ```
   DOCKER_USERNAME: your-dockerhub-username
   DOCKER_PASSWORD: your-dockerhub-token
   ```
   ![GitHub Secrets](images/github-secrets.png)

2. **Workflow Features**:
   - **Parallel Testing**: All services tested simultaneously
   - **Docker Layer Caching**: Faster builds using GitHub Actions cache
   - **Multi-tag Strategy**: Images tagged with `latest` and commit SHA
   - **Matrix Strategy**: Efficient parallel processing

3. **Trigger Condition**:
   - Push to `main` branch

4. **Pipeline Stages**:
   ```
   Test → Build → Push → Deploy (via ArgoCD)
   ```
   
   ![CI/CD Pipeline](images/ci-cd-pipeline.png)

5. **Monitor Pipeline**:
   - View workflow runs in GitHub Actions tab
   - Check build logs for any failures
   - Verify images are pushed to Docker Hub

## API Documentation

### Product Service

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `GET` | `/products` | List all products | - |
| `GET` | `/products/{product_id}` | Get specific product | - |
| `POST` | `/products/` | Create new product | `{"name": "string", "price": 0, "description": "string"}` |
| `PUT` | `/products/{product_id}` | Update product | `{"name": "string", "price": 0, "description": "string"}` |
| `DELETE` | `/products/{product_id}` | Delete product | - |

### Cart Service

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `POST` | `/carts/` | Create new cart | `{"user_id": "string"}` |
| `GET` | `/carts/{cart_id}` | Get cart contents | - |
| `POST` | `/carts/{cart_id}/items` | Add item to cart | `{"product_id": "string", "quantity": 1}` |
| `DELETE` | `/carts/{cart_id}/items/{product_id}` | Remove item | - |
| `DELETE` | `/carts/{cart_id}` | Clear cart | - |

### Order Service

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `POST` | `/orders/` | Create new order | `{"cart_id": "string", "user_id": "string"}` |
| `GET` | `/orders/` | List all orders | - |
| `GET` | `/orders/{order_id}` | Get specific order | - |
| `PUT` | `/orders/{order_id}/status` | Update order status | `{"status": "string"}` |

## Testing

Comprehensive testing strategy using pytest and FastAPI's TestClient.

### Test Structure

Each service includes:
- **Unit Tests**: Test individual functions and endpoints
- **Integration Tests**: Test service interactions
- **API Tests**: Test HTTP endpoints and responses

### Running Tests

**All Services**:
```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

**Individual Service**:
```bash
cd product-service
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

**With Coverage**:
```bash
cd product-service
pytest --cov=. --cov-report=term-missing
```

**Test Commands Reference**:

| Command | Description |
|---------|-------------|
| `pytest -v` | Verbose test output |
| `pytest --cov=.` | Run with coverage |
| `pytest -k "test_name"` | Run specific test |
| `pytest --tb=short` | Short traceback format |

### Sample Test Cases

```python
# product-service/test_main.py
def test_create_product():
    response = client.post("/products/", json={
        "name": "Test Product",
        "price": 29.99,
        "description": "Test Description"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Troubleshooting

### Common Issues

**EKS Cluster Access**:
```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name ecommerce-cluster

# Verify access
kubectl get nodes
```

**ArgoCD Password Reset**:
```bash
# Delete the secret to reset password
kubectl -n argocd delete secret argocd-initial-admin-secret

# Restart ArgoCD server
kubectl -n argocd rollout restart deployment argocd-server
```

**Service Not Accessible**:
```bash
# Check pod status
kubectl get pods -l app=product-service

# Check service endpoints
kubectl get endpoints

# Check ingress
kubectl get ingress
```

**Docker Build Issues**:
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

**Log Analysis**:
```bash
# Check pod logs
kubectl logs -f deployment/product-service

# Check ArgoCD logs
kubectl logs -f -n argocd deployment/argocd-server
```

### Performance Optimization

**Scaling Services**:
```bash
# Scale individual service
kubectl scale deployment product-service --replicas=5

# Auto-scaling (HPA)
kubectl autoscale deployment product-service --cpu-percent=70 --min=2 --max=10
```

**Resource Optimization**:
```yaml
# In deployment manifests
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```



## Contributing

### Development Workflow

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/your-username/ecommerce-platform-microservice-architecture.git
   cd ecommerce-platform-microservice-architecture
   ```

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Development Setup**:
   ```bash
   # Install dependencies for all services
   cd product-service && pip install -r requirements.txt -r requirements-dev.txt
   cd ../cart-service && pip install -r requirements.txt -r requirements-dev.txt
   cd ../order-service && pip install -r requirements.txt -r requirements-dev.txt
   ```

4. **Make Changes and Test**:
   ```bash
   # Run tests
   run_tests.bat
   
   # Test locally with Docker Compose
   docker-compose up -d
   ```

5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Ensure all CI/CD checks pass
   - Include description of changes
   - Reference any related issues

### Code Standards

- **Python**: Follow PEP 8 style guidelines
- **Testing**: Maintain >80% test coverage
- **Documentation**: Update README for new features
- **Commits**: Use conventional commit messages

### Pull Request Checklist

- [ ] Tests pass locally and in CI/CD
- [ ] Code follows project style guidelines
- [ ] Documentation updated if needed
- [ ] No breaking changes without discussion
- [ ] Commit messages are clear and descriptive

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Quick Start Summary

1. **Setup EKS Cluster**: `eksctl create cluster --name ecommerce-cluster`
2. **Install ArgoCD**: `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`
3. **Deploy Services**: `kubectl apply -f argocd/applicationset.yaml`
4. **Setup Monitoring**: `kubectl apply -f k8s/monitoring/`
5. **Setup Logging**: `kubectl apply -f k8s/logging/`
6. **Access Services**: Get external IPs and access via API Gateway

For detailed instructions, follow the complete guide above.

**Support**: For questions or issues, please open a GitHub issue or contact the maintainers.

**Documentation**: This README provides comprehensive setup and operational guidance. For API-specific documentation, visit the `/docs` endpoint of each service.