from flask import Flask
from flask import request, render_template

app = Flask(__name__)
    
"""
Ab hier werden die einzelnen Seiten eingefügt
"""

@app.get("/neu.html")
def neu():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('neu.html', param=param)

@app.get("/übersicht_projekte.html")
def übersicht_projekte():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('übersicht_projekte.html', param=param)

@app.get("/Wahl_fertig.html")
def Wahl_fertig():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('Wahl_fertig.html', param=param)

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8081)

