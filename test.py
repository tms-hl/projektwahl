import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")
Person = db.get_user(2)
print(user)

if user is None:
    print("Projekt nicht gefunden!")
else:
    print(user.name)