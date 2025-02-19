import os
import uvicorn
from api.app import app

if __name__ == "__main__":
    host = os.getenv("BR_BOT_HOST", "0.0.0.0")
    port = int(os.getenv("BR_BOT_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
