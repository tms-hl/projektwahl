import yaml
import model

from flask import Flask
from flask import request, render_template

# Config laden
with open("config.yaml") as stream:
    config = yaml.safe_load(stream)
    
# Datenbank öffnen
db = model.Db(config['db']['host'], config['db']['name'], config['db']['user'], config['db']['password'])

# App einrichten
app = Flask(__name__)

# Funktionen
def get_current_user():
    u = model.Schueler(3, "max.mustermann@tms-hl.org", "Max", "Mustermann")
    return u

# Anfragen bearbeiten
@app.get("/")
@app.get("/index.html")
def projekte():
    liste = db.get_projects()
    return render_template('projekte.html', liste=liste)

@app.get("/projekt.html")
def projekt():
   pid = request.args.get("pid")
   
   p = db.get_project(pid)
   
   return render_template("projekt.html", p=p)
   
@app.get("/wahl.html")
@app.post("/wahl.html")
def wahl():
   return render_template('wahl.html')

@app.get("/neu.html")
def neu():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('neu.html', param=param)

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
