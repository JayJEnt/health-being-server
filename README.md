# Health-being Web App

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

One day there will be app description if i add it xD

## 📌 Table of Contents
- [Prerequisites](#-prerequisites)
- [Setup](#-setup)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [Testing](#-testing)

## 🛠 Prerequisites
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions)
- Python 3.13+


## 🚀 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/projectname.git
cd projectname
```

### 2. Create Conda Environment
```bash
conda create --name health-being-server python=3.13
conda activate health-being-server
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```


## ⚙ Configuration
Rename .env.example to .env:

```bash
# No need for now
# Not implemented
cp .env.example .env
```

Edit .env with your settings


## ▶ Running the Project

### Development (with hot reload)
```bash
# General case
python main.py
# Turn on just one router
uvicorn api.routers.[router_name]:router --reload
```
Use this for testing api (http://127.0.0.1:8000/docs)

### Production
```bash
# Not implemented
```


## Docker
```bash
docker build -f Dockerfile --platform linux/amd64 --provenance=false -t 199215058137.dkr.ecr.eu-north-1.amazonaws.com/my-fastapi-lambda:latest .
docker push 199215058137.dkr.ecr.eu-north-1.amazonaws.com/my-fastapi-lambda:latest
```


## Deployment
```bash
aws cloudformation deploy --template-file template.yml --stack-name MyFastAPIStack --capabilities CAPABILITY_IAM
```


## 🧪 Testing
```bash
pytest tests/
```


## 📜 License
MIT © JayJEnt