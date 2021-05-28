from django.urls import path,include
from .import views
from .views import SearchView

urlpatterns = [

    path('Dashboard/Admin/',views.admin_dashboard, name='admin_dashboard'),
    path('Dashboard/Admin/Search',SearchView.as_view(), name='search_view'),
    path('Dashboard/Admin/Wihdrawals/',views.admin_dashboard_withdraw, name='admin_dashboard_withdraw'),
    path('Dashboard/Admin/RefferalWihdrawals/',views.admin_dashboard_refwithdraw, name='admin_dashboard_refwithdraw'),
    path('Dashboard/Admin/Users/',views.admin_dashboard_users, name='admin_dashboard_users'),
    path('Dashboard/Admin/Investment/',views.admin_dashboard_investment, name='admin_dashboard_investment'),
    path('Dashboard/Admin/Users/<int:pk>/<str:username>',views.admin_dashboard_user_detail, name='admin_dashboard_user_detail'),
    path('Dashboard/Admin/Wihdrawals/<int:pk>/',views.admin_dashboard_with_detail, name='admin_dashboard_with_detail'),
    path('Dashboard/Admin/Wihdrawals/approve/',views.approve_withdraw, name='approve_withdraw'),
    path('Dashboard/Admin/RefWihdrawals/approve/',views.approve_ref_withdraw, name='approve_ref_withdraw'),
    path('Dashboard/Admin/Code/',views.admin_dashboard_verification_code, name='admin_dashboard_verification_code'),
    path('Dashboard/Admin/RefferalWihdrawals/<int:pk>/',views.admin_dashboard_refwith_detail, name='admin_dashboard_refwith_detail'),
    path('Dashboard/Admin/Messages/',views.admin_dashboard_messages, name='admin_dashboard_messages'),

]