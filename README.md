# E-commerce Platform Microservice Architecture

This project implements a scalable e-commerce platform using a microservices architecture. The platform consists of several microservices containerized with Docker, deployed to a Kubernetes cluster managed by ArgoCD, and exposed through an API Gateway.

## Architecture Overview

The platform is built using the following microservices:

- **Product Service**: Manages product information, inventory, and catalog
- **Cart Service**: Handles user shopping carts
- **Order Service**: Manages order processing and fulfillment

The services communicate with each other via RESTful APIs and are deployed as independent containers, allowing for scalability and resilience.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Containerization**: Docker
- **Container Orchestration**: Kubernetes
- **Continuous Deployment**: ArgoCD
- **API Gateway**: Emissary-Ingress (Ambassador)

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
│   ├── emissary-ingress.yaml  # API Gateway Host configuration
│   ├── emissary-listener.yaml # API Gateway Listener configuration
│   └── ingress.yaml           # API Gateway Mapping rules
├── argocd/               # ArgoCD configuration
│   ├── applicationset.yaml    # ApplicationSet for microservices
│   └── emissary-ingress-app.yaml  # ArgoCD app for API Gateway
└── docker-compose.yml    # Local development setup
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (local or cloud-based)
- kubectl CLI
- ArgoCD installed on your Kubernetes cluster
- Python 3.8+ with pip for running tests

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

4. Access the API Gateway:
   ```bash
   # Get the external IP or LoadBalancer address of the Emissary-Ingress service
   kubectl get svc -n emissary
   
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

- `GET /products`: List all products
- `GET /products/{product_id}`: Get a specific product
- `POST /products/`: Create a new product
- `PUT /products/{product_id}`: Update a product
- `DELETE /products/{product_id}`: Delete a product

### Cart Service

- `POST /carts/`: Create a new cart (requires user_id in request body)
- `GET /carts/{cart_id}`: Get a specific cart
- `POST /carts/{cart_id}/items`: Add item to cart
- `DELETE /carts/{cart_id}/items/{product_id}`: Remove item from cart
- `DELETE /carts/{cart_id}`: Clear cart

### Order Service

- `POST /orders/`: Create a new order
- `GET /orders/`: List all orders
- `GET /orders/{order_id}`: Get a specific order
- `PUT /orders/{order_id}/status`: Update order status

## Monitoring and Scaling

The microservices architecture allows for independent scaling of each service based on demand. Kubernetes provides built-in scaling capabilities:

```bash
kubectl scale deployment product-service --replicas=5
```

For monitoring, consider implementing:
- Prometheus for metrics collection
- Grafana for visualization
- Jaeger for distributed tracing

## Testing

Each microservice includes unit tests to verify API functionality. The tests use pytest and FastAPI's TestClient.

### Running Tests

#### Running All Tests

On Windows:
```bash
run_tests.bat
```

#### Running Tests for a Specific Service

```bash
cd product-service
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

#### Running Tests with Coverage

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