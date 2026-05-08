from fastapi import FastAPI

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run

app = FastAPI()
app.mount(
  "/static",
  StaticFiles(
    directory="static",
    html=True,
    check_dir=False,
  ),
  name="static",
)

@app.get("/")
def home():
  return {"message": "Hello, MedRush!"}

@app.get("/favicon.ico")
def favicon():
  return FileResponse(
    "static/MedRush.png",
    media_type="image/png"
  )

def main():
  run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
  main()

