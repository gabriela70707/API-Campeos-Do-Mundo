from typing import Optional
from pydantic import BaseModel #permite trabalhar com dados de forma eficiente , declarando tipos, declarando obrigatoriedade de preenchimento e alem disso 
#o pydantic pode converter um tipo automaticamnte quando ver que esse tipo foi inserido de forma incorreta


class Campeoes(BaseModel):
    id: Optional[int] = None  # Permite que o ID seja opcional
    nome: Optional[str] = None
    posicao: Optional[str] = None
    pais: Optional[str] = None
    ano: Optional[int] = None
    foto: Optional[str] = None
