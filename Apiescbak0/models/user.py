
from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, EmailStr
import datetime


# region clases base
class User(Base):
   __tablename__ = "usuarios"

   id = Column("id", Integer, primary_key=True)
   username = Column("username", String(50),nullable=False, unique=True )
   password = Column("password", String)
   email = Column("email", String(80), nullable=False, unique=True)
   id_userdetail = Column("id_userdetail", Integer, ForeignKey("userdetails.id"))
  # id_career= Column("id_career", Integer, ForeignKey("carreras.id"), nullable=True ,default=None)

 #  relaUserCareer = relationship("Career", backref="relaCareerUser")
   relaUserdetail = relationship("UserDetail", backref="user", uselist=False)

   relaUserPayments= relationship("Payment", uselist=True, back_populates="relaPaymentUser")
 
   def __init__(self, username, password, email):
       self.username = username
       self.password = password
       self.email = email

    #_________________________________________________________________________________________________________________
class Payment (Base) :
   
   __tablename__ ="pagos"

   id = Column("id", Integer, primary_key=True)
   id_career =Column("id_career", Integer , ForeignKey("carreras.id") )
   id_user = Column ("id_user" , Integer , ForeignKey("usuarios.id"))
   amount = Column("amount", Integer)
   afect_moth = Column("afect_month", DateTime)
   created_at = Column("created_at", DateTime ,default=datetime.datetime.now() )

   relaPaymentUser=relationship("User", uselist=False , back_populates="relaUserPayments")
   relaPaymentCareer = relationship("Career", uselist=False,backref= "relaUserCareer")

   def __init__(self,career_id,user_id,amount,afect_mount):
     self.career_id = career_id 
     self.user_id = user_id
     self.amount= amount
     self.afect_mount = afect_mount

#_________________________________________________________________________________________________________________________
class Career (Base): 
    __tablename__= "carreras"
    id = Column("id", Integer, primary_key=True)
    name = Column("name",String(50) )
    
    def __init__(self,name): 
     self.name = name


#____________________________________________________________________________________________________________________------

class Materia(Base):
   __tablename__ = "materias"

   id = Column("id", Integer, primary_key=True)
   name = Column("name", String )
   status = Column("status", String)

   
   def __init__(self, name, status, ID_User):
       self.name = name
       self.status = status
       self.Id_User = ID_User

#______________________________________________________________________________________________________________________-
class UserDetail(Base):

   __tablename__ = "userdetails"


   id = Column("id", Integer, primary_key=True)
   dni = Column("dni", Integer)
   firstname = Column("firstname", String)
   lastname = Column("lastname", String)
   type = Column("type", String)

   def __init__(self, dni, firstname, lastname, type):
       self.dni = dni
       self.firstname = firstname
       self.lastname = lastname
       self.type = type

# endregion

# region session
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)  


session = Session()

# endregion

# region Basemodel 

class ImputMaterias(BaseModel):
    name:str
    status:str


#class GetMateriaByID(BaseModel):
 

class InputUser(BaseModel):
   username: str
   password: str
   email: EmailStr
   dni: int
   firstname: str
   lastname: str
   type :str

   
class InputLogin(BaseModel):
    username: str
    password: str


class Imputcareer(BaseModel):
   name :str


class ImputPayment(BaseModel):
   id_career : int
   id_user :int
   amount :int
   afect_mount:datetime.date

# endregion

"""class InputUserChanges(BaseModel):
   username: str
   email: EmailStr
   password: str
   dni :Integer
   firstName :str
   lastName :str
   type :str
   relauserdetail : User.relaUserdetail.
   
     
class InputUserChanges(BaseModel):
   username: str
   email: EmailStr
   password: str 
   


   @user.put("/users/dniChange")
def dni_update(usrToChange: InputUserChanges):
   user = session.query(User).filter(User.username == usrToChange.username).first()
   if not user:
       return JSONResponse(
           status_code=404, content={"detail": "Usuario no encontrado"}
       )
   
   user.relaUserdetail = usrToChange.dni
   session.commit()
   session.refresh(user)
   return {"mensaje": "dni cambiado!!", "usuario": user}

   
   

@user.put("/users/emailChange")
def email_update(usrToChange: InputUserChanges):
   user = session.query(User).filter(User.username == usrToChange.username).first()
   if not user:
       return JSONResponse(
           status_code=404, content={"detail": "Usuario no encontrado"}
       )
   EmailExist = session.query(User).filter(User.email == usrToChange.email).first()
   if EmailExist:
       return JSONResponse(status_code=404, content={"detail": "Email ya existe"})
   user.email = usrToChange.email
   session.commit()
   session.refresh(user)
   return {"mensaje": "Email actualizado!!", "usuario": user }

@user.put("/users/passwordChange")
def password_update(usrToChange: InputUserChanges):
   user = session.query(User).filter(User.username == usrToChange.username).first()
   if not user:
       return JSONResponse(
           status_code=404, content={"detail": "Usuario no encontrado"}
       )
   user.password = usrToChange.password
   session.commit()
   session.refresh(user)
   return {"mensaje": "Password cambiada!!", "usuario": user}


   """


   