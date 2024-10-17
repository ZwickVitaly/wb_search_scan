from server.server_main import app
import uvicorn

app = app

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", workers=4)