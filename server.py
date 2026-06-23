import yaml
import model

from flask import Flask
from flask import request, redirect, render_template

# Config laden
with open("config.yaml") as stream:
    config = yaml.safe_load(stream)
    
# Datenbank öffnen
db = model.Db(config['db']['host'], config['db']['name'], config['db']['user'], config['db']['password'])

def get_current_user():
    return model.User(1, "max.mustermann@tms-hl.org", "Max", "Mustermann")

# App einrichten
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/'
app.secret_key = 'secret' #config['secret_key']

@app.context_processor
def context():
    return dict(current_user=get_current_user(), is_organisator=is_organisator())

@app.before_request
def inject_db():
    g.db = db
    
# Anfragen bearbeiten
@app.get("/")
@app.get("/index.html")
def projekte():
    #liste = db.get_projects()
    return "OK" #render_template('projekte.html', liste=liste)

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
    if not is_organisator():
        return "Zugriff verweigert", 402
        
    users = db.get_users()
    return render_template('neu.html', users=users)

@app.post("/projektneu.html")
def projektneu():
    if not is_organisator():
        return "Zugriff verweigert", 402

    p = model.Projekt()
    p.name = request.form['name']
    p.beschreibung = request.form['beschreibung']
    p.plaetze_min = int(request.form['plaetze_min'])
    p.plaetze_max = int(request.form['plaetze_max'])
    p.klasse_min = int(request.form['klasse_min'])
    p.klasse_max = int(request.form['klasse_max'])
    
    p.organisatoren = [int(uid) for uid in request.form.getlist('organisatoren[]')]
    
    pid = db.add_project(p)
    return render_template('projektneu.html', pid=pid)

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
