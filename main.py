from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
import re
import click
import os

app = Flask(__name__)



@app.route("/")
def index():
    files = os.listdir("datos")
    alerta = request.args.get("alerta")
    return render_template("index.html",alerta=alerta,files=files[::-1])

@app.route("/upload",methods=["POST"])
def subir_archivo():
    if "filename" not in request.form or "filedata" not in request.files:
        return redirect("/?alerta=Error al subir el archivo.")
    filename = request.form["filename"] if len(request.form["filename"]) > 0 else request.files["filedata"].filename
    match = re.search(".([a-z]|[A-Z]|[0-9])*$", request.files["filedata"].filename)
    new_filename = filename[:match.span()[0]]+(match.group() if match else "")
    request.files["filedata"].save("datos/"+new_filename)
    
    return redirect("/?alerta="+"Archivo subido como "+new_filename+".")

@app.route("/load/<filename>")
def cargar_archivo(filename):
    return send_from_directory("datos",filename)

@app.route("/delete/<filename>")
def eliminar_archivo(filename):
    files = os.listdir("datos")
    if filename not in files:
        return redirect("/?alerta="+"Archivo "+filename+" no encontrado.")
    os.remove("datos/"+filename)
    return redirect("/?alerta="+"Archivo "+filename+" eliminado.")

@click.command()
@click.option("-p","--port",type=int,help="Puerto de el servidor.")
def get_events(port="80"):
    app.run("0.0.0.0",port,True)

if __name__ == "__main__":
    get_events()