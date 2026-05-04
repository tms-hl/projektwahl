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
    u = model.Person(1, "max.mustermann@tms-hl.org", "Max", "Mustermann")
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
    uid = get_current_user().uid
    
    if request.form.get("wahl1") is not None: 
        pid1 = int(request.form.get("wahl1"))
        pid2 = int(request.form.get("wahl2"))
        pid3 = int(request.form.get("wahl3"))
    
        db.add_choice(uid, pid1, pid2, pid3)
    
    return render_template('wahl.html')

query = "SELECT name FROM projekt WHERE pId = %s"

@app.get("/neu.html")
def neu():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('neu.html', param=param)

@app.get("/bestaetigen.html")
def bestaetigen():
   return render_template('bestaetigen.html')

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
