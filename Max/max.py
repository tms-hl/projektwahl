from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.get("/wahlfertig.html")
def template():
   param = {
      "id": request.args.get("id"),
      "name": request.args.get("name")
   }
   return render_template('wahlfertig.html', param=param)

"""
Dies steht immer am Ende. Bitte nicht löschen
"""
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
