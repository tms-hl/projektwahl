import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")
project = db.get_project(2)

if project is None:
    print("Projekt nicht gefunden!")
else:
    print(project.name)
    
user = db.get_user(5)
if user is None:
    print("Benutzer nicht gefunden!")
else:
    print(user.nachname, user.vorname)

projects = db.get_projects()
for p in projects:
    print(p.name)
    
c = db.get_choice(5)
print(c)

