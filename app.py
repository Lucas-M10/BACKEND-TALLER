from flask import Flask, render_template, request, redirect
import requests
import os 
from models import db, Favorite

BASE_DIR = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "app.db")

# Aca creo la aplicacion y guardo en la variable app 
# Si se desea cambiar el nombre de la carpeta templates se deberia agregar esta sintaxis 
# app = Flask(__name__, tamplate_folder = "nombre_carpeta.html") 
app = Flask(__name__) 

# Guardamos la direccion de la pagina a una variable URL que devolvera la informacion de los personajes.
URL = "https://rickandmortyapi.com/api/character" 


app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"


app.config["SQLALCHEMY_DATABASE_MODIFICATIONS"] = False


db.init_app(app)

with app.app_context():
    db.create_all()

# Esto es un decorador de flask "cuando alguien entra a la ruta /, se ejecuta la funcion de abajo"
@app.route("/")
# URL/pagina 

# Se crea la funcion que es la que ejecuta cuando el usuario entra a la pagina principal 
def index ():

    #requests.get() se usa para hacer peticiones a una URL en este caso esta pidiendo la pagina y por defecto le pasa la pagina 1
    page = request.args.get ("page", 1)

    #
    name = request.args.get ("name")

    # Aca se pregunta si el personaje buscado se encontro o no si se encontro imprime los personaje y sino imprime el mensaje de "Personaje no encontrado" 
    if name :
        aux = requests.get (URL, params={"name": name})

        if aux.status_code != 200:
            # render_tamplate ("nombre.html" parametro_1, parametro_2) los parametros deben estar renderizados en el html 
            # Por defeco render_template busca en una carpeta templates y busca en este caso el archivo con nombre "index.html"
            
            return render_template("index.html", #En la carpeta de templates busca el archivo con nombre "index.html"
                                   personaje= [], # Pasa una lista vacia para que no recorra el for 
                                   search = True, # Pasa true porque el usuario realizo una busqueda 
                                   error_msj = "Personaje no encontrado")# va a imprimir este mensaje 
    
        data = aux.json()
        return render_template("index.html",
                               personaje= data["results"],#devuelve una lista donde accedemeos con la clave results donde estan los personajes 
                               search=True)


    #aca se esta pidiendo 
    aux = requests.get(URL, params={'page': page})

    data = aux.json()

    return render_template("index.html", 
                           personaje = data['results'], 
                           info=data["info"], 
                           search = False)

@app.route ("/save", methods = ["POST"])

def save ():
    # Aca estamos agarrando los campos que queremos agarrar de nuestro from 
    api_id = request.form["api_id"]
    name = request.form ["name"]
    image = request.form["image"]
    page= request.form.get("page", 1)

    if not Favorite.query.filter_by(api_id=api_id).first():
        fav= Favorite(api_id=api_id, name=name, image=image)

        db.session.add(fav)

        db.session.commit()

    return redirect(f"/?page={page}")


@app.route ("/favorite")
def favorites ():
    favorites = Favorite.query.all()
    return render_template("favorites.html", favorites= favorites, search=True)


@app.rout ("/delete/<int:id>", methods = ["POST"])
def delete(id):
    fav = Favorite.query.get(id)
    if fav:
        db.session.delete (fav)
        db.session.commit()

    return redirect("/favorites")

if __name__ == '__main__':
    app.run(debug=True)
