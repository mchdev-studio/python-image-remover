import os
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from rembg import remove
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI()

# ✅ CORS Middleware (Fixes frontend blocked requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Ensure OPTIONS is allowed
    allow_headers=["*"],  # Allow all headers
)

# ✅ Handle CORS Preflight Requests (Important for Fetch API in browsers)
@app.options("/remove-bg/")
async def preflight():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    return JSONResponse(content={}, headers=headers)

# ✅ Hello World Route (For testing)
@app.get("/")
async def hello_world():
    return {"message": "Hello, World! FastAPI is running 🚀"}

# ✅ Background Removal Endpoint
@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):  # Expecting "file"
    input_image = await file.read()
    output_image = remove(input_image)

    # Convert processed image to bytes
    img = Image.open(BytesIO(output_image))
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    # ✅ Add CORS Headers in Response
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    return Response(content=img_io.getvalue(), media_type="image/png", headers=headers)

# ✅ Automatically detect PORT from environment (Render requires this)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
