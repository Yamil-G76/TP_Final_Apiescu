from fastapi import APIRouter
from models.user import session, InputUser, User , InputLogin , UserDetail, Materia,ImputMaterias,Payment,ImputPayment,Career,Imputcareer#,GetMateriaByID
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from sqlalchemy.orm import (
   joinedload,
)  ## muy útil para devolver el objeto user con cada uno de sus userDetail, todo junto (técnica llamada join loading: carga con unión)

user = APIRouter()
userDetail = APIRouter()
materia = APIRouter()
career = APIRouter()
payment = APIRouter()

# region carreras 

@career.post("/Careers/new")
def crear_Career (carerr: Imputcareer):
    try:
        careernueva = Career(carerr.name)
        session.add(careernueva)
        session.commit()
        return "carrera creada"
    except  Exception as e:
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )
    finally: session.close()
    
@payment.post("/payments/new")
def confeccionar_pago (payment: ImputPayment):
    try:
        paynew= Payment(payment.id_career , payment.id_user,payment.amount, payment.afect_mount)
        session.add(paynew)
        session.commit()
        return "carrera creada"
    except  Exception as e:
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )
    finally: session.close()

@career.get("/career/all") 
def obtener_career() : 
    try:      
       res = session.query(Career).all
       return res
    except  Exception as e:
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )
    finally: session.close() 

@payment.get("/payment/all") 
def obtener_pagos() : 
    try:      
       res = session.query(Payment).all
       return res
    except  Exception as e:
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )
    finally: session.close() 





      


# endregion 


# region user
@user.post("/users/new")
def crear_usuario(user: InputUser):
   try:
       # Si el usuario cumple con la validación, y no hay errores, lo agregamos.
       if validate_username(user.username): 
           if validate_email(user.email):
             usuNuevo = User(user.username, user.password,user.email)
             usuDetailNuevo = UserDetail (user.dni,user.firstname,user.lastname,user.type   )
             usuNuevo.relaUserdetail=usuDetailNuevo
             session.add(usuNuevo)
             session.commit()
             return "usuario agregado"
           else:
               return"el mail ya existe"
       else:
           return "el usuario ya existe"
   except IntegrityError as e:  
       # Suponiendo que el mje de error contiene "username" para el campo duplicado
       if "username" in str(e):
           return JSONResponse(
               status_code=400, content={"detail": "Username ya existe"}
           )
       else:
           # Maneja otros errores de integridad
           print("Error de integridad inesperado:", e)
           return JSONResponse(
               status_code=500, content={"detail": "Error al agregar usuario"}
           )                        
   except Exception as e:
       print("Error inesperado:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al agregar usuario"}
       )
   finally: session.close()

@user.post("/users/login")
def login_user(us: InputLogin):
   try:
       user = session.query(User).filter(User.username == us.username).first()
       if user and user.password == us.password:
           return {"status": "success",
                   "token": "qwelkrlñqwkrlñqwkerñlkjwn",
                   "user": user.relaUserdetail,
                   "message":"User logged in successfully!"}

       else:
           return {"message": "Invald username or password"}
   except Exception as ex:
       print("Error ---->> ", ex)
   finally:
       session.close()


@user.get("/users/all")
def obtener_usuarios():
   try:
      return obtener_usuarios1()

   except Exception as e:
       print("Error al obtener usuarios:", e)
       return JSONResponse(
           status_code=500, content={"detail": "Error al obtener usuarios"}
       )
   
# login user que trae las carreras de los alumnos
@user.post("/users/loginUser")
def login_post(user: InputLogin):
    try:
        usu = User(user.username, user.password ,"")
        res = session.query(User).options(joinedload(User.relaUserdetail)).filter(User.username == usu.username).first()
        if res.password == usu.password:
            print("usuario correcto")
            return res
        else:
            return "as"
    except Exception as e:
        print(e)



# endregion

# region carrera
"""@materia.get("/materia/all")
def obtener_materias():
    
    try:
        materias = session.query(Materia).all()

        return materias      
    except Exception as e:
     print("Error inesperado:", e)
    return JSONResponse(
           status_code=500, content={"detail": "Error al leer todas las materias"}
       )



@materia.post("/materia/new")
def nueva_carrera(materia: ImputMaterias):
    try:
        MateriaNueva=Materia(materia.name,materia.status,materia.ID_User)
        session.add(MateriaNueva)
        session.commit()
        return "materia agregada"
    except Exception as e:
     print("Error inesperado:", e)
    return JSONResponse(
           status_code=500, content={"detail": "Error al agregar materia"}
       )


@materia.post("/materia/con/id_user")
def obtener_materia_con_ID_User( ID : GetMateriaByID):

    try:

        materias_usuario = session.query(Materia).filter(Materia.Id_User == ID.ID_User).all()
        print("lectura exitosa")
        return materias_usuario    
    except Exception as e:
        print(e)
    """
    
# endregion

# region funciones

def validate_username(value):
   existing_user = session.query(User).filter(User.username == value).first()
   session.close()
   if existing_user:
       return None
       ##raise ValueError("Username already exists")
   else:
       return value
   

def validate_email(value):
   existing_email = session.query(User).filter(User.email == value).first()
   session.close()
   if existing_email:
       ##raise ValueError("Username already exists")
       return None
   else:
       return value
   

def obtener_usuarios1():
    try:
        usuarios = session.query(User).options(joinedload(User.relaUserdetail)).all()
        print(len(usuarios))
        usuarios_con_detalles = []
        for usuario in usuarios:
            usuario_con_detalle = {
                "id": usuario.id,
                "username": usuario.username,
                "email": usuario.email,
                "dni": usuario.relaUserdetail.dni,
                "firstname": usuario.relaUserdetail.firstname,
                "lastname": usuario.relaUserdetail.lastname,
                "type": usuario.relaUserdetail.type,
                "password": usuario.password
            }
            usuarios_con_detalles.append(usuario_con_detalle)
        
        return JSONResponse(status_code=200, content=usuarios_con_detalles)

    except Exception as e:
        print("Error al obtener usuarios:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al obtener usuarios"}
        )
# endregion