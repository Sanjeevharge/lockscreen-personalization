#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Lock-Screen Personalization Engine..."

# Create folders
mkdir -p frontend backend ml infra

# Init git
git init
echo "# Lock-Screen Personalization Engine" > README.md

##############################################
# Backend
##############################################
cat > backend/main.py <<EOL
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is alive! 🚀"}
EOL

cat > backend/requirements.txt <<EOL
fastapi
uvicorn
EOL

cat > backend/Dockerfile <<EOL
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

##############################################
# ML
##############################################
cat > ml/train.py <<EOL
# Placeholder ML training script
print("ML training pipeline coming soon 🚀")
EOL

##############################################
# Infra
##############################################
cat > infra/k8s.yaml <<EOL
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lockscreen-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: backend:latest
          ports:
            - containerPort: 8000
EOL

##############################################
# Frontend placeholder (Dockerfile)
##############################################
cat > frontend/Dockerfile <<EOL
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOL

##############################################
# docker-compose
##############################################
cat > docker-compose.yml <<EOL
version: "3.9"
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
EOL

echo "✅ Project skeleton created!"
