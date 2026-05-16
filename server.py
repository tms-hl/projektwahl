import yaml
import model
from usertools import *

from flask import Flask, Blueprint, url_for
from flask import g, request, redirect, render_template
from authlib.integrations.flask_client import OAuth

# Config laden
with open("config.yaml") as stream:
    config = yaml.safe_load(stream)
    
# Datenbank öffnen
db = model.Db(config['db']['host'], config['db']['name'], config['db']['user'], config['db']['password'])

# OAuth
oauth = OAuth(app)
provider = oauth.register(
    name=config['oauth']['name'],
    client_id=config['oauth']['client_id'],
    client_secret=config['oauth']['client_secret'],
    server_metadata_url=config['oauth']['server_metadata_url'],
    client_kwargs=config['oauth']['client_kwargs'],
)

# App einrichten
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = "https"
app.secret_key = config['secret_key']

@app.context_processor
def context():
    return dict(current_user=get_current_user(), is_organisator=is_organisator())

@app.before_request
def inject_db():
    g.db = db
    
# Anfragen bearbeiten
@app.get("/")
@app.get("/index.html")
@login_required
def projekte():
    liste = db.get_projects()
    return render_template('projekte.html', liste=liste)

@app.get("/projekt.html")
@login_required
def projekt():
   pid = request.args.get("pid")
   
   p = db.get_project(pid)
   
   return render_template("projekt.html", p=p)
   
@app.get("/wahl.html")
@app.post("/wahl.html")
@login_required
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
@login_required
def neu():
    if not is_organisator():
        return "Zugriff verweigert", 402
        
    users = db.get_users()
    return render_template('neu.html', users=users)

@app.post("/projektneu.html")
@login_required
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
    
    p.organisatoren = [model.Person(int(uid)) for uid in request.form.getlist('organisatoren[]')]
    
    pid = db.add_project(p)
    return render_template('projektneu.html', pid=pid)

@app.route("/login")
def login():
    next = request.args.get("next")
    if next is None:
        next = url_for("projekte")
    return provider.authorize_redirect(url_for("callback", next=next, _external=True))


@app.route("/callback")
def callback():
    token = provider.authorize_access_token()
    email = token["userinfo"]["email"]
    g.user = g.db.get_user_by_email(email)
    
    if g.user is None:
        return render_template("access_denied.html"), 401
    
    session["uid"] = g.user.uid
    
    next = request.args.get("next")
    if next is None:
        next = url_for("projekte")
    return redirect(next)


@app.route("/logout")
def logout():
    session.pop("uid", None)
    return "Ausgeloggt"
    
"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
