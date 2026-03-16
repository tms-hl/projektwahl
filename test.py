import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")
project = db.get_project(1)
print(project)