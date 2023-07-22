from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Department, Risk, Imns, CIC
from .forms import DepartmentsForm, RiskForm, IMNSForm, CICForm, UploadRiskFileForm
from .function import handle_upload_file, update_risk


# Create your views here.
@login_required
def main(request:HttpRequest, page:int=1):
    user = request.user
    
    if user.access == 1 or user.access == 3 or user.access == 5:
        cic_list = CIC.objects.order_by('-id')
    else:
        cic_list = CIC.objects.filter(imnss=user.imns.id).order_by('-id')
    
    paginator = Paginator(cic_list, 10)
    page_obj = paginator.get_page(page)
    
    context = {'page_obj': page_obj}
    return render(request, 'tvk/main.html', context=context)

@login_required
def cic(request:HttpRequest, id:int=None):
    user = request.user
    
    cic_form = CICForm()
    
    if id:
        cic = CIC.objects.get(id=id)
        cic_form = CICForm(instance=cic)
    
    if user.access == 2 or user.access == 4:
        cic_form.fields['imnss'].queryset = Imns.objects.filter(id=user.imns.id)
        cic_form.fields['obj'].queryset = Imns.objects.filter(id=user.imns.id)
    
    context = {'form': cic_form}
    
    return render(request, 'tvk/cic.html', context=context)

@login_required
def save_cic(request:HttpRequest):
    if request.method == "POST":
        id = request.POST.get('id', '')
        if id != '':
            cic = CIC.objects.get(id=id)
            cic_form = CICForm(instance=cic, data=request.POST)
        else:
            cic_form = CICForm(data=request.POST)
        if cic_form.is_valid():
            cic_form.save()
        else:
            return HttpResponse(str(cic_form.errors))
    return redirect('tvk:main')

@login_required
def department(request:HttpRequest, id:int=None):
    dep_form = DepartmentsForm()
    department_list = Department.objects.all()
    
    if id:
        dep_form = DepartmentsForm(instance=Department.objects.get(id=id))
    
    context = {'form': dep_form,
               'department_list': department_list}
    
    return render(request, 'tvk/departments.html', context=context)

@login_required
def save_department(request:HttpRequest):
    if request.method == 'POST':
        dep_form = DepartmentsForm(data=request.POST)
        if request.POST.get('id') != '':
            department = Department.objects.get(id=request.POST.get('id'))
            dep_form = DepartmentsForm(data=request.POST, instance=department)
        if dep_form.is_valid():
            dep_form.save()
        else:
            return HttpResponse(str(dep_form.errors))
    return redirect('tvk:department')

@login_required
def delete_department(request:HttpRequest, id:int=None):
    if id:
        department = Department.objects.get(id=id)
        department.delete()
    return redirect('tvk:department')

@login_required
def risk(request:HttpRequest, id:int=None):
    risk_form = RiskForm()
    file_form = UploadRiskFileForm()
    
    risk_list = Risk.objects.order_by('-enable', 'code')
    
    if id:
        risk = Risk.objects.get(id=id)
        risk_form = RiskForm(instance=risk)
    
    context = {'form': risk_form,
               'file_form': file_form,
               'risk_list': risk_list}
    
    return render(request, 'tvk/risk.html', context=context)

@login_required
def save_risk(request:HttpRequest):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        if id != '':
            risk = Risk.objects.get(id=id)
            risk_form = RiskForm(data=request.POST, instance=risk)
        else:
            risk_form = RiskForm(data=request.POST)
        if risk_form.is_valid():
            risk_form.save()        
        else:
            return HttpResponse(str(risk_form.errors))
    
    return redirect('tvk:risk')

@login_required
def delete_risk(request:HttpRequest, id:int=None):
    if id:
        risk = Risk.objects.get(id=id)
        risk.delete()
    return redirect('tvk:risk')

@login_required
def upload_file(request:HttpRequest):
    if request.method == 'POST':
        file_form = UploadRiskFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            list = handle_upload_file(request.FILES['file'])
            if list:
                update_risk(list)
        else:
            return HttpResponse(str(file_form.errors))
    return redirect('tvk:risk')

@login_required
def imns(request:HttpRequest, id:int=None):
    imns_form = IMNSForm()
    
    imns_list = Imns.objects.order_by('number')
    
    if id:
        imns = Imns.objects.get(id=id)
        imns_form = IMNSForm(instance=imns)
    
    context = {'form': imns_form,
               'imns_list': imns_list}
    return render(request, 'tvk/imns.html', context=context)

@login_required
def save_imns(request:HttpRequest):
    if request.method == 'POST':
        imns_form = IMNSForm()
        id = request.POST.get('id', '')
        if id != '':
            imns = Imns.objects.get(id=id)
            imns_form = IMNSForm(data=request.POST, instance=imns)
        else:
            imns_form = IMNSForm(data=request.POST)
        if imns_form.is_valid:
            imns_form.save()
        else:
            return HttpResponse(str(imns_form.errors))
    return redirect('tvk:imns')

@login_required
def delete_imns(request:HttpRequest, id:int=None):
    if id:
        imns = Imns.objects.get(id=id)
        imns.delete()
    return redirect('tvk:imns')
