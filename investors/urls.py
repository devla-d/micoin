from django.urls import path,include
from . import views

urlpatterns = [
    
     path('',views.home, name='home'),
     path('ref/<str:ref_code>/',views.register_view, name='register_view_ref'),
     path('auth/login/',views.login_view, name='login_view'),
     path('auth/register/',views.register_view, name='register_view'),
     path('auth/logout/',views.logout_view, name='logout_view'),
     path('Dashboard/',views.dashboard, name='dashboard'),
     path('invest/',views.fund_wallet, name='fund_wallet'),
     #path('packages/purchase/',views.purchase_plans, name='puchase_plans'),
     path('Credit/user/',views.credit_user, name='credit_user'),
     path('withdraw/',views.user_withdraw, name='user_withdraw'),
     path('Ref/withdraw/',views.ref_user_withdraw, name='ref_user_withdraw'),
     path('History/',views.user_history, name='user_history'),
     path('Downlines/',views.user_downlines, name='user_downlines'),
     path('Withdraw/',views.withdraw, name='withdraw'),
     path('contact-us/',views.contact_us, name='contact-us'),
     path('contact/message/',views.contact_js, name='contact_js'),
     path('privacy/',views.privacy, name='privacy'),
     path('about-us/',views.how_it_works, name='how_it_works'),



]
