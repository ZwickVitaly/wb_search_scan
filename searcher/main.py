from server.server_main import app
import uvicorn

app = app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", workers=4)