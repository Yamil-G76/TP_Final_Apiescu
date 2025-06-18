
from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, EmailStr
import datetime

# region clases base

# region usuario , usuarioDetail , type 
class User(Base):
   __tablename__ = "usuarios"

   id = Column("id", Integer, primary_key=True)
   username = Column("username", String(50),nullable=False, unique=True )
   password = Column("password", String)
   id_userdetail = Column("id_userdetail", Integer, ForeignKey("userdetails.id"))
 
   relaUserdetail = relationship("UserDetail", backref="user", uselist=False)

   
 
   def __init__(self, username, password):
       self.username = username
       self.password = password
  #_________________________________________________________________________________________________________________


#______________________________________________________________________
class Type (Base):
   __tablename__ = "types"
   id=Column("id", Integer, primary_key=True)
   type = Column("type", String)

   def __init__(self,type):
   
      self.type =type

# endregion


# region pagos
class Payment (Base) :
   
   __tablename__ ="pagos"

   id = Column("id", Integer, primary_key=True)
   id_usuarioxcarrera = Column ("id_usuarioxcarrera" , Integer , ForeignKey("usuarioxcarrera.id"))
   amount = Column("amount", Integer)
   afect_moth = Column("afect_month", DateTime)
   created_at = Column("created_at", DateTime ,default=datetime.datetime.now() )

   relaPaymentUsuarioxcarrera=relationship("UsuarioXcarrera" , back_populates="relaUsuarioxcarreraPayment")

   def __init__(self,id_usuarioxcarrera,amount,afect_mount):
     self.id_usuarioxcarrera = id_usuarioxcarrera
     self.amount= amount
     self.afect_mount = afect_mount

# endregion 


# region carrera y materia
class UserDetail(Base):

   __tablename__ = "userdetails"


   id = Column("id", Integer, primary_key=True)
   dni = Column("dni", Integer)
   firstname = Column("firstname", String)
   lastname = Column("lastname", String)
   email = Column("email", String(80), nullable=False, unique=True)
   id_type = Column("id_type", Integer ,  ForeignKey("types.id"))


   relaUserdetailType= relationship("Type", uselist=False, backref="relaTypeUserdetail")
   relaUserdetailusuarioxcarrera=relationship("UsuarioXcarrera",uselist=True, back_populates="relausuarioxcarreraUserdetail")



   def __init__(self, dni, firstname, lastname, email,id_type):
       self.dni = dni
       self.firstname = firstname
       self.lastname = lastname
       self.email=email
       self.id_type =id_type


#_________________________________________________________________________________-
class UsuarioXcarrera (Base):
   __tablename__="usuarioxcarrera"
   id = Column("id", Integer, primary_key=True)
   id_userdetail = Column("id_userdetail", Integer ,  ForeignKey("userdetails.id"))
   id_carrera = Column("id_carrera", Integer ,  ForeignKey("carreras.id"))
   fecha_inicio = Column("fecha_inicio",DateTime)

   relausuarioxcarreraUserdetail=relationship("UserDetail", uselist=False, back_populates="relaUserdetailusuarioxcarrera")
   relausuariosxcarrerascareer = relationship("Career",uselist=False, back_populates="relausuariosxcarreras")
   relaUsuarioxcarreraPayment =relationship("Payment" , back_populates="relaPaymentUsuarioxcarrera")

   def __init__(self,id_carrera, fecha_inicio,id_userdetail =None):
      self.fecha_inicio=fecha_inicio
      self.id_carrera = id_carrera    
      if id_userdetail:
       self.id_userdetail = id_userdetail



#_________________________________________________________________________________________________________________________

class Career (Base): 
    __tablename__= "carreras"
    id = Column("id", Integer, primary_key=True)
    name = Column("name",String(50) )
    costo_mensual = Column("costo_mensual" , Integer) 
    duracion_en_meses = Column("duracion_en_meses" , Integer) 
    relausuariosxcarreras = relationship("UsuarioXcarrera",back_populates="relausuariosxcarrerascareer")

    def __init__(self,name,costo_mensual,duracion_en_meses): 
     self.name = name
     self.costo_mensual= costo_mensual
     self.duracion_en_meses = duracion_en_meses
     
   

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
# endregion

# endregion

# region session
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)  


session = Session()

# endregion

# region Basemodel 

class ImputUsuarioxcarrera(BaseModel):
   id_user : int
   id_carrera: int
   fecha_inicio: datetime.date

class Imputtype(BaseModel):
   type : str

class InputUser(BaseModel):
   username: str
   password: str
   email: EmailStr
   dni: int
   firstname: str
   lastname: str
   type :int
   id_carrera: int
   fecha_inicio : datetime.date
   
class InputLogin(BaseModel):
    username: str
    password: str


class Imputcareer(BaseModel):
   name :str
   costo_mensual : int
   duracion_meses : int


class ImputPayment(BaseModel):
   id_usuarioxcarrera :int
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


   