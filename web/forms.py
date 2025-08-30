from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee, Customer, Product, Complaint, ComplaintUpdate,Remark

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["designation","phone","personal_details","salary"]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name","contact","address"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","tax"]
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["customer","product","level","description","latitude","longitude","assigned_to","status"]
        #fields = ['title', 'description', 'assigned_to', 'status'] 
        widgets = {
            "description": forms.Textarea(attrs={"rows":3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = Employee.objects.select_related("user").all()
        self.fields["assigned_to"].label_from_instance = lambda obj: f"{obj.user.username} ({obj.designation})"






            
            
            
class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = ComplaintUpdate
        fields = ["remark","status_snapshot"]
        widgets = {
            "remark": forms.Textarea(attrs={"rows":3}),
        }
        
        
class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }