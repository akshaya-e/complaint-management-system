from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Employee, Customer, Product, Complaint, ComplaintUpdate, Remark
from .forms import LoginForm, EmployeeForm, CustomerForm, ProductForm,ComplaintForm, ComplaintUpdateForm,RemarkForm
from django.http import HttpResponse


# Create your views here.

def is_admin(user):   # superuser = Admin
    return user.is_superuser

def is_employee(user):  # has an Employee profile
    return hasattr(user, "employee") and not user.is_superuser

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "login.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    if is_admin(request.user):
        return render(request, "admin_home.html")
    elif is_employee(request.user):
        return redirect("employee_dashboard")
    return render(request, "no_role.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin_home.html")


@user_passes_test(is_admin)
def employee_list(request):
    employees = Employee.objects.select_related("user").all()
    return render(request, "employee_list.html", {"employees": employees})

@user_passes_test(is_admin)
def employee_create(request):
    if request.method == "POST":
        # Create a linked User (username, name) quickly
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password") or "changeme123"
        if not username:
            messages.error(request, "Username is required.")
        else:
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name)
            form = EmployeeForm(request.POST)
            if form.is_valid():
                emp = form.save(commit=False)
                emp.user = user
                emp.save()
                messages.success(request, "Employee created.")
                return redirect("employee_list")
            else:
                user.delete()
                messages.error(request, "Fix form errors below.")
    else:
        form = EmployeeForm()
    return render(request, "employee_form.html", {"form": form})

@user_passes_test(is_admin)
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=emp)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Employee updated.")
        return redirect("employee_list")
    return render(request, "employee_form.html", {"form": form, "edit": True, "emp": emp})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

# ---- Admin: Customers ----

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customer_list.html", {"customers": customers})

@user_passes_test(is_admin)
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customer_detail.html", {"customer": customer})

@user_passes_test(is_admin)
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Customer saved.")
        return redirect("customer_list")
    return render(request, "customer_form.html", {"form": form})

@user_passes_test(is_admin)
def customer_edit(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Customer updated.")
        return redirect("customer_list")
    return render(request, "customer_form.html", {"form": form, "edit": True})

# ---- Admin: Products ----

def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# ---- Admin: Complaints ----
@user_passes_test(is_admin)
def complaint_list(request):
    qs = Complaint.objects.select_related("customer","product","assigned_to").order_by("-created_at")
    return render(request, "complaint_list.html", {"items": qs})

@user_passes_test(is_admin)
def complaint_create(request):
    form = ComplaintForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        messages.success(request, "Complaint registered.")
        return redirect("complaint_list")
    return render(request, "complaint_form.html", {"form": form})

def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, "complaint_detail.html", {"complaint": complaint})


    
    
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == "POST":
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect("complaint_detail", pk=complaint.pk)
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, "complaint_form.html", {"form": form})


@login_required
@user_passes_test(is_employee)
def assigned_complaints(request):
    print("User:", request.user)
    print("Employee attribute exists?", hasattr(request.user, "employee"))
    try:
        emp = request.user.employee
        print("Employee instance:", emp)
    except Exception as e:
        print("Error getting employee:", e)
        return render(request, "assigned_complaints.html", {"complaints": []})

    complaints = Complaint.objects.filter(
        assigned_to=emp
    ).select_related("customer", "product")
    return render(request, "assigned_complaints.html", {"complaints": complaints})



#Employee side views
@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):
    # Make sure the user has an Employee profile
    if not hasattr(request.user, 'employee'):
        return redirect('login')  # or show an error

    emp = request.user.employee  # get Employee instance

    assigned_count = Complaint.objects.filter(assigned_to=emp).count()
    unassigned_count = Complaint.objects.filter(assigned_to__isnull=True).count()

    context = {
        'assigned_count': assigned_count,
        'unassigned_count': unassigned_count,
    }
    return render(request, 'employee_dashboard.html', context)

    
@login_required
def unassigned_complaints(request):
    items = Complaint.objects.filter(assigned_to__isnull=True)
    return render(request, "unassigned_complaints.html", {"items": items})

@login_required
def assigned_complaints(request):
    items = Complaint.objects.filter(assigned_to=request.user.employee)
    return render(request, "unassigned_list.html", {"items": items})


    
    
@login_required
def assign_to_me(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check if complaint is already assigned
    if complaint.assigned_to:
        messages.error(request, "This complaint is already assigned.")
        return redirect('unassigned_complaints')

    # Check if employee already has a complaint
    if Complaint.objects.filter(assigned_to=request.user.employee).exists():
        messages.error(request, "You already have an assigned complaint.")
        return redirect('unassigned_complaints')

    # Assign complaint
    complaint.assigned_to = request.user.employee
    complaint.save()
    messages.success(request, "Complaint successfully assigned to you.")
    return redirect('unassigned_complaints')





@login_required
def assign_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if complaint.assigned_to is None:
        complaint.assigned_to = request.user
        complaint.save()
        messages.success(request, "Complaint assigned to you.")
    else:
        messages.error(request, "Complaint is already assigned.")
    return redirect('unassigned_complaints')
    
    


    
@login_required
def add_remark(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    # Get all previous remarks and updates
    remarks = complaint.remarks.all().order_by('-created_at')
    updates = complaint.updates.all().order_by('-created_at')

    if request.method == "POST":
        if 'remark_submit' in request.POST:
            remark_form = RemarkForm(request.POST)
            update_form = ComplaintUpdateForm()
            if remark_form.is_valid():
                remark = remark_form.save(commit=False)
                remark.complaint = complaint
                remark.user = request.user
                remark.save()
                return redirect('add_remark', pk=complaint.pk)

        elif 'update_submit' in request.POST:
            update_form = ComplaintUpdateForm(request.POST)
            remark_form = RemarkForm()
            if update_form.is_valid():
                update = update_form.save(commit=False)
                update.complaint = complaint
                update.updated_by = request.user
                update.save()
                # Optionally update complaint status
                complaint.status = update.status_snapshot
                complaint.save()
                return redirect('add_remark', pk=complaint.pk)

    else:
        remark_form = RemarkForm()
        update_form = ComplaintUpdateForm()

    context = {
        'complaint': complaint,
        'remarks': remarks,
        'updates': updates,
        'remark_form': remark_form,
        'update_form': update_form
    }
    return render(request, "remark_form.html", context)


'''@login_required
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Complaint.STATUS_CHOICES).keys():
            complaint.status = new_status
            complaint.save()
    return redirect("assigned_complaints")'''




'''@login_required
@user_passes_test(is_employee)
def update_status(request, pk):
    c = get_object_or_404(Complaint, pk=pk, assigned_to=request.user.employee)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Complaint.STATUS_CHOICES):
            c.status = new_status
            c.save()
            ComplaintUpdate.objects.create(
                complaint=c, by_user=request.user, remark=f"Status -> {new_status}",
                status_snapshot=new_status
            )
            messages.success(request, "Status updated.")
    return redirect("assigned_complaints")'''
    
@login_required
@user_passes_test(is_employee)
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, assigned_to=request.user.employee)

    if request.method == "POST":
        new_status = request.POST.get("status")
        remark_text = request.POST.get("remark", "").strip()

        if new_status in dict(Complaint.STATUS_CHOICES):
            # 🔹 Update complaint main status
            complaint.status = new_status
            complaint.save()

            # 🔹 Save history entry in ComplaintUpdate
            ComplaintUpdate.objects.create(
                complaint=complaint,
                by_user=request.user,
                remark=remark_text if remark_text else f"Status changed to {new_status}",
                status_snapshot=new_status
            )

            messages.success(request, "Status and remark updated successfully!")

    return redirect("assigned_complaints")



def employee_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Optional: Only allow staff/employees
                login(request, user)
                return redirect('employee_dashboard')  # Change to your employee dashboard
            else:
                messages.error(request, "You are not an employee.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'employee_login.html')




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if role == "admin" and user.is_superuser:
                return redirect("admin_dashboard")
            elif role == "employee" and Employee.objects.filter(user=user).exists():
                return redirect("employee_dashboard")
            else:
                return render(request, "login.html", {"error": "Invalid role selection"})
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")



'''@login_required
@user_passes_test(lambda u: u.is_superuser)  # only admin can delete
def complaint_delete(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    complaint.delete()
    messages.success(request, f"Complaint #{pk} deleted successfully.")
    return redirect("complaint_list")'''