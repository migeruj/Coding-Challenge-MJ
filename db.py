### Target DB #####
import pg8000
import os

pg_conn = pg8000.connect(os.environ.get('DB_USER'), os.environ.get('DB_HOST'),
                         os.environ.get('DB_NAME'), os.environ.get('DB_PORT'),
                         os.environ.get('DB_PASSWORD'))