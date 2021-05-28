from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from .decorators import manager_required
from .models import *
from investors.models import Account
from  .forms import CodeForm
import random
import json
import uuid


class SearchView(ListView):
    model = Account
    template_name = 'manager/users.html'
    context_object_name = 'accounts'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Account.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
        return object_list


@manager_required
def admin_dashboard(request):
    context = {
        "accounts": Account.objects.all().count(),
        "investments": Investment.objects.all().count(),
        "withdraws"  : Withdraw.objects.all().count(),
        "ref_withdraw" : ReferalWithdraw.objects.all().count(),
    }
    return render(request, 'manager/dashboard.html',context)



@manager_required
def admin_dashboard_withdraw(request):
    withdraws = Withdraw.objects.all()
    return render(request, 'manager/withdraws.html',{"withdraws":withdraws})


@manager_required
def admin_dashboard_refwithdraw(request):
    context = {
         "ref_withdraws"  : ReferalWithdraw.objects.all(),
     }
    return render(request, 'manager/ref-withdraws.html',context)


@manager_required
def admin_dashboard_users(request):
    context = {
         "accounts"  : Account.objects.all(),
     }
    return render(request, 'manager/users.html',context)



@manager_required
def admin_dashboard_investment(request):
    context = {
         "investments"  : Investment.objects.all(),
     }
    return render(request, 'manager/investments.html',context)






@manager_required
def admin_dashboard_user_detail(request,pk,username):
    acc = get_object_or_404(Account, pk=pk, username=username)
    context = {
        "acc":acc,
        'withdraws':Withdraw.objects.filter(user=acc),
        'refwithdraws':ReferalWithdraw.objects.filter(user=acc),
        'investment':Investment.objects.filter(user=acc)
    }
    return render(request, 'manager/userdetail.html',context)



@manager_required
def admin_dashboard_with_detail(request,pk):
    withdraw = get_object_or_404(Withdraw, pk=pk)
    return render(request, 'manager/withdetail.html',{"withdraw":withdraw})


@manager_required
def admin_dashboard_messages(request):
    msgs = Message.objects.all()
    return render(request, 'manager/messages.html',{"msgs":msgs})


@manager_required
def admin_dashboard_refwith_detail(request,pk):
    ref_withdraw = get_object_or_404(ReferalWithdraw, pk=pk)
    return render(request, 'manager/ref_withdraw.html',{"ref_withdraw":ref_withdraw})


def rand_str():
      return str(random.randint(1000000000, 9999999999))

@manager_required
def admin_dashboard_verification_code(request):
    if request.POST:
        name = request.POST.get('name')
        plans = request.POST.get('plans')
        package = get_object_or_404( Packages, amount=plans)
        VerificationCode.objects.create(
            name = name,
            code = rand_str(),
            package = package
        )
        return redirect("admin_dashboard_verification_code")
    context = {
        "code":VerificationCode.objects.all(),
        "package": Packages.objects.all()
        
    }
    return render(request, 'manager/verification_code.html',context)






def approve_withdraw(request):
    pk = request.POST.get('pk')
    #invest_id = request.POST.get('invest_id')
    user_pk  = request.POST.get('user_pk')
    user =  Account.objects.get(pk=user_pk)
    #investment= get_object_or_404(Investment, pk=invest_id,user=user)
    withdraw = get_object_or_404(Withdraw, pk=pk)
    withdraw.complete = True
    #investment.p_with_status =True
    #investment.save()
    withdraw.save()
    user.withdraw_total += withdraw.amount
    user.save()
    return JsonResponse({"user":"approved"})

def approve_ref_withdraw(request):
    pk = request.POST.get('pk')
    #invest_id = request.POST.get('invest_id')
    user_pk  = request.POST.get('user_pk')
    user =  Account.objects.get(pk=user_pk)
    #investment= get_object_or_404(Investment, pk=invest_id,user=user)
    ref_withdraw = get_object_or_404(ReferalWithdraw, pk=pk)
    ref_withdraw.complete = True
    #investment.p_with_status =True
    #investment.save()
    ref_withdraw.save()
    user.withdraw_total += ref_withdraw.amount
    user.save()
    return JsonResponse({"user":"approved"})
