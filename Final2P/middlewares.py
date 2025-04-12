from genToken import validateToken
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer


class BearerJWT(HTTPBearer):
    async def _call_(self, request: Request):
        auth = await super()._call_(request)
        data = validateToken(auth.credentials)

        if not isinstance(data, dict): 
            raise HTTPException(status_code=401, detail="Token inválido")

        if data.get('mail') != 'elileon27@example.com':  
            raise HTTPException(status_code=403, detail="Credenciales no válidas")

        return data