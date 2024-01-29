import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from services import historical
from db import pg_conn
import logging

log = logging.getLogger("uvicorn")

def run_migrations():
    cursor = pg_conn.cursor()
    schema = os.environ.get('DB_SCHEMA')
    query = f'''
    create table IF NOT EXISTS {schema}.employees
    (
        id   integer not null
            constraint employees_pk
                primary key,
        name varchar,
        datetime timestamp,
        department_id integer,
        job_id integer
    );
    
    create table IF NOT EXISTS {schema}.jobs
    (
        id   integer not null
            constraint jobs_pk
                primary key,
        job varchar
    );
    
    
    create table IF NOT EXISTS {schema}.departments
    (
        id   integer not null
            constraint departments_pk
                primary key,
        department varchar
    );
    '''

    res = cursor.execute(query)
    pg_conn.commit()
    cursor.close()
@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up....")
    log.info("Creating tables if not exists....")
    run_migrations()
    yield
    log.info("Shutting down....")

app = FastAPI(lifespan=lifespan)
@app.on_event("shutdown")
def shutdown_event():
    pg_conn.close()
app.include_router(historical.router)