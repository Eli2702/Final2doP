from pydantic import BaseModel,Field,EmailStr

class modelPelicula(BaseModel):
    Titulo: str = Field(..., min_length=4, max_length=25, description="Solo letras sin espacios min 4 max 25")
    Genero: str = Field(..., min_length=4, max_length=25, description="Solo letras sin espacios min 4 max 25")
    Año: int = Field(..., ge=1000, le=9999, description="Año debe tener 4 dígitos")
    Clasificación: str = Field(..., min_length=1, max_length=1, description="Solo letras sin espacios min 1 max 1")
    

class modelAuth(BaseModel):
    mail: EmailStr
    passw: str = Field(..., min_lenth=8, strip_whitespace=True, description="Solo letras sin espacios min 8")