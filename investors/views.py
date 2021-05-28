from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import  messages
from .forms import RegistrationForm,LoginForm,DepositeForm
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import Account,RefferalProfile
from manager.models import *
from datetime import datetime, timedelta,date
from django.http import JsonResponse
from django.utils import timezone


def get_deadline():
	return datetime.today() + timedelta(days=1)




def home(request , **kwargs):
    '''code = str(kwargs.get('ref_code'))
    try:
        profile = Account.objects.get(ref_code= code)
        request.session['ref_profile'] = profile.id
        print(profile)
    except:
        pass'''
    return render(request, 'investors/index.html')





#dashboard
@login_required
def dashboard(request):
    user = request.user
    context ={}
    context['packs']  = Packages.objects.all()
    try:
        context['order']= Order.objects.get(user=user, complete=False)
        context['investment'] = Investment.objects.filter(user=user,status = 'complete')
    except:
        context['order']= None
        context['investment'] =None
    
    return render(request, 'investors/dashboard.html',context)



#fund_wallet
@login_required
def fund_wallet(request):
    user = request.user
    if request.POST:
        form = DepositeForm(request.POST)
        if form.is_valid():
            c_ = form.cleaned_data['code']
            code = VerificationCode.objects.filter(code=c_)[0]
            user.balance += code.package.amount
            user.deposited = True
            code.active = False

            pack_price = code.package.amount
            package = get_object_or_404(Packages, amount = pack_price)
            investment_item , created = Investment.objects.get_or_create(
                user=user,
                pack = package,
                end_date = get_deadline(),
                status = 'Active'
            )
            order_qs = Order.objects.filter(user=user)
            if order_qs.exists():
                order = order_qs[0]
                order.investment.add(investment_item)
                user.balance -= package.amount
                refered =  request.session.get('ref_profile')
                if refered is not None:
                    ref_by =Account.objects.get(username=refered)
                    amount = code.package.amount
                    perc = 5/100 * amount
                    ref_by.referral_balance += perc
                    ref_by.save()
                    user.bonus += perc
                    user.save()
                    code.save()
                    del request.session['ref_profile']
                    messages.success(request, f'Package Is Added!')
                    return redirect('dashboard')
                user.save()
                code.save()
                messages.success(request, f' Package Is Added ')
                return redirect('dashboard')
            else:
                order=Order.objects.create(user=user,complete=False)
                order.investment.add(investment_item)
                user.balance -= package.amount
                refered =  request.session.get('ref_profile')
                if refered is not None:
                    ref_by =Account.objects.get(username=refered)
                    amount = code.package.amount
                    perc = 5/100 * amount
                    ref_by.referral_balance += perc
                    ref_by.save()
                    user.bonus += perc
                    user.save()
                    code.save()
                    del request.session['ref_profile']
                    messages.success(request, f'Package Is Purchased!')
                    return redirect('dashboard')
                user.save()
                code.save()
                messages.success(request, f' Package Is Purchased ')
                return redirect('dashboard')


    else:
        form = DepositeForm()
    return render(request, 'investors/fund_wallet.html',{"form":form})



def user_history(request):
    user = request.user
    context = {
        'withdraw': Withdraw.objects.filter(user=user),
        'ref_withdraw': ReferalWithdraw.objects.filter(user=user),
    }
    return render(request, 'investors/user_history.html',context)

def user_downlines(request):
    user = request.user
    account = RefferalProfile.objects.get(user=user)
    myrecs = account.recom_profies()
    return render(request, 'investors/downlines.html',{"myrecs":myrecs})


def contact_us(request):
    #user = request.user
    return render(request, 'investors/contact.html')


def privacy(request):
    #user = request.user
    return render(request, 'investors/privacy.html')


def how_it_works(request):
    #user = request.user
    return render(request, 'investors/how_it_works.html')
#ajax


'''def purchase_plans(request):
    package_name = request.POST.get('pack_name')
    user = request.user
    package = get_object_or_404(Packages, amount = package_name)
    if user.balance >= package.amount:
        investment_item , created = Investment.objects.get_or_create(
            user=user,
            pack = package,
            end_date = get_deadline(),
            status = 'Active'
        )
        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            order.investment.add(investment_item)
            user.balance -= package.amount
            user.save()
            return JsonResponse({'user': ' Package Is Added '})
        else:
            order=Order.objects.create(user=user,complete=False)
            order.investment.add(investment_item)
            user.balance -= package.amount
            user.save()
            return JsonResponse({'user': ' Package Is Purchased '})
    else:
        return JsonResponse({'user':'Insuficient Funds to purchase'})'''



#credit user
def credit_user(request):
    user = request.user
    investment_id = request.POST.get('pack')
    investment = get_object_or_404(Investment, user=user, pk=investment_id)
    #if investment.withdraw == False :
    #investment.withdraw = True
    #investment.status = 'complete'
    investment.end_date = get_deadline()
    investment.status = 'Active'
    investment.save()
    #rio = 
    user.investment_earnings += investment.daily()
    user.save()
    return JsonResponse({'user':'credited'})
    '''else:
    return JsonResponse({'user':'notcredited'})'''

#withdraw
def withdraw(request):
    return render(request,  'investors/withdraw.html')
#withdrawjs
def user_withdraw(request):
    bank_name =  request.POST.get('bank_name')
    acc_name =  request.POST.get('acc_name')
    acc_num =  request.POST.get('acc_num')
    amount =  float(request.POST.get('amount'))
    #investment_id =  request.POST.get('investment')
    user =  request.user
    #investment = get_object_or_404(Investment, pk=investment_id,user=user)
    user_bal = user.investment_earnings
    if user_bal > amount:
        Withdraw.objects.create(
            user=user,
            bank_name = bank_name,
            account_number =acc_num,
            account_name=acc_name,
            amount=amount

        )
        #investment.p_with_status = False
        #investment.primary_withdraw = True
        #investment.save()
        #user.withdraw_total +=  amount
        user.investment_earnings -= amount
        user.save()
        return JsonResponse({'user':'withdrawal placed'})
    else:
        return JsonResponse({'user':'Insufficient Funds'})


#refwithdraw
def ref_user_withdraw(request):
    bank_name =  request.POST.get('ref_bank_name')
    acc_name =  request.POST.get('ref_acc_name')
    acc_num =  request.POST.get('ref_acc_num')
    user =  request.user
    amount = user.referral_balance
    if amount > 0:
        ReferalWithdraw.objects.create(
            user=user,
            bank_name = bank_name,
            account_number =acc_num,
            account_name=acc_name,
            amount=amount

        )
        user.referral_balance -=  amount
        user.save()
        return JsonResponse({'user':'withdrawal placed'})
    else:
        return JsonResponse({'user':'inssuficient funds'})



#contact us
def contact_js(request):
    name =  request.POST.get('name')
    email =  request.POST.get('email')
    message =  request.POST.get('message')
    date  = timezone.now()
    Message.objects.create(
        name=name,
        email=email,
        message=message,
        date = date
    )
    return JsonResponse({'user':'Thanks for reaching out. we will get back to you as soon as possible'})





#authenticaticion """
def login_view(request):
    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request,user)
                if destination:
                    return redirect(destination)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, 'investors/auth/login.html', {"form":form})



def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect





def logout_view(request):
    logout(request)
    return redirect('login_view')


def register_view(request,**kwargs):
    context = {}
    code = str(kwargs.get('ref_code'))
    try:
        profile = Account.objects.get(username= code)
        request.session['ref_profile'] = profile.username
        print(profile)
    except:
        pass
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            refered =  request.session.get('ref_profile')
            if refered is not None:
                recom_profile_user =Account.objects.get(username=refered)
                instance = form.save()
                RefferalProfile.objects.create(user=instance)
                recom_profile_user.refferal += 1
                recom_profile_user.save()
                registered_user = Account.objects.get(id=instance.id)
                registered_ref_by = RefferalProfile.objects.get(user =registered_user )
                registered_ref_by.recommended_by = recom_profile_user
                registered_ref_by.save()
                #registered_user = Account.objects.get(id=instance.id)
                #registered_user.refferal 
                messages.success(request, f'Account created !')
                return redirect('login_view')
            else:
                instance = form.save()
                RefferalProfile.objects.create(user=instance)
                messages.success(request, f'Account created !')
                return redirect('login_view')
    else:
        refered =  request.session.get('ref_profile')
        if refered is  not None:
            form = RegistrationForm(initial={'reffered_by': refered})
        else:
            form = RegistrationForm()
    return render(request, 'investors/auth/register.html',{"form":form})