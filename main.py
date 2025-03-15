import os
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI()

# Enable CORS (Fixes frontend CORS issues)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Hello World Route
@app.get("/")
async def hello_world():
    return {"message": "Hello, World! FastAPI is running 🚀"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):  # ✅ Expecting "file"
    input_image = await file.read()
    output_image = remove(input_image)

    # Convert processed image to bytes
    img = Image.open(BytesIO(output_image))
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    return Response(content=img_io.getvalue(), media_type="image/png")

# ✅ Automatically detect PORT from environment (Render requires this)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
