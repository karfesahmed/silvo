from django.shortcuts import render
from .serializers import *
from .models import *
from django.urls import reverse
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import requests
from django.contrib import messages

# Create your views here.
def add_wilaya_json(request):
    context = {}
    if request.method == 'POST':
        raw_data = request.POST.get('json_data')
        try:
            data = json.loads(raw_data)
            for item in data:
                WilayaInfo.objects.create(
                    IDWilaya = item.get('IDWilaya'),
                    name = item.get('name'),
                    delivery_home = item.get('delivery_home'),
                    delivery_office = item.get('delivery_office')
                )
            context['success'] = True
        except Exception as e:
            context['error'] = f"حدث خطأ: {e}"
    return render(request, 'pages/add_wilaya_json.html', context)


# normal users
def store(request):
    return render(request,"pages/store.html")

def product_page(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST["quantity"])
        price = product.price

        Client = request.POST["client"]
        MobileA = request.POST["phone"]
        Adresse = request.POST["adresse"]
        IDWilaya = int(request.POST["idWilaya"].split(",")[0])

        wilaya = WilayaInfo.objects.get(IDWilaya=IDWilaya)

        Total = (price*quantity) + wilaya.delivery_home
        size_or_color = request.POST["size_or_color"].split(",")[0]
        TProduit = f"{product.name} ({size_or_color})"
        order = Order(Client=Client,MobileA=MobileA,Adresse=Adresse,IDWilaya=IDWilaya,Total=Total,TProduit=TProduit,quantity=quantity)
        order.save()


        return HttpResponseRedirect(reverse("thankyou"))
    
    images = product.imgs.all()
    others = product.size_or_color.all()
    is_others = others.exists()
    
    return render(request,"pages/productpage.html",{
        "product":product,
        "images": images,
        "is_others":is_others,
        "others":others
    })

def say_thankyou(request):
    return render(request,"pages/thankyou.html")

def about_us(request):
    return render(request,"pages/aboutus.html")


# admin user

def add_product(request):
    if request.method == 'POST':

        name = request.POST["name"]
        description = request.POST["description"]
        price = int(request.POST["price"])

        
        product = Product(name=name, description=description, price=price)
        product.save()

        
        option_titles = request.POST.getlist("option_title[]")
        option_prices = request.POST.getlist("option_price[]")

        
        for title, price in zip(option_titles, option_prices):
            if title.strip():
                other = Other(
                    title=title.strip(),
                    price=price.strip() if price else None,
                    product=product
                )
                other.save()

        
        images = request.FILES.getlist('images')
        for image in images:
            img = ProductImage(product=product, image=image)
            img.save()

        
        return HttpResponseRedirect(reverse('store'))

    return render(request,"pages/add.html")

def orders(request):
    return render(request,"pages/orders.html")

def all_product(request):
    products = Product.objects.all()
    
    return render(request,"pages/allproduct.html", {'products': products})
def edit_product(request,product_id):
    product = Product.objects.get(pk=int(product_id))
    if request.method == 'POST':
        # تحديث بيانات المنتج
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.save()

        # حذف الصور المحددة
        delete_ids = request.POST.getlist('delete_image_ids')
        for img_id in delete_ids:
            try:
                img = ProductImage.objects.get(id=img_id, product=product)
                img.image.delete()  # حذف من media
                img.delete()
            except ProductImage.DoesNotExist:
                pass

        # حذف الخيارات القديمة وإنشاء جديدة
        product.size_or_color.all().delete()
        titles = request.POST.getlist('option_title[]')
        prices = request.POST.getlist('option_price[]')
        for title, price in zip(titles, prices):
            if title.strip():
                Other.objects.create(product=product, title=title.strip(), price=price or None)

        # رفع صور جديدة
        new_images = request.FILES.getlist('images')
        for img in new_images:
            ProductImage.objects.create(product=product, image=img)

        return HttpResponseRedirect(reverse("allproduct"))  # أو أي صفحة أخرى
    return render(request,"pages/edit.html", {'product': product})

def zrorders(request):
    trackings = Order.objects.filter(Confrimee="1").values_list("Tracking",flat=True)
    trk = []
    for t in trackings:
        trk.append({"Tracking" : f"{t}"})
    data = {
        "Colis" : trk
    }
    headers = {
        "token": "9d553c294e4ced5255c30b6c3289b467e7b8855c30a7770fb6cac2f233b276b1",  
        "key": "ee43069e18a64b6e926761281aca302e",  
        "Content-Type": "application/json"
    }
    url = "https://procolis.com/api_v1/lire"
    response = requests.post(url,json=data,headers=headers)
    return JsonResponse(response.json(),safe=False)

def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("store"))
    
    if request.method == 'POST':
        sub = request.POST["sub"]
        if sub == "send":
            try:
                order = Order.objects.get(pk=int(request.POST["order_id"]))
                order.Confrimee = "1"
                order.save()
                data = {
                     "Colis" : [{
                        "Tracking" : order.Tracking, 
                        "TypeLivraison" : order.TypeLivraison, # Domicile : 0 & Stopdesk : 1
                        "TypeColis" : order.TypeColis, # Echange : 1 
                        "Confrimee" : "", # 1 pour les colis Confirmer directement en pret a expedier 
                        "Client" : order.Client,
                        "MobileA" : order.MobileA,
                        "MobileB" : order.MobileA,
                        "Adresse" : order.Adresse,
                        "IDWilaya" : order.IDWilaya,
                        "Commune" : "",
                        "Total" : order.Total,
                        "Note" : order.Note,
                        "TProduit" :  order.TProduit,
                        "id_Externe" : order.id ,  # Votre ID ou Tracking 
                        "Source" : "" 
                     }]
                    
                }
                headers = {
                    "token": "9d553c294e4ced5255c30b6c3289b467e7b8855c30a7770fb6cac2f233b276b1",  
                    "key": "ee43069e18a64b6e926761281aca302e",  
                    "Content-Type": "application/json"
                }
                url = "https://procolis.com/api_v1/add_colis"
                response = requests.post(url,json=data,headers=headers)
                
                if response.status_code == 200:
                    messages.success(request, "✅ تم إرسال الطلب الى شركة الشحن بنجاح!")
                else:
                    messages.error(request, "❌ حدث خطأ أثناء الحفظ، الرجاء المحاولة لاحقاً.")

                return HttpResponseRedirect(reverse('dashboard'))
            except Order.DoesNotExist:
                return HttpResponse("thos order Does Not Exist" ,status=404)

        else :
            selected = int(sub)
                
            
            typeLivr = request.POST["typeLivr"]
            note = request.POST["note"]
            status = request.POST["status"]
            new_quantity = int(request.POST["new_quantity"])
            new_price = request.POST["new_price"]

            try :
                order = Order.objects.get(pk=selected)
                order.TypeLivraison = typeLivr
                order.Note = note
                order.conferme = status
                order.quantity = new_quantity
                order.Total = new_price
                order.save()
                return HttpResponseRedirect(reverse("dashboard"))
            except Order.DoesNotExist:
                return HttpResponse("thos order Does Not Exist" ,status=404)


    return render(request,"pages/dashboard.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('store'))
            
    return render(request,"pages/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('store'))


# Rest API's
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return JsonResponse(serializer.data,safe=False)


def product_detail(request,product_id):

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)

    return JsonResponse(serializer.errors, status=400)



def order_list(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            orders = Order.objects.all()
            serializer = OrderSerializer(orders,many=True)
            return JsonResponse(serializer.data,safe=False)
    return JsonResponse({"Access Denied":"You do not have permission to access this page"})


def wilaya(request):
    if request.method == 'GET':
        wilayas = WilayaInfo.objects.all()
        serializer = WilayaInfoSerializer(wilayas,many=True)
        return JsonResponse(serializer.data,safe=False)

def get_wilaya(request,IDWilaya):
    if request.method == 'GET':
        wilaya = WilayaInfo.objects.get(pk = int(IDWilaya))
        serializer = WilayaInfoSerializer(wilaya)
        return JsonResponse(serializer.data,safe=False)
