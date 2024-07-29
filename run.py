from app import create_app
import os
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=os.environ.get("FLASK_DEBUG", True), 
        host=os.environ.get("FLASK_RUN_HOST", '0.0.0.0'),
        port=os.environ.get("FLASK_RUN_PORT", 8000)
    )  