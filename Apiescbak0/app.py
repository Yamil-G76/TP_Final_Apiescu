import sys  # Importamos el módulo sys, que permite interactuar con el sistema y configurar el entorno de Python
sys.tracebacklimit = 1  # Limitamos la cantidad de líneas que se muestran en el traceback

from fastapi import FastAPI

from Rutas.users import user
from Rutas.users import materia
from Rutas.users import career
from Rutas.users import payment 
from Rutas.users import type


from fastapi.middleware.cors import CORSMiddleware
apiescu = FastAPI () 

apiescu.include_router(materia)
apiescu.include_router(user)
apiescu.include_router(career)
apiescu.include_router(payment)
apiescu.include_router(type)
apiescu.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials = True,
   allow_methods=["GET", "POST", "PUT", "DELETE"],
   allow_headers=["*"],
)


