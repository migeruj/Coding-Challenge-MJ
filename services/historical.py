import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from models.migration import Table, departments_columns, jobs_columns, employees_columns, schemas
import pandas as pd
import awswrangler as wr

### DB connection ###
from db import pg_conn

log = logging.getLogger("uvicorn")


router = APIRouter(prefix="")

@router.post("/", status_code=200)
def upload_file(upsert: bool, table_name: Table, include_header: bool = False,batch_file: UploadFile = File(...)):
    """
    This request is Sync. It Doesn't allow more than 1GB per operation
    :return:
    Request response
    """
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

    return JSONResponse(status_code=201,content={'message': "Accepted"})