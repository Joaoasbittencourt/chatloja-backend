# Chatloja

Chatloja is a simple chat application that allows users to create digital stores catalog to attract customers.

### Activate virtualenv
```bash
source .venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run Database
```bash
docker compose --profile infra up
```
This requires docker to be installed on your machine. It will start a postgres database on port 5432.

### Run Application on Debug mode
```bash
flask --app main.py --debug run
```

### Install a package
```bash
pip install <package>
pip freeze > requirements.txt
```
