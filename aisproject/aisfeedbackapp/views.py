from django.shortcuts import render,redirect
from .models import ClientData,ClientFeedback
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.db.models import Count


user1 = ""
def loginpage(request):
    if request.method == "GET":
        return render(request, 'loginpage.html')

    else:
        global user1
        user1 = request.POST.get('user1').lower()
        password1 = request.POST.get('password')
        print(user1,password1,'👍👍👍👍')
        user = authenticate(username=user1, password=password1)
        print(user,'✔✔')
        if user is not None:
            login(request, user)
            if user.is_staff:  # Check if the user is an admin
                return redirect('admin_panel1')  # Redirect to the admin panel
            else:
                return redirect('feedbackpage')  # Redirect to the customer feedback page
        else:
            messages.error(request, 'Invalid login credentials. Please try again')
            return redirect('loginpage')

def registration(request):
    if request.method == 'GET':
        return render(request, 'clientregister.html')

    else:
        user_type = request.POST.get('userType')
        fName = request.POST.get('fullName')
        userId=request.POST.get('userId').lower()
        email = request.POST.get('email')
        mob = request.POST.get('mobile')
        add = request.POST.get('address')
        pwd = request.POST.get('password')
        confirm_pwd = request.POST.get('confirmPassword')
        admin_code1 = request.POST.get('adminCode')
        # Your password validation logic here

        if pwd == confirm_pwd:
            # Create user and save registration data
            my_user = User.objects.create_user(username=userId, email=email, password=pwd)
            my_user.is_staff = True if user_type == 'admin' else False
            my_user.save()

            maindata = ClientData(
                user_type=user_type,
                user_id =userId,
                fullName=fName,
                email_id=email,
                mobile=mob,
                address=add,
                password=pwd,
                admin_code=admin_code1  # Save admin code if user type is admin
            )
            maindata.save()

            messages.success(request, 'Registration successful')

            if user_type == 'admin':
                return redirect('loginpage')
            elif user_type == 'customer':
                return redirect('loginpage')
        else:
            messages.error(request, 'Password and confirm password must be same')
            # Additional password validation error messages
            return redirect('registration')

the_user = None
@login_required(login_url="loginpage")
def feedbackpage(request):
    if request.method == "GET":
        global the_user
        the_user = ClientData.objects.get(user_id = user1 )

        print(the_user)
        return render(request, 'feedback.html',{'user':the_user})
    else:
        ClientFeedback(
            Name=the_user.fullName,
            Concern=request.POST.get('concern'),
            Help=request.POST.get('help'),
            YourFeedback=request.POST.get('feedback')
            ).save()
        return render(request, 'submission.html')

@login_required(login_url="loginpage")
def submissionpage(request):
    return render(request,'submission.html')


def successpage(request):
    return render(request,'successpage.html')


def logoutpage(request):
    logout(request)
    return render(request,'loginpage.html')


@login_required(login_url="loginpage")
def admin_panel(request):
    clients = ClientData.objects.all()
    feedbacks = ClientFeedback.objects.all()

    context = {
        'clients': clients,
        'feedbacks': feedbacks,
    }

    return render(request, 'admin_panel.html', context)

@login_required(login_url="loginpage")
def admin_panel1(request):
    if request.method=="GET":

        total_customers = ClientData.objects.count()
        total_feedbacks = ClientFeedback.objects.count()
        name=ClientData.objects.get(user_id=request.user.username)
        data = ClientData.objects.values('fullName')

        labels = ['Customers', 'Feedbacks', 'Remaining']
        sizes = [total_customers, total_feedbacks, 100 - (total_customers + total_feedbacks)]

        # Plotting the pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Saving the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Embedding the image in the HTML response
        image_uri = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
#second chart
        fig, ax = plt.subplots(figsize=(2, 5))  # Adjust width and height as needed

        # Create a bar graph with different colors
        labels = ['customers','Feedbacks']
        counts = [total_customers, total_feedbacks]
        colors = ['blue', 'yellow']  # Specify colors for each bar

        bars = plt.bar(labels, counts, color=colors)
        plt.xlabel('Categories')
        plt.ylabel('Counts')

        # Add count annotations above each bar
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.1, str(count), ha='center')

        # Saving the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Embedding the image in the HTML response
        image_uri1 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

    context = {
        'image_uri': image_uri,
        'image_uri1': image_uri1,
        'name':name,
        'data':data
        }

    return render(request, 'admin_panel1.html', context)



@login_required(login_url="loginpage")
def clients_data(request):
    data=ClientData.objects.all()
    data2=ClientData.objects.all()
    total_registrations=data2.count()
    return render(request, 'clients_data.html', {'data': data,'data2':data2,'total_registrations':total_registrations})

@login_required(login_url="loginpage")
def clients_feedback(request):
    data1 =ClientFeedback.objects.all()

    total_registrations1=data1.count()
    return render(request, 'clients_feedback.html', {'data1': data1,'total_registrations1':total_registrations1})
