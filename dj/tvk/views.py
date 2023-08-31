from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime
from .models import Department, Risk, Imns, CIC, Examination
from .forms import DepartmentsForm, RiskForm, IMNSForm, CICForm, UploadRiskFileForm,\
    ExaminationForm, FilterMainForm
from .function import handle_upload_file, update_risk


# Create your views here.
@login_required
def main(request:HttpRequest, page:int=1):
    """main"""
    user = request.user
    
    mainform = FilterMainForm()
    if user.access != 1 and user.access != 3 and user.access != 5:
        mainform.fields['obj'].queryset = Imns.objects.filter(id = user.imns.id)
        mainform.fields['subject'].queryset = Imns.objects.filter(id = user.imns.id)  
    
    
    subject = ''
    year = datetime.now().year
    if 'subject' in request.GET:
        mainform = FilterMainForm(data=request.GET)
        subject = mainform['subject'].value()
        year = mainform['year'].value()

    if user.access == 1 or user.access == 3 or user.access == 5:
        if subject != '':
            cic_list = CIC.objects.filter(imnss__pk=subject, date_state__year=year).order_by('-id')
        else:
            cic_list = CIC.objects.filter(date_state__year=year).order_by('-id')
    else:
        cic_list = CIC.objects.filter(imnss=user.imns.id, date_state__year=year).order_by('-id')
    
    cic_rez = []
    for i_cic in cic_list:
        exam_list = Examination.objects.filter(cic=i_cic.id)

        sum_all = exam_list.aggregate(Sum('count_all'))
        i_cic.sum_all = sum_all['count_all__sum'] if sum_all['count_all__sum'] else 0
        sum_cont = exam_list.aggregate(Sum('count_contravention'))
        i_cic.sum_cont = sum_cont['count_contravention__sum'] if sum_cont['count_contravention__sum'] else 0

        obj_list_buf = exam_list.values('obj').distinct()
        obj_list = []
        for i_obj in obj_list_buf:
            obj_list.append(Imns.objects.get(id=i_obj['obj']))
        i_cic.obj_list= obj_list
        risk_list_buf = exam_list.values('risk').distinct()
        risk_list = []
        for i_risk in risk_list_buf:
            risk_list.append(Risk.objects.get(id=i_risk['risk']))
        i_cic.risk_list = risk_list

        dep_list_buf = exam_list.values('department').distinct()
        dep_list = []
        for i_dep in dep_list_buf:
            dep_list.append(Department.objects.get(id=i_dep['department']))
        i_cic.dep_list = dep_list

        i_cic.exam_list = exam_list
        cic_rez.append(i_cic)

    paginator = Paginator(cic_rez, 20)
    page_obj = paginator.get_page(page)

    context = {'page_obj': page_obj,
               'form': mainform}
    return render(request, 'tvk/main.html', context=context)


@login_required
def cic(request:HttpRequest, id:int=None):
    """cic"""
    user = request.user

    cic_form = CICForm()

    if id:
        cic = CIC.objects.get(id=id)
        cic_form = CICForm(instance=cic)

    if user.access == 2 or user.access == 4:
        cic_form.fields['imnss'].queryset = Imns.objects.filter(id=user.imns.id)

    context = {'form': cic_form}

    return render(request, 'tvk/cic.html', context=context)


@login_required
def save_cic(request:HttpRequest):
    """save_cic"""
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
def view_cic(request:HttpRequest, id:int):
    """view_cic"""
    if id:

        cic = CIC.objects.get(id=id)
        exam_list = Examination.objects.filter(cic=cic)

        context = {'cic': cic,
                   'exam_list': exam_list}

        return render(request, 'tvk/view_cic.html', context=context)
    return redirect('tvk:main')


@login_required
def delete_cic(request:HttpRequest, id:int):
    """delete_cic"""
    if id:
        cic = CIC.objects.get(id=id)
        exam_list = Examination.objects.filter(cic=cic)
        for i_exam in exam_list:
            i_exam.delete()
        cic.delete()
    return redirect('tvk:main')


@login_required
def department(request:HttpRequest, id:int=None):
    """department"""
    dep_form = DepartmentsForm()
    department_list = Department.objects.all()

    if id:
        dep_form = DepartmentsForm(instance=Department.objects.get(id=id))

    context = {'form': dep_form,
               'department_list': department_list}

    return render(request, 'tvk/departments.html', context=context)


@login_required
def save_department(request:HttpRequest):
    """save_department"""
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
    """delete_deparment"""
    if id:
        department = Department.objects.get(id=id)
        department.delete()
    return redirect('tvk:department')


@login_required
def risk(request:HttpRequest, id:int=None):
    """risk"""
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
    """save_risk"""
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
    """delete risk"""
    if id:
        risk = Risk.objects.get(id=id)
        risk.delete()
    return redirect('tvk:risk')


@login_required
def upload_file(request:HttpRequest):
    """upload file"""
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
    """imns"""
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
    """save_imns"""
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
    """delete_imns"""
    if id:
        imns = Imns.objects.get(id=id)
        imns.delete()
    return redirect('tvk:imns')


@login_required
def exam(request:HttpRequest, cic:int, id:int=None):
    """exam"""
    form = ExaminationForm()

    user = request.user
    if user.access != 1:
        form.fields['obj'].queryset = Imns.objects.filter(id=user.imns.id)

    if id:
        exam = Examination.objects.get(id=id)
        form.fields['id'].initial = exam.id
        form.fields['obj'].initial = exam.obj
        form.fields['cic'].initial = cic
        form.fields['risk'].initial = exam.risk
        form.fields['department'].initial = exam.department
        form.fields['count_all'].initial = exam.count_all
        form.fields['count_contravention'].initial = exam.count_contravention
        form.fields['description'].initial = exam.description
    else:
        form.fields['cic'].initial = cic

    exam_list = Examination.objects.filter(cic=CIC.objects.get(id=cic))

    context = {'form': form,
               'exam_list': exam_list}

    return render(request, 'tvk/exam.html', context=context)


@login_required
def save_exam(request:HttpRequest):
    """save_exam"""
    if request.method == 'POST':
        id = request.POST.get('id', '')
        obj = request.POST.get('obj')
        risk = request.POST.get('risk')
        cic = request.POST.get('cic')
        dep = request.POST.get('department')
        count_all = request.POST.get('count_all')
        count_contravention = request.POST.get('count_contravention')
        description = request.POST.get('description')
        fio = request.POST.get('fio')

        exam = Examination()
        if id != '':
            exam = Examination.objects.get(id=id)

        exam.obj = Imns.objects.get(id=obj)
        exam.risk = Risk.objects.get(id=risk)
        exam.cic = CIC.objects.get(id=cic)
        exam.department = Department.objects.get(id=dep)
        exam.count_all = count_all
        exam.count_contravention = count_contravention
        exam.description = description
        exam.fio = fio
        exam.save()

        return redirect('tvk:exam', cic=cic)

    return redirect('tvk:main')


@login_required
def delete_exam(request:HttpRequest, id:int=None):
    """delet_exam"""
    if id:
        exam = Examination.objects.get(id=id)
        cic = exam.cic.id
        exam.delete()
        return redirect('tvk:exam', cic=cic)

    return redirect('tvk:main')
