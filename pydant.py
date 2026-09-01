from pydantic import StrictInt
from pydantic import BaseModel
class new(BaseModel):
    name:str
    age:StrictInt
dicto={'name':"Laraib",'age':"30"}
p1=new(**dicto)
def insert_patient_data():
    print(p1.age)
    print(p1.name)
    print("inserted data")
insert_patient_data(newboe)