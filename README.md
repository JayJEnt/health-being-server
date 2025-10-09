# Health-being-server

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)

Backend server of health-being-app

## 📌 Table of Contents
- [Prerequisites](#-prerequisites)
- [Endpoints](#-endpoints)
- [Setup](#-setup)
- [Running the Project](#-running-the-project)
- [Deployment](#-deployment)
- [Testing](#-testing)


## 🛠 Prerequisites
- AWS CLI
- Python 3.13


## 🔚 Endpoints

### 1. Postman collection
https://health-being-app.postman.co/workspace/health-being-app-Workspace~26619ec6-b666-4a0c-8eb6-cdabdeb3d851/collection/43536051-8151902d-9004-4a29-8880-724114496a6f?action=share&creator=43536051


## ⚙ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/JayJEnt/health-being-server.git
cd health-being-server
```

### 2. Create and activate an Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements_dev.txt
```

### 4. Secrets configuration
Rename example.env to .env:

```bash
cd src
cp example.env .env
cd ..
```

open and Fullfill .env with given settings

### 5. Setup pre-commit
```bash
# Run this for install
pre-commit install

# Optional run this if something went wrong with install and rerun
pre-commit autoupdate
```


## ▶ Running the Project

### Local
```bash
# General case
python src/main.py

# Turn on just one router
uvicorn src/api.routers.[router_name]:router --reload
```
Use this for testing api (http://127.0.0.1:8000/docs)

### Development
AWS link will be delivered here...


## 🚀 Deployment

### Manual deployment

#### 1. Updated Lambda source code
```bash
# Create a zip file from repo dir and push it on S3 bucket as "lambda.zip"
```

#### 2. Updated Lambda layer code
```bash
# Create a zip file from all dependencies used in repo push file into S3 bucket as "python.zip"
```

#### 3. Create a cloudformation stack
```bash
aws cloudformation deploy --template-file infrastructure/template.yml --stack-name health-being-server --capabilities CAPABILITY_IAM
```

### Auto deployment
After each time u merge code to the main branch, there will be auto deployment run, which is set as github workflow.

*IMPORTANT! Remember to change version.txt so cloudformation stack could pass*


## 🧪 Testing

### Manual testing

#### Run all tests
```bash
pytest tests/
```

#### Check coverage
```bash
pytest --cov=src
```

#### Check lacking coverage
```bash
pytest --cov=src --cov-report=term-missing
```

### Auto testing
After each time u try to commit changes, it will run all tests with pre-commit
