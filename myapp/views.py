import razorpay
from time import time

from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt

from myapp.models import Categories,Course,Level,UserCourse,Payment,contactdb,reviewdb

client = razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
# Create your views here.

def BASE(request):
    return render(request,"base.html")

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:6]
    course= Course.objects.filter(status='PUBLISH').order_by('-id')   

    context = {
        'category': category,
        'course': course,
    }
    return render(request,'Main/home.html',context,)

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()

    context ={
        'category':category,
        'level': level,
        'course': course,
        'FreeCourse_count' : FreeCourse_count,
        'PaidCourse_count' : PaidCourse_count,
    }
    return render(request,'Main/single_course.html',context)

def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course =Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    context = {
        'course': course
    }
    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})

def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request,'Main/contact_us.html',context)

def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    review = reviewdb.objects.all()
    context = {
        'category': category,
        'review': review
    }
    return render(request,'Main/about_us.html',context)

def LOGIN(request):
    return render(request,'Main/registration/login.html')

def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
    query = request.GET['query']
    course = Course.objects.filter(title__icontains= query)
    context = {
        'course': course,
        'category':category,
    }
    return render(request,"search/search.html",context)

def COURSE_DETAILS(request,id):
    category = Categories.get_all_category(Categories)
    cdata = Course.objects.all()
    selectcourse = Course.objects.all()
    course_id = Course.objects.get(id = id)
    try:
     check_enroll = UserCourse.objects.get(user = request.user, course = course_id)
     print(check_enroll)
    except UserCourse.DoesNotExist:
     check_enroll = None

    course = Course.objects.filter(id = id)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    reviews = reviewdb.objects.filter(selectcourse=course)
    context= {
        'course':  course,
        'category': category,
        'check_enroll': check_enroll,
        'cdata': cdata,
        'selectcourse': selectcourse,
        'reviews': reviews
    }
    return render(request,"course/course_details.html",context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request,'error/error404.html',context)

def CHECKOUT(request,id):
    course = Course.objects.get(id = id)
    action = request.GET.get('action')
    order = None
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,"Courses are successfully Enrolled")
        return redirect('my_course')
    
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            amount_cal = course.price - (course.price * course.discount / 100)
            amount = int(amount_cal) * 100
            currency = "INR"
            notes = {
                "name": f'{first_name}  {last_name}',
                "country": country,
                "address" : address_1,
                "city": city,
                "state": state,
                "postcode":postcode,
                "phone": phone,
                "email": email,
            }
            receipt = f"SKILLACADEMY-{int(time())}"
            order = client.order.create(
                {
                    'receipt':receipt,
                    'notes':notes,
                    'amount':amount,
                    'currency': currency,
                }
            )
            payment = Payment(
                course = course,
                user=request.user,
                order_id = order.get('id')
            )
            payment.save()

    context = {
        'course': course,
        'order': order,
    }

    return render(request,"checkout/checkout.html",context)

def My_Course(request):
    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course': course
    }
    return render(request,'course/mycourse.html',context)

@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method ==  'POST':
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_order_id']
            payment = Payment.objects.get(order_id = razorpay_order_id )
            payment.payment_id = razorpay_payment_id
            payment.status = True
            usercourse = UserCourse(
                user = payment.user,
                course = payment.course,

            )
            usercourse.save()
            payment.user_course = usercourse
            payment.save()

            context = {
                'data':data,
                'payment':payment,
            }
            return render (request,'verify_payment/success.html',context)
        except:
            return render(request,'verify_payment/fail.html')
        
def  contactdata(request):
     if request.method == "POST":
          na = request.POST.get('name')
          em = request.POST.get('email')
          mes = request.POST.get('message')
          obj = contactdb(NAME=na, EMAIL=em, MESSAGE=mes)
          obj.save()
          return redirect(CONTACT_US)
     
def reviewdata(request):
    if request.method == "POST":
        cr = request.POST.get('course')
        us = request.POST.get('user')
        ph = request.FILES['photo']
        re = request.POST.get('message')
        obj = reviewdb(selectcourse=cr,selectuser=us,Userphoto=ph,Review=re)
        obj.save()
        return redirect(ABOUT_US)
