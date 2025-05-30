# from datetime import datetime
# from docxtpl import DocxTemplate


# doc = DocxTemplate("Образец.docx")
# context = { 
#     'current_datetime' : datetime.today().strftime("%d.%m.%y"),
#     'persons' : "1\n2\n3\n5",
#     'count' : 14,
# }
# doc.render(context)
# doc.save("выписка.docx")

from Modules.DataBaseManager import DataBaseManager
data = DataBaseManager()
print(data.select_oct_contengent_for_military_unit(11361))
