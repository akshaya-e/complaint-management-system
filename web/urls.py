from django.urls import path
from . import views

urlpatterns = [
    # Admin-side CRUD
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/create/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/edit/", views.employee_edit, name="employee_edit"),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),

    path("customers/", views.customer_list, name="customer_list"),
    path("customers/create/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customer_edit"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    path("complaints/", views.complaint_list, name="complaint_list"),
    path("complaints/create/", views.complaint_create, name="complaint_create"),
    path("complaints/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    #path("complaints/<int:pk>/assign/", views.complaint_assign, name="complaint_assign"),

    # Employee-side
    path("dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("assigned/", views.assigned_complaints, name="assigned_complaints"),
    path("unassigned/", views.unassigned_complaints, name="unassigned_complaints"),
    path("complaints/<int:pk>/remark/", views.add_remark, name="add_remark"),
    path("complaints/<int:pk>/assign_me/", views.assign_to_me, name="assign_to_me"),
    path("complaints/<int:pk>/status/", views.update_status, name="update_status"),
    path("complaints/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    path("complaints/<int:pk>/edit/", views.complaint_update, name="complaint_update"),
    path("complaints/unassigned/", views.unassigned_complaints, name="unassigned_complaints"),
    path("complaints/assigned/", views.assigned_complaints, name="assigned_complaints"),
    path("complaints/<int:pk>/assign/", views.assign_to_me, name="assign_to_me"),
    
    path('login/employee/', views.employee_login, name='employee_login'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/assigned/', views.assigned_complaints, name='assigned_complaints'),
    path('employee/unassigned/', views.unassigned_complaints, name='unassigned_complaints'),
    path('employee/assign/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),
    path('employee/remark/<int:complaint_id>/', views.add_remark, name='add_remark'),
    
    path("assign/<int:pk>/", views.assign_to_me, name="assign_to_me"),
    path("remark/<int:pk>/", views.add_remark, name="add_remark"),
    path("status/<int:pk>/", views.update_status, name="update_status"),
    
    #path('', views.hom, name='hom'),
    path('login/', views.login_view, name='login'),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('complaints/<int:pk>/assign_me/', views.assign_to_me, name='assign_to_me'),
    #path('complaint/delete/<int:pk>/', views.complaint_delete, name='complaint_delete'),
    
    #path('unassigned/', views.unassigned_complaints, name='unassigned_complaints'),
    #path('assign/<int:pk>/', views.assign_to_me, name='assign_to_me'),
    
]
