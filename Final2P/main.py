from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
from models_pelicula import modelPelicula, modelAuth
from genToken import createToken, validateToken
from fastapi.responses import JSONResponse
from middlewares import BearerJWT

app= FastAPI(
    title="Mi primer API",
    description="Alma Elizabeth Tapia León",
    version="1.0.0"
)

peliculas =[
    {"Titulo": "Fronze", "Genero": "Animación", "Año":2013, "Clasificación": "A"},
    {"Titulo": "Harry Potter", "Genero": "Fantasía", "Año": 2001, "Clasificación": "B"},
    {"Titulo": "Jurassic Park", "Genero": "Ciencia ficción", "Año": 1993, "Clasificación": "C"},
    {"Titulo": "Batman", "Genero": "Acción", "Año": 2008, "Clasificación": "C"},
    {"Titulo": "Intensamente", "Genero": "Animación", "Año": 2015, "Clasificación": "A"}
]

async def token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    try:
        token = authorization.split(" ")[1]  
        data = validateToken(token)
        return data
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post('/auth', tags=['Autentificacion'])
def crear_token(credenciales: modelAuth):
    if credenciales.mail == 'elileon27@example.com' and credenciales.passw == '123456789':
        token: str = createToken(credenciales.model_dump())
        return {"token de acceso": token}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")



#Guardar Peliculas
@app.post('/pelicula', response_model=modelPelicula, tags=['Peliculas'])
def guardar(pelicula:modelPelicula):
    for peli in peliculas:
        if peli["Titulo"]== pelicula.Titulo:
            raise  HTTPException(status_code=400,detail="Esta pelicula ya existe")
    pelicula_dict = pelicula.dict()
    peliculas.append(pelicula_dict)
    return pelicula_dict

#Editar Peliculas
@app.put('/pelicula/{Titulo}',response_model=modelPelicula, tags=['Peliculas'])
def actualizar(Titulo:str,peliculaActualizada:modelPelicula):
    for index,  peli in enumerate(peliculas):
        if peli ["Titulo"] == Titulo:
            peliculas[index].update(peliculaActualizada.model_dump())
            return peliculas[index]
    raise HTTPException(status_code=400,detail="Pelicula no encontrada")


#Eliminar Peliculas
@app.delete("/pelicula/{Titulo}", tags=['Peliculas'])
async def eliminar(Titulo: str, token_data: dict = Depends(BearerJWT())):
    for index, peli in enumerate(peliculas):
        if isinstance(peli, dict) and "Titulo" in peli:
            if peli["Titulo"].lower() == Titulo.lower():
                peliculas.pop(index)
                return {'Peliculas Registradas': peliculas}
    raise HTTPException(status_code=404, detail="Película no encontrada")

#Buscar pelicula 
@app.get('/pelicula/{Titulo}', tags=['Peliculas'])
def buscar(Titulo:str):
    for index,  peli in enumerate(peliculas):
        if peli ["Titulo"] == Titulo:
            return peliculas[index]
    raise HTTPException(status_code=400,detail="Pelicula no encontrada")

#Todas las peliculas
@app.get('/pelicula', tags=['Peliculas'])
def leer():
    return {'Peliculas Registradas' : peliculas}