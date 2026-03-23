import model
db = model.Db("intern.tms-hl.org", "if_01", "if_01", "if_01")
choice = db.get_choice(5)
print(choice)

