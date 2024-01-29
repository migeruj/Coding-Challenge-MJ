from pydantic import BaseModel

class NumEmployeesGrouped(BaseModel):
    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int