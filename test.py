import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")

p = model.Projekt()
p.name = "Test1"
p.beschreibung = "Test 1 Beschreibung"
p.plaetze_min = 1
p.plaetze_max = 100
p.klasse_min = 4
p.klasse_max = 7

db.add_project(p)
print("ok")