from db.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = 'peliculas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    categoria = Column(String)
    year = Column(Integer)
    score = Column(Float)

    def __repr__(self):
        return f'Movie: {self.title}'
