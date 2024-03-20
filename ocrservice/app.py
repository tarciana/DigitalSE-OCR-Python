from faststream import FastStream
from faststream.rabbit import RabbitBroker
from minio import Minio
from io import BytesIO
from PIL import Image
import pytesseract
import json
from pydantic import BaseModel

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672")
app = FastStream(broker)

minio_bucket = "images"

minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)

class UploadedFile(BaseModel):
    user_id: int
    document_id: int
    file_name: str


@broker.subscriber("ocr")
async def handle(message):
    print(message)
    try:
        uploaded_file = UploadedFile(**message)
        print("User ID:", uploaded_file.user_id)
        print("Document ID:", uploaded_file.document_id)
        print("File Name:", uploaded_file.file_name)
    
        objeto = minio_client.get_object(minio_bucket, uploaded_file.file_name)
        imagem_bytes = objeto.read()
        imagem = Image.open(BytesIO(imagem_bytes))

            # Extrair texto usando Tesseract
        texto_extraido = pytesseract.image_to_string(imagem)

            # Imprimir o texto extraído
        print(texto_extraido)
    except Exception as e:
        print(f"Erro ao transformar a mensagem em uma instância Pydantic: {e}")
