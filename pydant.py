from pydantic import StrictInt
from pydantic import BaseModel
class newi(BaseModel):
    name:str
    age:StrictInt
dicto={'name':"Laraib",'age':30}
p1=newi(**dicto)
def insert_patient_data():
    print(p1.age)
    print(p1.name)
    print("inserted data")
insert_patient_data()
def helper2(p: newi):
    print(p.name)
    print(p.age)
dicto2={'name':'akkad','age':44}
p2=newi(**dicto2)
helper2(p2)
