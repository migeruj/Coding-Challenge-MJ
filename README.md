### About the environment
Incorporating Python libraries such as `httpx`, `awswrangler`, and `pandas`, this project requires Python 3.10 or later due to version dependencies.
You should have no problems if you use the Dockerfile provided in this project.

### Environment Variables
This project requires the following variables that refers to database credentials

```console
export DB_HOST=localhost;
export DB_NAME=postgres;
export DB_PASSWORD=BO7ZdJ49p;
export DB_PORT=5439;
export DB_USER=postgres
```
In case that you use Pycharm you can import the following line and paste out in enviroment files declaration
```textmate
DB_HOST=localhost;DB_NAME=postgres;DB_PASSWORD=BO7ZdJ49p;DB_PORT=5439;DB_USER=postgres
```

**You should have no problems If you use dockercompose**

### Run it

#### Manually
Run the server with:

```console
$ uvicorn main:app --reload
```
You are able to see if everything is working:

```console
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [19864] using WatchFiles
INFO:     Started server process [34316]
INFO:     Waiting for application startup.
INFO:     Starting up....
INFO:     Creating tables if not exists....
INFO:     Application startup complete.
```

#### Dockercompose

For docker desktop use
```console
docker compose up -d
```
For older versions u require to [install](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually) docker-compose as binary first
```console
docker-compose up -d
```

#### Tests

The project uses pytest library for this part. 
Is already configured. You only required to have the environment variables imported.
To execute the automated tests:

```console
pytest
```
You will be able to see the test results:

```console
Testing started at 11:25 p. m. ...
Launching pytest with arguments C:\Users\micki\PycharmProjects\Coding-Challenge-MJ --no-header --no-summary -q in C:\Users\micki\PycharmProjects\Coding-Challenge-MJ

============================= test session starts =============================
collecting ... collected 9 items

test_main.py::test_empployees_insert PASSED                              [ 11%]
test_main.py::test_jobs_insert PASSED                                    [ 22%]
test_main.py::test_departments_insert PASSED                             [ 33%]
test_main.py::test_empployees_upsert PASSED                              [ 44%]
test_main.py::test_jobs_upsert PASSED                                    [ 55%]
test_main.py::test_departments_upsert PASSED                             [ 66%]
test_main.py::test_wrong_for_employees PASSED                            [ 77%]
test_main.py::test_wrong_for_departments PASSED                          [ 88%]
test_main.py::test_wrong_for_jobs PASSED                                 [100%]

======================== 9 passed, 2 warnings in 2.32s ========================

Process finished with exit code 0
```

#### Documentation

Once you launch this project you can visit the project documentation at
- http://localhost:8000/docs
- http://localhost:8000/redoc