import os

from dotenv import load_dotenv
from quotes import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=os.getenv("FLASK_RUN_PORT", "5000"),
        debug=os.getenv("DEBUG", "False").lower() == "true",
    )
