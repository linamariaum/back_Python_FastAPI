from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

class Persona(BaseModel):
    numero_identificacion: int
    nombre: str
    apellido: str
    edad: int
    genero: str

app = FastAPI()

personas = [
   {
      "numero_identificacion": 1,
      "nombre": "Ana",
      "apellido": "Acosta",
      "edad": 20,
      "genero": "Femenino"
   },
   {
      "numero_identificacion": 2,
      "nombre": "Bernardo",
      "apellido": "Botero",
      "edad": 21,
      "genero": "Masculino"
   },
   {
      "numero_identificacion": 3,
      "nombre": "Camila",
      "apellido": "Cardona",
      "edad": 22,
      "genero": "Femenino"
   },
   {
      "numero_identificacion": 4,
      "nombre": "Daniel",
      "apellido": "Davila",
      "edad": 23,
      "genero": "Masculino"
   },
   {
      "numero_identificacion": 5,
      "nombre": "Elisa",
      "apellido": "Espinosa",
      "edad": 24,
      "genero": "Femenino"
   },
   {
      "numero_identificacion": 6,
      "nombre": "Franco",
      "apellido": "Fernandez",
      "edad": 25,
      "genero": "Masculino"
   }
]

@app.get("/api")
async def bienvenida():
 return {"mensaje": "Bienvenidos a Personas FastAPI"}

@app.get("/api/personas", response_model=List[Persona])
async def obtener_personas():
 return personas
