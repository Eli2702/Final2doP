from fastapi import FastAPI, HTTPException
from models_pelicula import modelPelicula, modelAuth
from genToken import createToken
from fastapi.responses import JSONResponse


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

#Guardar Peliculas
@app.post('/pelicula', response_model=modelPelicula, tags=['Peliculas'])
def guardar(pelicula:modelPelicula):
    for peli in peliculas:
        if peli["Titulo"]== pelicula.Titulo:
            raise  HTTPException(status_code=400,detail="Esta pelicula ya existe")
    
    peliculas.append(pelicula)
    return pelicula

#Editar Peliculas
@app.put('/pelicula/{Titulo}',response_model=modelPelicula, tags=['Peliculas'])
def actualizar(Titulo:str,peliculaActualizada:modelPelicula):
    for index,  peli in enumerate(peliculas):
        if peli ["Titulo"] == Titulo:
            peliculas[index].update(peliculaActualizada)
            return peliculas[index]
    raise HTTPException(status_code=400,detail="Tarea no encontrada")


#Eliminar Peliculas
@app.delete('/pelicula/{Titulo}', tags=['Peliculas'])
def eliminar(Titulo:str):
    for index,  peli in enumerate(peliculas):
        if peli["Titulo"] == Titulo:
            return peliculas.pop(index)
    raise HTTPException(status_code=400,detail="Esta pelicula no se puede borrar")


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


@app.delete('/pelicula',tags=['Peliculas'])
def eliminar(credenciales:modelAuth):
    if credenciales.mail == 'elileon27@example.com' and credenciales.passw == '123456789':
        token: str= createToken(credenciales.model_dump())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso":"Usuario no cuenta con permiso"}