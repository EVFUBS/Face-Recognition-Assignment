# uvicorn server:app --reload
# server to host face recognition model and return results
# take in image and return results

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
import tensorflow as tf
import io
from PIL import Image

app = FastAPI()

# allow CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model('face_model.h5')

names = ['Alvaro_Uribe', 'Andre_Agassi', 'Luke', 'Recep_Tayyip_Erdogan', 'Tiger_Woods', 'Winona_Ryder']

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/face_recognition")
async def face_recognition(file: UploadFile = File(...)):
    
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))   
    image = image.resize((224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    
    prediction = model.predict(image)
    prediction = names[prediction.argmax()]
    
    return {"prediction": prediction}


