# misp-lite
This repository is a kind of [RiiR](https://transitiontech.ca/random/RIIR) exercise to implement MISP core components in a modern tech stack.

## Backend
* **FastAPI**: API
* **SQLAlchemy+Alembic+Pydantic**: ORM/Migrations/Data validation
* **PostgreSQL**: Data persistance
* **Redis**: Cache
* **Celery**: Task Queue / Background Jobs
* **ZeroMQ**: Message queue

### Structure
```
./
├─ backend/
│  └─ app/
│     ├─ models/
│     ├─ repositories/
│     ├─ routers/
│     ├─ schemas/
│     ├─ main.py
│     ├─ database.py
│     ├─ dependencies.py
│     └─ main.py
└─ frontend/
```

* `models/`: Where the SQLAlchemy models are defined, these models are used for creating the SQL tables, each file represents a table.
* `repositories/`: Where the methods that interact directly with the database via SQLAlchmy ORM live, each file clusters the methods related to a given model.
*  `routers/`: Where the FastAPI endpoints are defined, each file represents a resource.
*  `schemas/`: FastAPI models lie, these define the API contracts that are used in OpenAPI spec generation and `Pydantic` validation rules.
*  `database.py`: Database and SQLAchemy bootstraping.
*  `dependencies.py`: Global stuff here, could be refactored.
*  `main.py`: FastAPI entrypoint, routers for all resources are included here.

### Migrations
Migrations are managed by [Alembic](https://alembic.sqlalchemy.org).

#### Show migrations history
```
docker-compose exec backend alembic history
```
#### Upgrade to lastest
```
$ docker-compose exec alembic upgrade head
```
#### Downgrade to revision
```
$ docker-compose exec alembic downgrade [revision]
```

#### Help
```
$ docker-compose exec alembic help 
```

### Testing
```
$ docker-compose --env-file=".env.test" up -d
...
$ docker-compose exec backend pytest
=========================================================================================== test session starts ===========================================================================================
platform linux -- Python 3.9.12, pytest-7.1.2, pluggy-1.0.0
rootdir: /code
collected 1 item                                                                                                                                                                                          

app/test_main.py .                                                                                                                                                                                  [100%]

============================================================================================ 1 passed in 0.33s ============================================================================================
```


### Development and Debugging
This guide is for Visual Studio Code, but should work with other IDEs with minor adjustements.

First make sure Make sure the [Python VS Code extension](https://marketplace) is installed, then:


1. Launch the docker containers with the debug configuration:
    ```
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
    ```
2. Add the following Python debug profile to VS Code: `.vscode/launch.json`
    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Remote Attach",
                "type": "python",
                "request": "attach",
                "port": 5678,
                "host": "localhost",
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}/backend",
                        "remoteRoot": "/code"
                    }
                ]
            }
        ]
    }
    ```

3. Press **F5** on VS Code and start adding breakpoints.

### TODO
- get oauth2 scopes from user role
- background celery jobs
- users ~~cr~~ud
- events ~~c~~r~~ud~~
- attributes ~~cr~~ud
- servers ~~cr~~ud
- roles ~~c~~r~~ud~~
- objects crud
- `/api/v1` prefix for API
- autogenerated docs
- events reports crud
- encrypted server authkey
- event blocklists / org blocklists logic
- protected events logic
- event attribute updates
- event object updates
- breakOnDuplicate logic
- check if we can link somehow PyMISP models and with SQLAlchemy models, example MISPEvent <-> Event

## Frontend
* Vue.js 3
* Bootstrap 5

### Structure
```
./
├─ backend/
└─ frontend/
    └─ ...
```

### Deployment
#### Docker
To start the application run:

```
$ docker-compose up -d
```

### Futher reading
* https://fastapi.tiangolo.com/deployment/docker/#container-images
* https://fastapi.tiangolo.com/tutorial/sql-databases/
* https://fastapi.tiangolo.com/tutorial/bigger-applications/
* https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/
* https://fastapi.tiangolo.com/advanced/security/
* https://fastapi.tiangolo.com/advanced/settings/


