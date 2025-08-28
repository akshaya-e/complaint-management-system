from django.contrib import admin
from .models import Employee, Customer, Product, Complaint, ComplaintUpdate,Remark


# Register your models here.

#admin.site.register(Employee)
#admin.site.register(Customer)
#admin.site.register(Product)
#admin.site.register(Complaint)
#admin.site.register(ComplaintUpdate)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "designation", "phone")
    search_fields = ("user__username", "designation", "phone")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact")
    search_fields = ("name", "contact")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "tax")
    search_fields = ("name",)

'''@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ("complaint", "employee", "remark", "status_snapshot", "updated_at")'''
    #search_fields = ("complaint__customer__name", "employee__username", "remark")

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "assigned_to", "status", "level", "created_at")
    list_filter = ("status", "level")
    search_fields = ("customer__name", "product__name", "assigned_to__user__username")
    autocomplete_fields = ("customer", "product", "assigned_to")

'''@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ("complaint", "employee", "remark", "created_at")'''
    #search_fields = ("complaint__customer__name", "employee__username", "remark")
    
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ["complaint", "updated_by", "remark", "created_at"]

class RemarkAdmin(admin.ModelAdmin):
    list_display = ["complaint", "user", "text", "created_at"]

admin.site.register(ComplaintUpdate, ComplaintUpdateAdmin)
admin.site.register(Remark, RemarkAdmin)



