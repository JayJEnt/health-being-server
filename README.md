# Health-being-server

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

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
- Python 3.12


## 🔚 Endpoints

### Test
- GET /test (test message)

### Recipes
- GET/POST /recipes/ (get all recipes from data base or add new one)
- GET/PUT/DELETE /recipes/{recipes_id} (get single recipe with that index_id, modify it or delete it from fridge)

### And many more...

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
python -m pip install -r requirements.txt
```

### 4. Secrets configuration
Rename example.env to .env:

```bash
cd src
cp example.env .env
cd ..
```

open and Fullfill .env with given settings


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
Soon i will deliver Postman collection


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


## 🧪 Testing
```bash
# Not yet implemented!
pytest tests/
```