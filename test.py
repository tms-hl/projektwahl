import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")
project = db.get_project(2)
print(project)

if project is None:
    print("Projekt nicht gefunden!")
else:
    print(project.name)