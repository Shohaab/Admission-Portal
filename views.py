from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm, LoginForm, AdmissionForm
from django.contrib.auth.decorators import login_required
from .forms import  AdmissionForm
from .models import Admission
from django.core.paginator import Paginator


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'admission/sign_up.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('admission')  
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error('email', "No user with this email.")
    return render(request, 'admission/log_in.html', {'form': form})

@login_required
def admission_view(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.user = request.user  # ✅ Set the user manually
            admission.save()
            messages.success(request, '🎉 آپ کا فارم کامیابی سے جمع ہو گیا ہے!')
            return redirect('admission')  # ✅ Redirect to clear POST and prevent re-submission
        else:
            messages.error(request, '⚠️ براہ کرم تمام ضروری معلومات درست طریقے سے درج کریں۔')
    else:
        form = AdmissionForm()

    return render(request, 'admission/admission_form.html', {'form': form})


def show_data_view(request):
    query = request.GET.get('q')  # Get search query from search bar

    if query:
        students_list = Admission.objects.filter(
            first_name__icontains=query
        ) | Admission.objects.filter(
            last_name__icontains=query
        ) | Admission.objects.filter(
            father_name__icontains=query
        )
    else:
        students_list = Admission.objects.all().order_by('-id')

    paginator = Paginator(students_list, 10)  # 10 records per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    return render(request, 'admission/show_data.html', {'students': students})







def submission_success(request):
    return render(request, 'admission/success.html')



def logout_view(request):
    logout(request)
    return redirect('login')



def update_student(request,pk):
    student = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES,instance=student)
        if form.is_valid():
            form.save()
            return redirect('show_data')
    else:
        form = AdmissionForm(instance=student)
    return render(request, 'admission/update_student.html', {'form': form})        


def  delete_student(request,pk):
    student= get_object_or_404(Admission,pk=pk)
    if request.method =='POST':
      student.delete()
      messages.success(request, 'Record Is deleted')
      return redirect('show_data')
    return render(request, 'admission/confirm_delete.html',{'student':student})


def print_student(request,pk):
    student = get_object_or_404(Admission,pk=pk)
    return render(request,'admission/print_student.html',{'student':student})