from flask import Flask
from flask import request, render_template

from model import Db

app = Flask(__name__)

@app.get("/wahlfertig.html")
def wahlfertig():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('wahlfertig.html', param=param)

@app.get("/neu.html")
def neu():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('neu.html', param=param)

@app.get("/projekte.html")
def projekte():
   return render_template('projekte.html')

@app.get("/projekt.html")
def projekt():
    pid = request.args.get("pid")
    pid = int(pid)

    datenbank = Db("10.0.0.4", "if_01", "if_01", "if_01")
    pj = datenbank.get_project(pid)
    print(pj.name)
    print(pj.beschreibung)
    
    return render_template('projekt.html', p=pj)

@app.get("/bestaetigen.html")
def bestaetigen():
   return render_template('bestaetigen.html')

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
