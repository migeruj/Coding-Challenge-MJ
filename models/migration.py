from pydantic import BaseModel
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

schemas = {
    'employees': {
        'id': int,
        'name': str,
        'datetime': str,
        'department_id': int,
        'job_id': int
    },
    'jobs': {
        'id': int,
        'job': str
    },
    'departments': {
        'id': int,
        'department': str
    }
}