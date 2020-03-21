import os

from server.app.pis import create_app

app = create_app()

if __name__ == "__main__":
    app.run("0.0.0.0", port=os.getenv('PORT'))
