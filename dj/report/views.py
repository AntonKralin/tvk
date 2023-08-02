from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ChoosePeriodForm, FilterForm
from tvk.models import Department, Imns, CIC, Examination


# Create your views here.
@login_required
def choose_period(request:HttpRequest):
    choose_form = ChoosePeriodForm()
    
    context = {'form': choose_form}
    return render(request, 'report/choose_period.html', context=context)

@login_required
def report(request:HttpRequest):
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
            
            rez_dep = []
            for i_dep in departments:
                dep_filt = b_cic.filter(departments=i_dep)
                if not dep_filt or dep_filt.count == 0:
                        rez_dep.append(0)
                        rez_dep.append(0)
                        continue
                        
                c1 = 0
                c2 = 0
                for i_cic in dep_filt:                    
                    exam = Examination.objects.filter(obj=i_imns, cic=i_cic).exclude(count_contravention=0)
                    c2 = exam.count()
                    if c2 != 0:
                        c1 += 1
                rez_dep.append(c1)
                rez_dep.append(c2)
            
            sum1 = 0
            sum2 = 0
            for i in range(len(rez_dep)):
                if i == 0 or i % 2 == 0:
                    sum1 += rez_dep[i]
                else:
                    sum2 += rez_dep[i]
            
            buf_rez.append(sum1)
            buf_rez.append(sum2)      
            buf_rez.extend(rez_dep) 
            
            rez.append(buf_rez)
            count += 1
        
        #итого
        buf_rez_list = []
        len_list = (departments.count() * 2) + 5
        for i_rez in range(3, len_list):
            buf_count = 0
            for j_rez in rez:
                buf_count += j_rez[i_rez]
            buf_rez_list.append(buf_count)
        
        buf_rez = []
        buf_rez.append('')
        buf_rez.append('итого')
        buf_rez.append('')
        buf_rez.extend(buf_rez_list)
        rez.append(buf_rez)
        
        context = {'department_list': departments,
                   'rezult': rez}

        return render(request, 'report/report.html', context=context)
    
    return redirect('tvk:main')

@login_required
def contraventions(request: HttpRequest, page:int=1):
    user = request.user
    
    form = FilterForm()
    
    if user.access != 1 or user.access != 3 or user.access != 5:
        form.fields['obj'].queryset = Imns.objects.filter(id = user.imns.id)    
    
    subject = ''
    obj = ''
    if request.method == 'POST':
        form = FilterForm(data=request.POST)
        subject = form['subject'].value()
        obj = form['obj'].value()
    
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

        for i_exam in exam:
            cic_buf = {'risk': i_cic}
            cic_buf['exam'] = i_exam
            rez.append(cic_buf)
            
    paginator = Paginator(rez, 10)
    page_obj = paginator.get_page(page)        
    
    context = {'page_obj': page_obj,
               'form': form}
        
    return render(request, 'report/contraventions.html', context=context)