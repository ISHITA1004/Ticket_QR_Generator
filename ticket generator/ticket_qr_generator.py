from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import qrcode
from io import BytesIO
import base64

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TicketInfo(BaseModel):
    name: str
    phone: str

@app.options("/generate_ticket_qr")
async def options_generate_ticket_qr():
    return {}  # This handles the OPTIONS preflight request

@app.post("/generate_ticket_qr")
async def generate_ticket_qr(ticket_info: TicketInfo):
    try:
        # Create QR code instance
        qr = qrcode.QRCode(version=1, box_size=10, border=5)

        # Add data to QR code
        data = f"Name: {ticket_info.name}\nPhone: {ticket_info.phone}"
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a bytes buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_image = buffer.getvalue()

        # Encode the image to base64
        qr_base64 = base64.b64encode(qr_image).decode('utf-8')

        return {
            "qr_code": qr_base64,
            "message": "QR code generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)