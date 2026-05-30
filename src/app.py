from flask import Flask
from src.models import Base, engine
from src.models.clientes import Clientes
from src.models.productos import Productos


app = Flask(__name__)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)

