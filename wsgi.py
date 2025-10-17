from app import create_app
from app.openapi.swagger import init_swagger

app = create_app()
init_swagger(app)

if __name__ == "__main__":
    app.run(port=5000)