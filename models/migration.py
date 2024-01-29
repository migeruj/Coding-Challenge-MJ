from enum import Enum

class Table(str, Enum):
    """
    Unique available tables for data migration
    """
    departments = 'departments'
    jobs = 'jobs'
    employees = 'employees'

departments_columns: list[str] = ["id", "department"]
jobs_columns: list[str] = ["id", "job"]
employees_columns: list[str] = ["id", "name", "datetime", "department_id", "job_id"]

schemas: dict = {
    'employees': {
        'id': 'INTEGER',
        'name': 'VARCHAR',
        'datetime': 'TIMESTAMP',
        'department_id': 'INTEGER',
        'job_id': 'INTEGER'
    },
    'jobs': {
        'id': 'INTEGER',
        'job': 'VARCHAR'
    },
    'departments': {
        'id': 'INTEGER',
        'department': 'VARCHAR'
    }
}