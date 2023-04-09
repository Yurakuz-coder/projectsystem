import datetime
from docxtpl import DocxTemplate
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

context = {}
context['contract_number'] = '1'
context['org_name'] = '2'
context['contract_end_date'] = '10.02.2022'
context['org_ur_address'] = 'this'
context['org_postal_address'] = 'check'
context['contract_start_date'] = datetime.date.today().strftime("«%d» %B %Y г.")

doc = DocxTemplate('./documents/contract_template.docx')

doc.render(context)

doc.save('test.doc')
