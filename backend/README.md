`cd backend`

```
pyenv install 3.8.2
pyenv virtualenv 3.8.2 hakaton
pyenv local hakaton 3.8.2
pip install pipenv
pipenv --python 3.8.2
pipenv install --dev
pipenv shell
```

```
export FLASK_APP=hakaton/main.py
export FLASK_ENV=development
flask run
```
