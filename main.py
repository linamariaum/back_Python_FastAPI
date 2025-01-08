## Resumen de requerimientos
"""
pip install fastapi uvicorn
pip install PyJWT
pip install SQLAlchemy
extension vscode sqlite viewer from Florian Klampfer
"""
##-------------------

from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
# Pydantic es una libreria que permite validar los datos que se envian a traves de la API, basado en Modelos
from pydantic import BaseModel, Field
from typing import Optional

class Persona(BaseModel):
    numero_identificacion: int
    nombre: str
    apellido: str
    edad: int
    genero: str

app = FastAPI(
    title='Backend API',
    description='API FastApi',
    version='0.0.1'
   )

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
    """Function printing bienvenida."""
    return {"mensaje": "Bienvenidos a Personas FastAPI"}

@app.get("/api/personas", response_model=List[Persona])
async def obtener_personas() -> List[Persona]:
    """Function get Personas."""
    return personas

@app.post("/api/personas")
def crear_persona(persona: Persona):
    """Function create Persona."""
    personas.append(persona.dict())
    return persona

#-------------------------------------
class Pelicula(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(default='Titulo de la pelicula', min_length=3, max_length=60) # Se puede agregar validaciones a los campos
    categoria: str = Field(default='Categoria de la pelicula', min_length=10, max_length=100)
    anio: int = Field(default=2024)
    score: float = Field(default=0.0, ge=1.0, le=10.0)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'anio': self.anio,
            'score': self.score
        }

peliculas = []

@app.get('/peliculas', tags=['Peliculas'])
def obtener_peliculas():
    # return [{'mensaje': 'Todas las peliculas'}]
    # return peliculas
    return JSONResponse(content=peliculas)

@app.get('/peliculas/{id}', tags=['Peliculas']) # Parametros de ruta
def obtener_pelicula(id: int = Path(ge=1, le=100)): # Se pueden agregar validaciones a los parametros de ruta
    return [{'mensaje': f'La peliculas {id}'}]

@app.get('/peliculas/', tags=['Peliculas'])
def obtener_pelicula_por_categoria(categoria: str = Query(min_length=3, max_length=15)): # Parametros de query
    return [{'mensaje': f'Las peliculas categoria {categoria}'}]

@app.get('/carros', tags=['Carros'])
def obtener_carros():
    return [{'mensaje': 'Todos los carros'}]

@app.post('/peliculas/forma3', tags=['Peliculas'])
def crear_pelicula(pelicula: Pelicula): # Utilizando la clase Pelicula
    peliculas.append(pelicula)
    return JSONResponse(status_code=201,
      content={
         'mensaje': f'Pelicula {pelicula.nombre} creada',
         'pelicula': pelicula.to_dict()
         }
    )

# Tokens
from myTokens import createToken, validateToken

class User(BaseModel):
    username: str
    password: str

@app.post('/login', tags=['Autenticacion'])
def login(user: User):
    if user.username == 'admin' and user.password == 'admin':
        token = createToken(user.model_dump())
        return JSONResponse(content=token)
    return JSONResponse(status_code=401, content={'mensaje': 'Usuario o contraseña incorrectos'})

# Para proteger las rutas
from fastapi.security import HTTPBearer
class BearerToken(HTTPBearer):
    token: str
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['username'] != 'admin':
            raise HTTPException(status_code=401, detail='Token invalido')

@app.get('/peliculas/protegida', tags=['Peliculas'], dependencies=[Depends(BearerToken())])
def obtener_peliculas_protegida():
    return JSONResponse(content=peliculas)

# Para conexion con bd
from db.database import Session, engine, Base
from models.movies import Movie as MovieModel # Estos alias con la intencion de que nuestro modelo de db no se confunda con el modelo de la API, suponiendo que ambas tuviesen el mismo nombre Movie

Base.metadata.create_all(bind=engine)

@app.post('/peliculas/db', tags=['Peliculas'])
def crear_pelicula_db(pelicula: Pelicula):
    db = Session()
   #  newMovie = MovieModel(
   #      name=pelicula.nombre,
   #      category=pelicula.categoria,
   #      year=pelicula.anio,
   #      score=pelicula.score
   #  ) or
    newMovie = MovieModel(**pelicula.model_dump())
    db.add(newMovie)
    db.commit()
    peliculas.append(pelicula)
    return JSONResponse(status_code=201,
      content={
         'mensaje': f'Pelicula {pelicula.nombre} creada',
         'pelicula': pelicula.to_dict()
         }
    )

from fastapi.encoders import jsonable_encoder

@app.get('/peliculas/protegida/db', tags=['Peliculas'], dependencies=[Depends(BearerToken())])
def obtener_peliculas_protegida_db():
    db = Session()
    data = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(data)) # Para convertirlo a un formato jsonable

@app.get('/peliculas/db/{id}', tags=['Peliculas'])
def obtener_pelicula_db(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
         return JSONResponse(status_code=404, content={'mensaje': 'Pelicula no encontrada'})
    return JSONResponse(content=jsonable_encoder(data))

@app.put('/peliculas/db/{id}', tags=['Peliculas'])
def actualizar_pelicula_db(id:int, pelicula: Pelicula):
    db = Session()
    data: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
         return JSONResponse(status_code=404, content={'mensaje': 'Pelicula no encontrada'})
    data.nombre = pelicula.nombre
    data.categoria = pelicula.categoria
    data.year = pelicula.anio
    data.score = pelicula.score
    db.commit()
    return JSONResponse(
        status_code=200,
        content= {
            'mensaje': f'Pelicula {pelicula.nombre} actualizada',
            'pelicula': jsonable_encoder(pelicula)
            }        
        )

@app.delete('/peliculas/db/{id}', tags=['Peliculas'])
def eliminar_pelicula_db(id:int):
    db = Session()
    data: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not data:
         return JSONResponse(status_code=404, content={'mensaje': 'Pelicula no encontrada'})
    db.delete(data)
    db.commit()
    return JSONResponse(
        status_code=200,
        content={
            'mensaje': f'Pelicula {data.nombre} eliminada',
            'pelicula': jsonable_encoder(data)
         })

@app.get('/peliculas/db/', tags=['Peliculas'])
def obtener_pelicula_por_categoria_db(categoria: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(MovieModel).filter(MovieModel.category == categoria).all()
    if not data:
        return JSONResponse(status_code=404, content={'mensaje': 'Pelicula no encontrada'})
    return JSONResponse(content=jsonable_encoder(data))

# Para no tener todo el codigo en un solo archivo, se puede dividir en varios archivos usando Routes
## Para esto crearemos la carpeta routers

from routers.movie import routerMovie

app.include_router(routerMovie)
