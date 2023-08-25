from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.conf import settings
from .forms import ChoosePeriodForm, FilterForm, CheckingFilterForm
from tvk.models import Department, Imns, CIC, Examination, Risk
import csv
import os


# Create your views here.
@login_required
def choose_period(request:HttpRequest):
    """chose period"""
    choose_form = ChoosePeriodForm()

    context = {'form': choose_form}
    return render(request, 'report/choose_period.html', context=context)


@login_required
def report(request:HttpRequest):
    """report"""
    if 'raion' in request.POST:
        return report_function(request, subj_raion=True)
    elif '300' in request.POST:
        return report_function(request, subj_300=True)
    elif 'file' in request.POST:
        return unload_csv(request)
    else:
        return report_function(request)


def unload_csv(request:HttpRequest):
    user = request.user
    
    if user.access != 1 and user.access != 3 and user.access != 5:
        b_cic = CIC.objects.filter(imnss=user.imns)
    else:
        b_cic = CIC.objects.all()
    
    date_from = request.POST.get('date_from', None)
    date_to = request.POST.get('date_to', None)
    
    if date_from:
        b_cic = b_cic.filter(date_state__gte=date_from)
    if date_to:
        b_cic = b_cic.filter(date_state__lte=date_to)
        
    header = ['Субъект', 'Объект', '№ отчета', 'Дата утверждения', 'Дата с', 'Дата по',
              'Риск', 'Название риска', 'Документы', 'Нарушений', 'Краткая суть', 'Управление']
    with open(user.username + '.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for i_cic in b_cic:
            exam = Examination.objects.filter(cic=i_cic)
            for i_exam in exam:
                line = []
                line.append(i_cic.imnss.number)
                line.append(i_exam.obj.number)
                line.append(i_cic.number)
                line.append(i_cic.date_state)
                line.append(i_cic.date_from)
                line.append(i_cic.date_to)
                line.append(i_exam.risk.code)
                line.append(i_exam.risk.name)
                line.append(i_exam.count_all)
                line.append(i_exam.count_contravention)
                line.append(i_exam.description)
                line.append(i_exam.department.name)
                writer.writerow(line)
        
    #unload file
    file_path = os.path.join(settings.MEDIA_ROOT, user.username + '.csv')
    if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
    else:
        return redirect('tvk:main')
 
def report_function(request: HttpRequest, subj_300=False, subj_raion=False):
    if request.method == 'POST':
        date_from = request.POST.get('date_from', None)
        date_to = request.POST.get('date_to', None)

        departments = Department.objects.all()
        imns = Imns.objects.order_by('number').exclude(number=300)

        rez = []
        count = 1
        for i_imns in imns:
            buf_rez = []
            buf_rez.append(str(count))
            buf_rez.append(str(i_imns.shot_name))
            buf_rez.append(str(i_imns.number))

            b_cic =  CIC.objects.all()
            if date_from:
                b_cic = b_cic.filter(date_state__gte=date_from)
            if date_to:
                b_cic = b_cic.filter(date_state__lte=date_to)
            if subj_300:
                b_cic = b_cic.filter(imnss=Imns.objects.get(number=300))
            if subj_raion:
                b_cic = b_cic.exclude(imnss=Imns.objects.get(number=300))

            rez_dep = []
            exam = Examination.objects.filter(obj=i_imns, cic__in=b_cic).exclude(count_contravention=0)
            c1 = 0
            c2 = 0
            for i_dep in departments:

                dep_filt = exam.filter(department=i_dep)
                if not dep_filt or dep_filt.count == 0:
                    rez_dep.append(0)
                    rez_dep.append(0)
                    continue

                c1 = dep_filt.values('cic').distinct().count()        
                c2 = dep_filt.values('risk').distinct().count()

                rez_dep.append(c1)
                rez_dep.append(c2)

            #sum1 - cont all imns, sum2 -risk all imns
            sum1 = exam.values('cic').distinct().count()
            sum2 = exam.values('risk').distinct().count()

            buf_rez.append(sum1)
            buf_rez.append(sum2)      
            buf_rez.extend(rez_dep) 

            rez.append(buf_rez)
            count += 1

        #итого
        buf_rez_list = []
        for i_dep in departments:
            total_cic_dep = Examination.objects.filter(cic__in=b_cic, department=i_dep).exclude(count_contravention=0).values('cic').distinct().count()
            total_risk_dep = Examination.objects.filter(cic__in=b_cic, department=i_dep).exclude(count_contravention=0).values('risk').distinct().count()
            buf_rez_list.append(total_cic_dep)
            buf_rez_list.append(total_risk_dep)

        buf_rez = []
        buf_rez.append('')
        buf_rez.append('итого')
        buf_rez.append('')
        total_cic = Examination.objects.filter(cic__in=b_cic).exclude(count_contravention=0).values('cic').distinct().count()
        buf_rez.append(total_cic)
        total_risk = Examination.objects.filter(cic__in=b_cic).exclude(count_contravention=0).values('risk').distinct().count()
        buf_rez.append(total_risk)
        buf_rez.extend(buf_rez_list)
        rez.append(buf_rez)

        context = {'department_list': departments,
                   'rezult': rez}

        return render(request, 'report/report.html', context=context)

    return redirect('tvk:main')
    

@login_required
def contraventions(request: HttpRequest, page:int=1):
    """contravention"""
    user = request.user

    form = FilterForm()

    if user.access != 1 and user.access != 3 and user.access != 5:
        form.fields['obj'].queryset = Imns.objects.filter(id = user.imns.id)    

    subject = ''
    obj = ''
    risk = ''
    dep = ''
    if "subject" in request.GET:
        form = FilterForm(data=request.GET)
        subject = form['subject'].value()
        obj = form['obj'].value()
        risk = form['risk'].value()
        dep = form['department'].value()

    if subject == '':
        cic = CIC.objects.all()
    else:
        cic = CIC.objects.filter(imnss__pk=subject)

    rez = []
    for i_cic in cic:
        if user.access == 1 or user.access == 3 or user.access == 5:
            if obj == '':
                exam = Examination.objects.filter(cic=i_cic).exclude(count_contravention=0)
            else:
                exam = Examination.objects.filter(cic=i_cic, obj__pk=obj).exclude(count_contravention=0)
        else:
            exam = Examination.objects.filter(cic=i_cic, obj=user.imns).exclude(count_contravention=0)

        if risk != '':
            exam = exam.filter(risk__pk=risk)
        
        if dep != '':
            exam = exam.filter(department__pk=dep)

        for i_exam in exam:
            cic_buf = {'risk': i_cic}
            cic_buf['exam'] = i_exam
            rez.append(cic_buf)

    paginator = Paginator(rez, 10)
    page_obj = paginator.get_page(page)        

    context = {'page_obj': page_obj,
               'form': form}

    return render(request, 'report/contraventions.html', context=context)

@login_required
def checking(request:HttpRequest, page:int=1):
    """checking"""
    user = request.user

    form = CheckingFilterForm()

    subject = ''
    risk = ''
    if 'subject' in request.GET:
        form = CheckingFilterForm(data=request.GET)
        subject = form['subject'].value()
        risk = form['risk'].value()

    if subject == '':
        cic = CIC.objects.order_by('-pk')
    else:
        cic = CIC.objects.filter(imnss__pk=subject).order_by('-pk')

    rez = []
    for i_cic in cic:
        if user.access == 1 or user.access == 3 or user.access == 5:
            exam = Examination.objects.filter(cic=i_cic)
        else:
            exam = Examination.objects.filter(cic=i_cic, obj=user.imns)

        if risk != '':
            exam = exam.filter(risk__pk=risk)

        if exam.count() == 0:
            continue

        sum_all = exam.aggregate(Sum('count_all'))
        sum_cont = exam.aggregate(Sum('count_contravention'))
        cic_buf = {'risk': i_cic}
        risk_list = exam.values('risk').distinct()
        cic_buf['risk_list'] = Risk.objects.filter(id__in=risk_list)
        imns_list =exam.values('obj').distinct()
        cic_buf['imns_list'] = Imns.objects.filter(id__in=imns_list)
        dep_list = exam.values('department').distinct()
        cic_buf['dep_list'] = Department.objects.filter(id__in=dep_list)
        cic_buf['sum_all'] = sum_all['count_all__sum'] if sum_all['count_all__sum'] else 0
        cic_buf['sum_cont'] = sum_cont['count_contravention__sum'] if sum_cont['count_contravention__sum'] else 0
        rez.append(cic_buf)

    paginator = Paginator(rez, 20)
    page_obj = paginator.get_page(page)

    context = {'page_obj': page_obj,
               'form': form}

    return render(request, 'report/checking.html', context=context)
