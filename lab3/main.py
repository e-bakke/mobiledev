from docxtpl import DocxTemplate
import random
import os
import subprocess


try:
    from comtypes import client
except ImportError:
    client = None


def doc2pdf_linux(doc):
    """
    convert a doc/docx document to pdf format (linux only, requires libreoffice)
    :param doc: path to document
    """
    cmd = 'libreoffice --convert-to pdf'.split() + [doc]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=10)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)


'''list of vars:
    bank, bik,account_number1,
    INN, KPP, payee, account_number2 
    number_of_payment, day, month, year
    supplier, buyer, reason
    internet, int_count, int_unit, int_price, int_sum,
    sms, sms_count, sms_unit, sms_price, sms_sum,
    calls, cl_count, cl_unit, cl_price, cl_sum}
    price, nds
    director, accountant
'''

a = []  # 0-calls, 1-sms, 2-useless, 3-internet, 4-Mb
def readbillings(doc):
    f=open(doc, 'r', encoding='utf-8')
    s=f.readlines()
    for i in s:
        q=i.split()
        a.append(q[0])
    return 0

readbillings('calls_and_sms.txt')
readbillings('internet.txt')

price=round(float(a[0])+float(a[1])+float(a[3]),2)
nds=round(price*0.13,2)
vars=['Сберыч','044525700','30101810200000000700',
      '7722737766','772201001','Получатель_name','40702810900000002453',
      str(random.random())[2:4],'1','январь','2020',
      'Поставщик_name','Покупатель_name','Основание №1',
      'интернет',a[4],'Mb','',a[3],
      'смс','1','-','',a[1],
      'звонки','1','минута','',a[0],
      price,nds,
      'Руководитель_name','Бухгалтер_name']

doc = DocxTemplate("template.docx")
context = { 'bank':vars[0], 'bik':vars[1],'account_number1':vars[2],
    'INN':vars[3], 'KPP':vars[4], 'payee':vars[5], 'account_number2':vars[6],
    'number_of_payment':vars[7], 'day':vars[8], 'month':vars[9], 'year':vars[10],
    'supplier':vars[11], 'buyer':vars[12], 'reason':vars[13],
    'internet':vars[14], 'int_count':vars[15], 'int_unit':vars[16], 'int_price':vars[17], 'int_sum':vars[18],
    'sms':vars[19], 'sms_count':vars[20], 'sms_unit':vars[21], 'sms_price':vars[22], 'sms_sum':vars[23],
    'calls':vars[24], 'cl_count':vars[25], 'cl_unit':vars[26], 'cl_price':vars[27], 'cl_sum':vars[28],
    'price':vars[29], 'nds':vars[30],
    'director':vars[31], 'accountant':vars[32]}
doc.render(context)
doc.save("generated_doc.docx")
doc2pdf_linux('generated_doc.docx')
os.system('rm generated_doc.docx')