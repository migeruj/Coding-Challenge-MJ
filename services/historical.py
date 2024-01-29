import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
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

        dataframe = pd.read_csv(batch_file.file, header=None, names=col_names,dtype=str, delimiter=',')

        ### Validation Process
        cols = dataframe.columns
        if len(cols)>5:
            raise HTTPException(status_code=412, detail="More columns than expected")

        if table_name == 'employees' and len(cols)!=5:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't correspond to employees schema")
        if table_name == 'jobs' and len(cols) !=2:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't correspond to jobs schema")
        if table_name == 'departments' and len(cols) !=2:
            raise HTTPException(status_code=412, detail="Check your batch file, Doesn't correspond to departments schema")

        up_cols = ["id"] if upsert else None
        res = wr.postgresql.to_sql(df=dataframe,con=pg_conn, table=table_name, schema='public',upsert_conflict_columns=up_cols,
                                   dtype=schemas.get(table_name), use_column_names=True)

        logging.info(res)

    except Exception as e:
        logging.error(e)
    finally:
        pg_conn.close()