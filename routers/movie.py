from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

routerMovie = APIRouter()

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

@routerMovie.post('/peliculas/forma1', tags=['Peliculas'], status_code=201)
def crear_pelicula_por_queryParams(id:int, nombre:str, categoria:str, anio: int, score: float): # Si se deja así y sin la importacion del Body, se debe enviar los datos por query
    return [{'mensaje': f'Pelicula {nombre} creada'}]

@routerMovie.post('/peliculas/forma2', tags=['Peliculas'])
def crear_pelicula_por_body(id:int = Body(), nombre:str = Body(), categoria:str = Body(), anio: int= Body(), score: float= Body()): # Así y con la importacion de Body, ya se puede enviar los datos por Body
    return [{'mensaje': f'Pelicula {nombre} creada'}]

@routerMovie.put('/peliculas/forma1/{id}', tags=['Peliculas'])
def actualizar_pelicula_por_queryParams(id:int, nombre:str = Body(), categoria:str = Body(), anio: int= Body(), score: float= Body()):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            pelicula['nombre'] = nombre
            pelicula['categoria'] = categoria
            return [{'mensaje': f'Pelicula {nombre} actualizada'}]

@routerMovie.put('/peliculas/forma2/{id}', tags=['Peliculas'])
def actualizar_pelicula(id:int, pelicula: Pelicula):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            pelicula['nombre'] = pelicula.nombre
            pelicula['categoria'] = pelicula.categoria
            return [{'mensaje': f'Pelicula {pelicula.nombre} actualizada'}]


@routerMovie.delete('/peliculas/{id}', tags=['Peliculas'])
def eliminar_pelicula(id:int):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            nombre = pelicula['nombre']
            peliculas.remove(pelicula)
            return [{'mensaje': f'Pelicula {nombre} eliminada'}]
