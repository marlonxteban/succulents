# succulents
application that shows you succulents, their characteristics and where to get them.
Note: Actually this app is a prototype developed for the capstone project of Full Stack Web Developer nanodegree by Udacity.

## motivation
This project is carried out as the first step towards the implementation of an application that allows to see, manage and finally sell plants (succulents).

# Dependencies

## Database Setup
This project uses a postgres database engine.
In the root folder there is a file named `succulents.psql`.
- Run:
```bash
psql succulents < succulents.psql
```

- Create a database called
``` bash
succulents_test
```
for the unit tests.

## install Python dependencies

Install the packages using pip and the file `requirements.txt`.
``` bash
pip install -r requirements.txt
```
## Local Server
1. Install python dependencies.
2. In folder `config` create a file named `.env` and populate with the next following code:
``` bash
DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/succulents'
SQLALCHEMY_TRACK_MODIFICATIONS = False
OWNER_TOKEN = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlQQ3drelZ1LUItSl9qckdJVXJCciJ9.eyJpc3MiOiJodHRwczovL21hcmxvbnh0ZWJhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxOGJlZWVhMDgzN2EwMDY5ZjkwZDYyIiwiYXVkIjoic3VjY3VsZW50cyIsImlhdCI6MTYxNjkxODI0MiwiZXhwIjoxNjE3MDA0NjQyLCJhenAiOiJZZG84NFpJc1RwSm5LMWg2eWk3dkp5ZlRoVXE3NlNYVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmZhbWlseSIsImRlbGV0ZTpzdWNjdWxlbnQiLCJnZXQ6c3VjY3VsZW50LWRldGFpbCIsInBhdGNoOmZhbWlseSIsInBhdGNoOnN1Y2N1bGVudCIsInBvc3Q6ZmFtaWx5IiwicG9zdDpzdWNjdWxlbnQiXX0.FfwpzS3YWfF8Bukmh8ZC3rIneyATv6TUtUirpe4Z_Z-FJkF_yzEbl4gsHhXJIcU-TowfgiRCizFuFL-yua_CMTlYxTR-NhXNePMwPh7kJqQla82MeXIwF_SpgFLVFphxGsbXQ75imrQSJWmoSlMuoz_0Z52Jp3WTx2dlrB9pKdWTv8IAApDaxfulG2SHHghbadAkacjAXB_6wgEWnNj6k4cKQhqLHFyB7s6HQno-_lPk3JhypLBsmuUb0e03RLhOhJ7Ux81VHwMNOjU0cZwofaWjzHUK7PSVQsepOThttsX4BPtslaNbVS1ak4aggL0fEy8UewEGgR7O8MZfO51azA
COLLABORATOR_TOKEN = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlQQ3drelZ1LUItSl9qckdJVXJCciJ9.eyJpc3MiOiJodHRwczovL21hcmxvbnh0ZWJhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxOGMwYThhMDgzN2EwMDY5ZjkwZDgxIiwiYXVkIjoic3VjY3VsZW50cyIsImlhdCI6MTYxNjkxODM0NiwiZXhwIjoxNjE3MDA0NzQ2LCJhenAiOiJZZG84NFpJc1RwSm5LMWg2eWk3dkp5ZlRoVXE3NlNYVyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnN1Y2N1bGVudC1kZXRhaWwiLCJwYXRjaDpzdWNjdWxlbnQiLCJwb3N0OnN1Y2N1bGVudCJdfQ.FxTRvep85DZfmdo3rSURqcih22CP8ZNIjJPBBi5O10oaVy_xGL1Fn2u4ixEuH21yN_t3_OhPLDoNJxQ56LaP3Zs1XZC_Bcce2_dl7NSQlHiDebqQJqEHKnDXl88hwywSOGE-IvCby2cwAdHCcNEHfSvxON5UiOL2rP8h773TfscJ6tz1VV8swDQQzB9RfzoWvZfKXKeKw_OOoegEnpC9iuaZVUFOghEvrg9cuNuVBfgv_2jPspM2qhynboLNt0-q6qhSUSvdTQB2RMVrRK9CyWNV6R1dUafkpXIjWiXgByZUGtelOQNA3jJZ1MBI63URJqe3-_6KUmxTreTxB6lQOQ
```
These values are used for local environment so you can change according to your system. token values are actual functional tokens used for run tests.

3. Run tests
``` bash
python tests.py
```
All tests should run ok. This test file have several tests for each endpoint an RBAC tests. there are no tests in a postman collection because the access control is tested using unit tests.

4. Run development server
``` bash
python app.py
```
Now the API is up.

5. The front end for this API is in the repo [succulentsclient](https://github.com/marlonxteban/succulentsclient), the instructions of how to set up the front end are in te readme of the repo.

6. This API is live in [mysucculents](https://mysucculents.herokuapp.com/), the front end to use the API is live in [succulentsclient](https://succulentsclient.herokuapp.com/).

## Host in heroku
In this step it is assumed that you have at least one free subscription to heroku 
Run the following commands from a bash terminal (It could be git bash terminar for windows users)

1. Login in heroku
``` bash
heroku login -i
```
You should be requested to enter user and password.

2. Create app in heroku
For this API was run the following command
``` bash
heroku create mysucculents
```
When you create the app, the repository url should be prompted to you, you need the repo url for the next step.

3. Add repo to heroku
For this app the next command was run.
``` bash
git remote add succulentsheroku https://git.heroku.com/mysucculents.git
```

4. Add postgress addon to the app
``` bash
heroku addons:create heroku-postgresql:hobby-dev --app mysucculents
```

5. Push code to heroku repo
``` bash
git push succulentsheroku main
```
This command should deploy the app in heroku.

6. Run migrations
``` bash
heroku run python manage.py db upgrade --app mysucculents
```

Now the API is hosted in heroku. When make changes in code just push the code to heroku (step 5) and the deployment will be run automatically.

# Endpoints

## GET '/families'

- Fetches an array of families of succulents
- Auth: not required
- Request Arguments: None
- Returns: An object that has the list of families.
### response example
```json
    {
      "status_code": 200,
      "total": 1,
      "success": "True",
      "families": [
        {
        "differentiator": "test 1", 
        "environment": "dry", 
        "id": 1, 
        "name": "test family 1", 
        "weather": "sunny"
        }
      ]
    }
```
## GET '/families/<int:id>'
- Fetches a family specified by the id.
- Auth: not required
- Request Arguments: `id` integer.
- Returns: An object that contains: `status_code`, `success`, `family`.

### response example
```json
{
  "family": {
    "differentiator": "test 1", 
    "environment": "dry", 
    "id": 1, 
    "name": "test family 1", 
    "weather": "sunny"
  }, 
  "status_code": 200, 
  "success": true
}
```

## DELETE '/families/<int:id>'
- Delete a family using id
- Auth: owner
- Request Arguments: `id` integer.
- Returns: An object that contains: `deleted`, `success`, `remaining_families`, `remaining_succulents` (after delete).
### response example
```json
{
  "deleted": 2, 
  "remaining_families": 1, 
  "remaining_succulents": 1, 
  "success": true
}
```

## POST '/families'
- Create new family
- Auth: owner
- Request Arguments: `name`: string, `environment`: string, `weather`: string, `differentiator`: string.
- Returns: An object that contains: `status_code`, `success`, `total_families`, `created` (id of new family).
### request body example
```json
{
  "name": "test family 2",
  "environment": "hot",
  "weather": "rainy",
  "differentiator": "test 2"
}
```
### response example
```json
{
  "created": 2, 
  "status_code": 200, 
  "success": true, 
  "total_families": 2
}
```

## PATCH '/families/<int:id>'
- Update a family by id
- Auth: owner
- Request Arguments: `id`: integer,`name`: string, `environment`: string, `weather`: string, `differentiator`: string.
- Returns: An object that contains: `status_code`, `success`, `updated`.
### request body example
```json
{
  "differentiator": "test 1",
  "environment": "dry",
  "id": 1,
  "name": "test family 1 updated",
  "weather": "sunny"
}
```
### response example
```json
{
  "status_code": 200, 
  "success": true, 
  "updated": {
    "differentiator": "test 1", 
    "environment": "dry", 
    "id": 1, 
    "name": "test family 1 updated", 
    "weather": "sunny"
  }
}
```


## GET '/succulents'

- Fetches an array of succulents
- Auth: not required
- Request Arguments: None
- Returns: An object that has the list of succulents.
### response example
```json
    {
  "status_code": 200, 
  "success": true, 
  "succulents": [
    {
      "family_id": 1, 
      "id": 1, 
      "life_time": 5, 
      "name": "test succulent 1"
    }, 
    {
      "family_id": 1, 
      "id": 2, 
      "life_time": 2, 
      "name": "succulent 2"
    }
  ], 
  "total": 2
}
```
## GET '/succulents/<int:id>'
- Fetches a succulent specified by the id.
- Auth: collaborator at least
- Request Arguments: `id` integer.
- Returns: An object that contains: `status_code`, `success`, `succulent`.

### response example
```json
{
  "status_code": 200, 
  "success": true, 
  "succulent": {
    "family_id": 1, 
    "id": 1, 
    "life_time": 5, 
    "name": "test succulent 1"
  }
}
```

## DELETE '/succulents/<int:id>'
- Delete a succulents using id
- Auth: collaborator at least
- Request Arguments: `id` integer.
- Returns: An object that contains: `deleted`, `success`, `remaining_succulents` (after delete).
### response example
```json
{
  "deleted": 2, 
  "remaining_succulents": 1, 
  "success": true
}
```

## POST '/succulents'
- Create new succulent
- Auth: collaborator at least
- Request Arguments: `name`: string, `life_time`: number, `family_id`: integer.
- Returns: An object that contains: `status_code`, `success`, `total_succulents`, `created` (id of new succulent).
### request body example
```json
{
  "name": "succulent 2",
  "life_time": "2",
  "family_id": 1
}
```
### response example
```json
{
  "created": 2, 
  "status_code": 200, 
  "success": true, 
  "total_succulents": 2
}
```

## PATCH '/succulents/<int:id>'
- Update a succulent by id
- Auth: collaborator at least
- Request Arguments: `id`: integer,`family_id`: integer, `life_time`: number, `name`: string.
- Returns: An object that contains: `status_code`, `success`, `updated`.
### request body example
```json
{
  "family_id": 1,
  "id": 1,
  "life_time": "7",
  "name": "test succulent 1 updated"
}
```
### response example
```json
{
  "status_code": 200, 
  "success": true, 
  "updated": {
    "family_id": 1, 
    "id": 1, 
    "life_time": 7, 
    "name": "test succulent 1 updated"
  }
}
```
