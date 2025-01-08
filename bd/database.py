import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'peliculas.sqlite' # Nombre de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__)) # Directorio actual, ruta para la base de datos
databaseUrl = f'sqlite:///{base_dir}/{sqliteName}' # Ruta completa de la base de datos
#databaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}' # Otra forma de hacer la ruta completa de la base de datos

engine = create_engine(databaseUrl, echo=True) #,connect_args={"check_same_thread": False}) # Crear el motor de la base de datos

Session = sessionmaker(bind=engine) # Crear la sesion de la base de datos

Base = declarative_base() # Crear la base de datos declarativa, que se va a usar como clase que representan las tablas de la base de datos

