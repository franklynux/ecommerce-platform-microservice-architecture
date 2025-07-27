# E-commerce Platform Microservice Architecture

This project implements a scalable e-commerce platform using a microservices architecture. The platform consists of several microservices containerized with Docker, deployed to a Kubernetes cluster managed by ArgoCD, and exposed through an API Gateway.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Building and Pushing Docker Images](#building-and-pushing-docker-images)
- [Configuration](#configuration)
  - [ROOT_PATH Environment Variable](#root_path-environment-variable)
  - [CORS Configuration](#cors-configuration)
- [API Documentation](#api-documentation)
  - [Product Service](#product-service)
  - [Cart Service](#cart-service)
  - [Order Service](#order-service)
- [Logging and Monitoring](#logging-and-monitoring)
  - [ELK Stack Setup](#elk-stack-setup)
  - [Scaling](#scaling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Architecture Overview

![Architecture Diagram](images/architecture-diagram.png)

The platform is built using the following microservices:

- **Product Service**: Manages product information, inventory, and catalog
- **Cart Service**: Handles user shopping carts
- **Order Service**: Manages order processing and fulfillment

The services communicate with each other via RESTful APIs and are deployed as independent containers, allowing for scalability and resilience.

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │────│  Kubernetes      │────│   ELK Stack     │
│ (Emissary)      │    │  Cluster         │    │ (Logging)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Microservices  │    │     ArgoCD       │    │    Kibana       │
│ - Product       │    │ (GitOps CD)      │    │ (Visualization) │
│ - Cart          │    │                  │    │                 │
│ - Order         │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|----------|
| **Backend** | FastAPI (Python) | RESTful API development |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Container management |
| **CI/CD** | ArgoCD | GitOps deployment |
| **API Gateway** | Emissary-Ingress | Traffic routing & management |
| **Logging** | ELK Stack | Log aggregation & visualization |
| **Monitoring** | Kibana | Dashboard & analytics |

## Project Structure

```
ecommerce-platform/
├── product-service/       # Product management microservice
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Container definition
├── cart-service/         # Shopping cart microservice
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Container definition
├── order-service/        # Order processing microservice
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Container definition
├── k8s/                  # Kubernetes manifests
│   ├── product-service/  # Product service manifests
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── cart-service/     # Cart service manifests
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── order-service/    # Order service manifests
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── logging/          # ELK Stack for log aggregation
│   │   ├── elasticsearch.yaml
│   │   ├── kibana.yaml
│   │   ├── fluentd-config.yaml
│   │   └── fluentd-daemonset.yaml
│   ├── emissary-ingress.yaml  # API Gateway Host configuration
│   ├── emissary-listener.yaml # API Gateway Listener configuration
│   └── ingress.yaml           # API Gateway Mapping rules
├── argocd/               # ArgoCD configuration
│   ├── applicationset.yaml    # ApplicationSet for microservices
│   └── emissary-ingress-app.yaml  # ArgoCD app for API Gateway
├── images/               # Screenshot placeholders
│   ├── architecture-diagram.png
│   ├── local-services.png
│   ├── k8s-services.png
│   ├── api-gateway-access.png
│   ├── elk-deployment.png
│   ├── kibana-service.png
│   ├── index-pattern-creation.png
│   ├── log-discovery.png
│   ├── dashboard-creation.png
│   └── argocd-applications.png
└── docker-compose.yml    # Local development setup
```

## Getting Started

### Prerequisites

Ensure you have the following tools installed:

| Tool | Version | Purpose |
|------|---------|----------|
| Docker & Docker Compose | Latest | Container runtime |
| Kubernetes cluster | 1.20+ | Container orchestration |
| kubectl CLI | Latest | Kubernetes management |
| ArgoCD | Latest | GitOps deployment |
| Python | 3.8+ | Running tests |
| Helm | 3.0+ | Package management |

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-platform-microservice-architecture.git
   cd ecommerce-platform-microservice-architecture
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the services:
   - Product Service: http://localhost:8001
   - Cart Service: http://localhost:8002
   - Order Service: http://localhost:8003
   
   Access the interactive API documentation:
   - Product Service: http://localhost:8001/docs
   - Cart Service: http://localhost:8002/docs
   - Order Service: http://localhost:8003/docs

   ![Local Development Services](images/local-services.png)

### Kubernetes Deployment

1. Update the Docker registry in Kubernetes manifests:
   ```bash
   # Replace ${DOCKER_REGISTRY} with your registry URL
   sed -i 's/${DOCKER_REGISTRY}/your-registry-url/g' k8s/*.yaml
   ```

2. Install Emissary-Ingress:
   ```bash
   # Add the Emissary-Ingress Helm repository
   helm repo add datawire https://app.getambassador.io
   helm repo update
   
   # Create namespace for Emissary-Ingress
   kubectl create namespace emissary
   
   # Install the Emissary-Ingress CRDs first
   kubectl apply -f https://app.getambassador.io/yaml/emissary/3.7.0/emissary-crds.yaml
   
   # Wait for the CRDs to be established
   kubectl wait --timeout=90s --for=condition=established crd -l app.kubernetes.io/name=emissary-ingress
   
   # Install Emissary-Ingress
   helm install emissary-ingress datawire/emissary-ingress --namespace emissary
   
   # Apply Emissary-Ingress configuration
   kubectl apply -f k8s/emissary-ingress.yaml -f k8s/emissary-listener.yaml -f k8s/ingress.yaml
   ```
   
   > **Note**: The Listener resource is critical for Emissary-Ingress v3.x to function properly. Without it, the API Gateway won't have any ports to listen on.

3. Deploy using ArgoCD:
   ```bash
   # Deploy the Emissary-Ingress resources
   kubectl apply -f argocd/emissary-ingress-app.yaml
   
   # Deploy the microservices using ApplicationSet
   kubectl apply -f argocd/applicationset.yaml
   ```
   
   This will create the following ArgoCD applications:
   - **product-API**: Deploys the Product Service
   - **cart-API**: Deploys the Cart Service
   - **order-API**: Deploys the Order Service
   - **emissary-ingress**: Deploys the API Gateway
   
   ![ArgoCD Applications](images/argocd-applications.png)

4. Access the API Gateway:
   ```bash
   # Get the external IP or LoadBalancer address of the Emissary-Ingress service
   kubectl get svc -n emissary
   ```
   
   ![Kubernetes Services](images/k8s-services.png)
   
   ```bash
   # Access the services using the external IP or LoadBalancer address:
   # Replace EXTERNAL_IP with the actual IP address
   http://EXTERNAL_IP/products
   http://EXTERNAL_IP/carts
   http://EXTERNAL_IP/orders
   ```
   
   You can also access the interactive API documentation:
   ```
   http://EXTERNAL_IP/products/docs
   http://EXTERNAL_IP/carts/docs
   http://EXTERNAL_IP/orders/docs
   ```
   
   ![API Gateway Access](images/api-gateway-access.png)

### Building and Pushing Docker Images

To build and push all Docker images to your registry:

```bash
# Build all images
docker-compose build

# Push all images to Docker Hub
docker-compose push
```

Make sure you're logged into Docker Hub:
```bash
docker login
```

## Configuration

### ROOT_PATH Environment Variable

Each microservice supports a configurable `ROOT_PATH` environment variable that allows the service to be aware of its URL prefix when deployed behind an API Gateway.

**Local Development**: Services run without ROOT_PATH, so APIs and docs are available at the root:
- API endpoints: `http://localhost:8001/products`
- Documentation: `http://localhost:8001/docs`

**Kubernetes Deployment**: Services use ROOT_PATH to handle prefixed URLs:
- API endpoints: `http://EXTERNAL_IP/products/`
- Documentation: `http://EXTERNAL_IP/products/docs`

The ROOT_PATH is automatically configured in the Kubernetes deployment manifests:
- Product Service: `ROOT_PATH=/products`
- Cart Service: `ROOT_PATH=/carts`
- Order Service: `ROOT_PATH=/orders`

### CORS Configuration

The API Gateway includes CORS (Cross-Origin Resource Sharing) configuration to enable:
- Access to FastAPI interactive documentation UI
- Browser-based applications to make API requests
- "Try it out" functionality in Swagger UI

## API Documentation

### Product Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | List all products |
| `GET` | `/products/{product_id}` | Get a specific product |
| `POST` | `/products/` | Create a new product |
| `PUT` | `/products/{product_id}` | Update a product |
| `DELETE` | `/products/{product_id}` | Delete a product |

### Cart Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/carts/` | Create a new cart (requires user_id) |
| `GET` | `/carts/{cart_id}` | Get a specific cart |
| `POST` | `/carts/{cart_id}/items` | Add item to cart |
| `DELETE` | `/carts/{cart_id}/items/{product_id}` | Remove item from cart |
| `DELETE` | `/carts/{cart_id}` | Clear cart |

### Order Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orders/` | Create a new order |
| `GET` | `/orders/` | List all orders |
| `GET` | `/orders/{order_id}` | Get a specific order |
| `PUT` | `/orders/{order_id}/status` | Update order status |

## Logging and Monitoring

### ELK Stack Setup

1. Deploy logging infrastructure:
   ```bash
   kubectl create namespace logging
   kubectl apply -f k8s/logging/
   ```
   
   ![ELK Stack Deployment](images/elk-deployment.png)

2. Access Kibana:
   ```bash
   kubectl get svc -n logging kibana
   # Access via LoadBalancer IP:5601
   ```
   
   ![Kibana Service](images/kibana-service.png)

3. Create index pattern:
   - Go to **Stack Management** → **Index Patterns**
   - Create pattern: `kubernetes-*`
   - Select `@timestamp` as time field
   
   ![Index Pattern Creation](images/index-pattern-creation.png)

4. View logs:
   - Go to **Discover**
   - Filter: `kubernetes.namespace_name : ecommerce`
   - Add fields: `kubernetes.container_name`, `log`
   
   ![Log Discovery](images/log-discovery.png)

5. Create dashboard:
   - Go to **Visualize** → Create visualizations
   - Go to **Dashboard** → Add visualizations
   
   ![Dashboard Creation](images/dashboard-creation.png)

### Scaling

```bash
kubectl scale deployment product-service --replicas=5
```

## CI/CD Pipeline

### GitHub Actions Setup

The project includes automated CI/CD using GitHub Actions that ensures code quality and streamlines deployment.

**Why CI/CD is necessary:**
- **Quality Assurance**: Automatically runs tests on every code change
- **Consistency**: Ensures all services are built and deployed uniformly
- **Speed**: Reduces manual deployment time and human error
- **Reliability**: Catches issues early before they reach production

**Setup Steps:**

1. **Configure Docker Hub Secrets**:
   Go to your GitHub repository → Settings → Secrets and variables → Actions
   
   Add these repository secrets:
   ```
   DOCKER_USERNAME: your-dockerhub-username
   DOCKER_PASSWORD: your-dockerhub-password-or-token
   ```

2. **Workflow Triggers**:
   - Pushes to `main` or `develop` branches
   - Pull requests to `main` branch

3. **Pipeline Stages**:
   - **Test**: Runs pytest for all microservices with proper PYTHONPATH
   - **Build**: Creates Docker images with layer caching for faster builds
   - **Push**: Uploads images to Docker Hub with `latest` and commit SHA tags

The pipeline runs in parallel for all three services (product, cart, order) using GitHub's matrix strategy.

## Testing

Each microservice includes comprehensive unit tests using pytest and FastAPI's TestClient.

### Test Commands

| Command | Description |
|---------|-------------|
| `run_tests.bat` | Run all tests (Windows) |
| `pytest -v` | Run tests for specific service |
| `pytest --cov=. --cov-report=term` | Run tests with coverage |

### Running Tests

**All Services:**
```bash
run_tests.bat
```

**Specific Service:**
```bash
cd product-service
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

**With Coverage:**
```bash
cd product-service
pip install -r requirements.txt -r requirements-dev.txt
pytest --cov=. --cov-report=term
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Ensure all tests pass (`run_tests.bat`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.