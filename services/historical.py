import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from models.migration import Table, departments_columns, jobs_columns, employees_columns, schemas
from responses.historical import Historical_Services_Responses
import pandas as pd
import awswrangler as wr
from pg8000.core import DatabaseError

### DB connection ###
from db import pg_conn

log = logging.getLogger("uvicorn")


router = APIRouter(prefix="")

@router.post("/", status_code=200, responses=Historical_Services_Responses)
def upload_file(upsert: bool, table_name: Table, include_header: bool = False,batch_file: UploadFile = File(...)):
    """
    I created this based on the following infered context:

    This request is Sync. It probably failed with loads more than 1GB per request
    It will always depend on the amount of available ram memory to run

    This is created taking in mind that it is a controlled context and not more than 100 requests are accepted per min. (Sync pool)

    If this solution were for a SaaS, I would add a work/job/request queue and an async implementation for the DB pool.

    If the historical files are more than 2GB i will consider another solution like Airflow to process the upload
    If the files are more than 5GB I will consider AWS Glue - PySpark
    If the files are more than 5GB and will be more than 2 I will consider AWS Glue - PySpark

    :param upsert: A boolean indicating whether to perform an upsert operation. This helpful if you require to manage conflicts on insert, it will use `id` PK by default
    :param table_name: The name of the table where the insert or upsert operation will be performed.
    """
    try:
        if batch_file.content_type != 'text/csv':
            raise HTTPException(status_code=412, detail="File MIME type is not valid.")

        ### Selecting the correct columns names for the table
        col_names: list[str] = [""]
        if table_name =='employees':
            col_names = employees_columns
        if table_name =='jobs':
            col_names = jobs_columns
        if table_name =='departments':
            col_names = departments_columns

        dataframe: pd.DataFrame = pd.read_csv(batch_file.file, header=None,dtype=str, delimiter=',')

        ### Validation Process
        cols = dataframe.columns
        if len(cols)>5:
            raise HTTPException(status_code=412, detail="More columns than expected")

        if table_name == 'employees' and len(cols)!=5:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't belong to employees schema")
        if table_name == 'jobs' and len(cols) !=2:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't belong to jobs schema")
        if table_name == 'departments' and len(cols) !=2:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't belong to departments schema")

        dataframe.columns = col_names

        up_cols: list[str] | None = ["id"] if upsert else None
        mode: str = 'upsert' if upsert else 'append'

        table_schema: dict = schemas.get(table_name)

        wr.postgresql.to_sql(df=dataframe,con=pg_conn, table=table_name, schema='public',upsert_conflict_columns=up_cols,
                                   dtype=table_schema, use_column_names=True, mode=mode, chunksize=1000)
    except DatabaseError as e:
        if str(e).__contains__("duplicate key value violates unique constraint"):
            raise HTTPException(status_code=500, detail="Duplicate key. Use Upsert mode if you require to overwrite your data")

    return JSONResponse(status_code=200,content={'message': "Accepted"})