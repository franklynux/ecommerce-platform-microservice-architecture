# Kubernetes Configuration Files

This directory contains all the Kubernetes manifests needed to deploy the e-commerce platform.

## Microservices

Each microservice has its own directory containing:
- `deployment.yaml`: Defines the Kubernetes Deployment for the service
- `service.yaml`: Defines the Kubernetes Service for the service

## Emissary-Ingress Configuration

Emissary-Ingress (formerly Ambassador) is configured using three key resources:

1. **emissary-ingress.yaml**: Contains the Host resource that defines domain settings
2. **emissary-listener.yaml**: Contains the Listener resource that defines ports and protocols
3. **ingress.yaml**: Contains the Mapping resources that define routing rules

### Understanding Emissary-Ingress v3.x Architecture

Emissary-Ingress v3.x uses a modular architecture with three main components:

- **Host**: Defines the hostname/domain and TLS settings
- **Listener**: Defines the ports and protocols to listen on
- **Mapping**: Defines the routing rules for incoming requests

The Listener resource is particularly important - without it, Emissary-Ingress won't have any ports to listen on and the load balancer won't have any target groups.

## Deployment Order

For proper deployment:

1. First apply the CRDs: `kubectl apply -f https://app.getambassador.io/yaml/emissary/3.7.0/emissary-crds.yaml`
2. Install Emissary-Ingress: `helm install emissary-ingress datawire/emissary-ingress --namespace emissary`
3. Apply the Host and Listener: `kubectl apply -f emissary-ingress.yaml -f emissary-listener.yaml`
4. Apply the Mappings: `kubectl apply -f ingress.yaml`
5. Deploy the microservices: Apply the manifests in each service directory

Alternatively, use ArgoCD to manage the deployment as described in the main README.