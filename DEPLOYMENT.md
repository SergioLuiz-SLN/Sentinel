# 🚀 SENTINEL — Guia de Deployment

## Índice

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Monitoring & Logging](#monitoring--logging)
7. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development

### Pré-requisitos

- Python 3.9+
- pip ou conda
- Git

### Instalação Passo-a-Passo

```bash
# 1. Clone o repositório
git clone https://github.com/slnit/sentinel.git
cd sentinel

# 2. Crie ambiente virtual
python -m venv .venv

# 3. Ative o ambiente
# Linux/Mac:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat

# 4. Instale dependências
pip install -r Requirements.txt

# 5. Configure (se necessário)
# Edite config/config_motor.json conforme sua necessidade

# 6. Execute o motor (terminal 1)
python src/anomaly_engine.py

# 7. Execute o dashboard (terminal 2)
streamlit run src/dashboard_anomalias.py
```

**Acesso:**
- Dashboard: http://localhost:8501
- API Engine: N/A (processa localmente)

**Variáveis de Ambiente (Opcional):**

```bash
export SENTINEL_CONFIG_PATH="$(pwd)/config/config_motor.json"
export SENTINEL_LOG_LEVEL="INFO"
export SENTINEL_TIMEOUT="30"
```

---

## 🐳 Docker Deployment

### Build Manual

```bash
# Build a imagem
docker build -t sentinel:latest .

# Verifique a imagem
docker images | grep sentinel
```

### Run com Docker Compose (Recomendado)

```bash
# Inicie os containers
docker-compose up -d

# Verifique status
docker-compose ps

# Veja logs
docker-compose logs -f dashboard

# Pare os containers
docker-compose down
```

**Output esperado:**
```
NAME                COMMAND                  STATUS
sentinel-engine     python src/anomaly...    Up (healthy)
sentinel-dashboard  streamlit run src/...    Up (healthy)
```

### Run Manual com Docker

```bash
# Network
docker network create sentinel-net

# Engine
docker run -d \
  --name sentinel-engine \
  --network sentinel-net \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  sentinel:latest \
  python src/anomaly_engine.py

# Dashboard
docker run -d \
  --name sentinel-dashboard \
  --network sentinel-net \
  -p 8501:8501 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  sentinel:latest \
  streamlit run src/dashboard_anomalias.py
```

### Verificar Logs

```bash
# Engine
docker logs sentinel-engine

# Dashboard
docker logs -f sentinel-dashboard

# Ambos
docker logs sentinel-engine && docker logs sentinel-dashboard
```

### Health Check

```bash
# Dashboard health
curl http://localhost:8501/_stcore/health

# Resposta esperada: 200 OK
```

---

## ☸️ Kubernetes Deployment

### Pré-requisitos

- kubectl configurado
- Acesso a um cluster Kubernetes
- Imagem Docker em registy (Docker Hub, ECR, GCR, etc.)

### 1. Push da Imagem

```bash
# Docker Hub
docker build -t seu-usuario/sentinel:1.0 .
docker push seu-usuario/sentinel:1.0

# AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URI
docker tag sentinel:latest YOUR_ECR_URI/sentinel:1.0
docker push YOUR_ECR_URI/sentinel:1.0
```

### 2. Manifests Kubernetes

**`k8s-configmap.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sentinel-config
  namespace: default
data:
  config_motor.json: |
    {
      "paths": {
        "log_processado": "/data/log_sistema.txt"
      },
      "parametros": {
        "ativos": ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA"]
      }
    }
```

**`k8s-engine.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinel-engine
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sentinel-engine
  template:
    metadata:
      labels:
        app: sentinel-engine
    spec:
      containers:
      - name: engine
        image: seu-usuario/sentinel:1.0
        imagePullPolicy: IfNotPresent
        command: ["python", "src/anomaly_engine.py"]
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
      volumes:
      - name: config
        configMap:
          name: sentinel-config
      - name: data
        emptyDir: {}
```

**`k8s-dashboard.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinel-dashboard
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sentinel-dashboard
  template:
    metadata:
      labels:
        app: sentinel-dashboard
    spec:
      containers:
      - name: dashboard
        image: seu-usuario/sentinel:1.0
        imagePullPolicy: IfNotPresent
        command: ["streamlit", "run", "src/dashboard_anomalias.py"]
        ports:
        - containerPort: 8501
          name: web
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
      volumes:
      - name: config
        configMap:
          name: sentinel-config
      - name: data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: sentinel-dashboard
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: sentinel-dashboard
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
    name: web
```

### 3. Deploy

```bash
# Aplicar configurações
kubectl apply -f k8s-configmap.yaml
kubectl apply -f k8s-engine.yaml
kubectl apply -f k8s-dashboard.yaml

# Verifique status
kubectl get deployments
kubectl get pods
kubectl describe pod <pod-name>

# Acesse o dashboard
kubectl port-forward svc/sentinel-dashboard 8501:80
# Acesso: http://localhost:8501

# Limpar
kubectl delete -f k8s-*.yaml
```

---

## ☁️ Cloud Platforms

### AWS ECS (Elastic Container Service)

```bash
# 1. Criar cluster
aws ecs create-cluster --cluster-name sentinel

# 2. Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 3. Criar serviço
aws ecs create-service \
  --cluster sentinel \
  --service-name sentinel-dashboard \
  --task-definition sentinel:1 \
  --desired-count 1
```

### Google Cloud Run

```bash
# 1. Build e push
gcloud builds submit --tag gcr.io/PROJECT_ID/sentinel:latest

# 2. Deploy
gcloud run deploy sentinel-dashboard \
  --image gcr.io/PROJECT_ID/sentinel:latest \
  --platform managed \
  --region us-central1 \
  --port 8501

# 3. Acesso
gcloud run services describe sentinel-dashboard --platform managed
```

### Heroku

```bash
# 1. Login
heroku login

# 2. Create app
heroku create sentinel-slnit

# 3. Add Procfile
echo "web: streamlit run src/dashboard_anomalias.py --server.port=\$PORT" > Procfile

# 4. Deploy
git push heroku main

# 5. View logs
heroku logs -t
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (`.github/workflows/deploy.yml`)

```yaml
name: Deploy Sentinel

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r Requirements.txt
        pip install pytest pytest-cov
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Run tests
      run: pytest

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/sentinel:latest
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/sentinel-dashboard \
          dashboard=${{ secrets.DOCKER_USERNAME }}/sentinel:latest

```

### GitLab CI (`.gitlab-ci.yml`)

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r Requirements.txt pytest pytest-cov
    - pytest
    - flake8 src/

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:latest

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/sentinel-dashboard dashboard=$CI_REGISTRY_IMAGE:latest
  only:
    - main
```

---

## 📊 Monitoring & Logging

### Docker Compose com ELK Stack

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"

  sentinel-engine:
    # ... (config anterior)
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  sentinel-dashboard:
    # ... (config anterior)
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Prometheus Metrics (Futuro)

```python
from prometheus_client import Counter, Histogram, start_http_server

anomalias_detectadas = Counter('sentinel_anomalias_total', 'Total de anomalias')
latencia_processamento = Histogram('sentinel_latencia_segundos', 'Latência de processamento')

@latencia_processamento.time()
def processar_ativo(ticker):
    # ...
    if is_anomalia:
        anomalias_detectadas.inc()
```

---

## 🔧 Troubleshooting

### Problema: Dashboard não conecta ao log

```
Error: FileNotFoundError: [Errno 2] No such file or directory: 'data/log_sistema.txt'
```

**Solução:**
```bash
# Engine não foi executado ainda
# Terminal 1: Execute o engine
python src/anomaly_engine.py

# Aguarde 5-10 segundos
# Terminal 2: Execute o dashboard
streamlit run src/dashboard_anomalias.py
```

### Problema: Porta 8501 já em uso

```bash
# Encontre o processo
lsof -i :8501

# Ou use outra porta
streamlit run src/dashboard_anomalias.py --server.port 8502
```

### Problema: yfinance connection timeout

```
ConnectTimeout: HTTPSConnectionPool(host='query1.finance.api.yahoo.com', port=443)
```

**Solução:**
```bash
# Verifique conexão de internet
ping 8.8.8.8

# Reinicie o engine
python src/anomaly_engine.py
```

### Problema: Docker image muito grande

**Solução - Use multi-stage build:**
```dockerfile
FROM python:3.11-slim as builder
# Build wheels
FROM python:3.11-slim
# Copy wheels do builder
```

---

## ✅ Checklist de Deployment

- [ ] Configurar `config/config_motor.json`
- [ ] Testar localmente (sem Docker)
- [ ] Build da imagem Docker
- [ ] Testar com Docker Compose
- [ ] Push para registry (Docker Hub, ECR, etc.)
- [ ] Configurar CI/CD pipeline
- [ ] Deploy em staging
- [ ] Testes de carga
- [ ] Configurar monitoring/logging
- [ ] Deploy em produção
- [ ] Validar alertas
- [ ] Documentar runbooks

---

**Guia**: DEPLOYMENT.md  
**Versão**: 1.0  
**Última atualização**: 2024-09-01  
**Autor**: SLN IT Solutions
