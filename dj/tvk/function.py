from .models import Risk
import csv
import io



def imns_to_choice(imns_list):
    rez = []
    for i_imns in imns_list:
        buf = (i_imns.id, i_imns.number)
        rez.append(buf)
    return rez

def handle_upload_file(f):
    file = f.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    
    rez = []
    for line in reader:
        if len(line) != 2:
            return None
        rez.append(line)
        
    return rez

def update_risk(list):
    code = []
    for i_elem in list:
        code.append(i_elem[0])
        
    risks = Risk.objects.all()
    
    #disable old risk
    for i_risk in risks:
        if i_risk.code not in code:
            i_risk.enable = False
            i_risk.save()
            
    for i_elem in list:
        risk = Risk.objects.filter(code=i_elem[0])
        if risk.exists():
            risk = risk.first()
            risk.name = i_elem[1]
            risk.enable = True
            risk.save()
        else:
            risk = Risk()
            risk.code = i_elem[0]
            risk.name = i_elem[1]
            risk.save()