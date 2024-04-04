from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from watchapp.models import Sch
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from watchapp.models import Product,Cart,Order
from django.db.models import Q
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages



def stud(request):
    print("request is:",request.method)
    if request.method=="GET":
       return render(request,'stud.html')
    else:
        n=request.POST['sname']
        r=request.POST['rnum']
        s=request.POST['div']
        c=request.POST['class']
        g=request.POST['gen']
       # print("name is",n)
       #print("email address is",m)
        p=Sch.objects.create(name=n,rollno=r,div=s,cl=c,gender=g)
        p.save 
        return redirect('/dashboard')
def dashboard(request):
    p=Sch.objects.all()
    print(p)
    context={}
    context['info']=p
    return render(request,'dashboard.html',context)
def delete(request,rid):
    print("Id to be deleted is:",rid)
    m=Sch.objects.filter(id=rid)
    print(m)
    m.delete()
    return redirect('/dashboard')
def edit(request,rid):
    if request.method=='GET':
        m=Sch.objects.filter(id=rid)
        print(m)
        context={}
        context['info']=m
        return render(request,'edit.html',context)
    else:
        fn=request.POST['sname']
        b=request.POST['rnum']
        sd=request.POST['div']
        cd=request.POST['class']
        gd=request.POST['gen']
        print(fn)
        m=Sch.objects.filter(id=rid)
        m.update(name=fn,rollno=b,div=sd,cl=cd,gender=gd)
        return redirect('/dashboard')
def home(request):
    #userid=request.user.id
    #print(userid)
    #print("result:",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['product']=p
    
    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['product']=p
    return render(request,'index.html',context)
def sort(request,ap):
    if ap=='0':
        col='price'
    else:
       col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    print(p)
    context={}
    context['product']=p
    return render(request,'index.html',context)
def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    #print(min)
    #print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['product']=p
    return render(request,'index.html',context)
    #return HttpResponse('values fetch')

def product_details(request,pid):
    context={}
    context['product']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def cart(request):
    return redirect('/cart')
def placeorder(request):
    return render(request,'placeorder.html')
def index_online(request):
    return render(request,'index_online.html')
def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upassword']
        cpass=request.POST['upass']
        if uname=="" or upass=="" or cpass=="":
            context['errormsg']="field cannot be empty"
            return render(request,'register.html',context)
        elif upass !=cpass:
              context['errormsg']="password and confirm password did not match"
              return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname,password=upass, email=uname)
                u.set_password(cpass)
                u.save()
                context['success']="user created successfully please login"
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="Username already exist"
                return render(request,'register.html',context)
                
            
    else:
        return render(request,'register.html')
def user_login(request):
    context={}
    if request.method=='POST':
        uname=request.POST['username']
        upass=request.POST['upass']
        if uname=="" or upass=="":
           context['errormsg']="field cannot be empty"
           return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']="Invalid username and password"
                return render(request,'login.html',context)
               # print(u.password)
               # return HttpResponse("data is fetch")
   
    else:
        return render(request,"login.html")
def user_logout(request):
    logout(request)
    return redirect('/home')
def addtocart(request,pid):
    if request.user.is_authenticated:
        
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u[0])
        p=Product.objects.filter(id=pid)
        print(p[0])
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        #print(userid)
        #print(pid)
        return redirect("/viewcart")
    else:
        return redirect('/user_login')
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')
def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    context={}
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
        context['product']=c
        context['total']=s
        context['n']=np
    return render(request,'cart.html',context)  
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    return redirect('/viewcart')
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print( "order id",oid)
    for x  in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    context={}
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
        context={}
        context['product']=c
        context['total']=s
        context['n']=np
    return render(request,'placeorder.html',context) 
    #return render(request,"placeorder.html")
def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0

    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_zyMr545mMqCvJ5", "xbRsMvRRs6hIXrvD7HW2Huai"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    
    return render(request,'pay.html',context)

def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        new_password = request.POST.get('upassword')
        confirm_password = request.POST.get('upass')

        user = User.objects.filter(username=username).first()

        if user:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                # Update the session to avoid automatic logout
                update_session_auth_hash(request, user)

                messages.success(request, 'Password reset successfully!')
                return redirect('/user_login')  # Redirect to login page after successful password reset
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'User not found.')
    return render(request, 'forget.html')

    
    

    
    
 