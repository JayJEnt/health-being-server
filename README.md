## Initial setup

### Instal miniconda from web

### Set new enviorment
bash'''
conda init
conda create --name [enviorment_name] python=[python_version]
'''

### Activate this enviorment
bash'''
conda activate [enviorment_name]
'''

### Install all dependencies from config.txt
not yet implemented!

## To Run any router
bash'''
uvicorn api.routers.[router_name]:router
'''