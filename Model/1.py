from OCR import main_for_ocr
from bot import Main_for_query

docum = main_for_ocr(r'/workspaces/SchemeSaathi/uploads/1.png')
result = Main_for_query("Tell me about the bihar student credit card scheme")

print(docum)
print(result)


