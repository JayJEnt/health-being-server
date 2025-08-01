# Health-being Web App

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Backend server of health-being-app

## 📌 Table of Contents
- [Prerequisites](#-prerequisites)
- [Endpoints](#-endpoints)
- [Setup](#-setup)
- [Running the Project](#-running-the-project)
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

## 🚀 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/JayJEnt/health-being-server.git
cd health-being-server
```

### 2. Create Environment
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
cp example.env .env
```

Fullfill .env with given settings


## ▶ Running the Project

### Local
```bash
# General case
python main.py
# Turn on just one router
uvicorn api.routers.[router_name]:router --reload
```
Use this for testing api (http://127.0.0.1:8000/docs)

### Development
Soon i will deliver Postman collection


## Deployment
```bash
aws cloudformation deploy --template-file infrastructure/template.yml --stack-name health-being_server --capabilities CAPABILITY_IAM
```


## 🧪 Testing
```bash
pytest tests/
```


## 📜 License
MIT © JayJEnt
