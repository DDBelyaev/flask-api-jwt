Flask API template app w/ JWT.
Considered for projects using JavaScript Front-End frameworks, like VueJS, as it has implemented token generation functionality.

To run in development environment:
```
pipenv shell
pip3 install -r requirements.txt
python3 run.py
```

To run in Heroku production environment, consider a project with name PROJECT_NAME on Heroku:
```
git init
git add . && git commit 'Init'
heroku git:remote -a PROJECT_NAME
git push heroku master
heroku run python
```
