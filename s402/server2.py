# Importamos la clase constructora del servidor
from fastapi import FastAPI

from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

# Para iniciar el servidor:
# $ python -m uvicorn server1:app --reload

# Para finalizar el servidor:
# $ [PRESIONA CTRL+C]

# Creamos un objeto de servidor (app)
app = FastAPI()

# Definir una ruta, decorando una funcion
# @app.<metodo>("<ruta>") - Escucha la <ruta> en el <metodo>
#   get - Accesible desde la URL (o el navegador)
#   post - Privada bajo la URL (modo peticion)
# def <nombre>() - Controlar la peticion (darle una respuesta a un cliente)
#   * Cada peticion llama a la funcion <nombre>
@app.get("/")
def home():
    return "Hola soy el Servidor 2 🥹"

@app.post("/login") # curl http://127.0.0.1:8000/test
def login(user: User):

    token = jwt(user)

    return {
        "token": token,
    }

@app.post("/test") # curl -X POST http://127.0.0.1:8000/test
def test_post(token: str):

    validate(token)

    user = getUser(token)

    return {
        "x": 456,
        "y": False,
        "z": "Mundo",
        "w": 5.4321,
        "v": [
            "piña",
            "fresa",
            "melon"
        ]
    }