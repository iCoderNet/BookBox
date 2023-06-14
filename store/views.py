import os, requests
from .models import *
from register.models import *
from dotenv import load_dotenv
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

load_dotenv()

def send_message(msg):
    TOKEN = os.getenv("API_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=html"
    return requests.get(url).json()

@login_required
def BookInfo(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        catbook = Book.objects.filter(category=book.category).order_by('-id')[:9]
        return render(request, "book-page.html", {'book': book, 'catbook': catbook})
    except Book.DoesNotExist:
            return redirect('PNF404')
    except Exception as e:
        print(e)
        return redirect('PNF404')

@login_required
def bookDownload(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        response = HttpResponse(open(book.document.path, 'rb').read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + book.name + '.pdf"'
        return response
    except Book.DoesNotExist:
            return redirect('PNF404')
    except Exception as e:
        print(e)
        return redirect('PNF404')

@login_required
def bookRead(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        return render(request, "book-pdf.html", {'book': book})
    except Book.DoesNotExist:
            return redirect('PNF404')
    except Exception as e:
        return redirect('PNF404')

@login_required
def pageWishList(request):
    allWishlist = WishList.objects.all().order_by('-id')
    return render(request, "wishlist.html", {'wls': allWishlist})

@login_required
def addWishList(request, pk):
    if pk:
        try:
            book = Book.objects.get(pk=pk)
            found = WishList.objects.filter(user=request.user, book=book)
            data = {
                'ok': True,
                "detalist": {
                    'bookname': book.name,
                }
            }
            if len(found) > 0:
                found[0].delete()
                data['detalist']['add'] = False
                data['detalist']['status'] = "Yoqtirgan kitoblaringizdan olib tashlandi"
                return JsonResponse(data)
            else:
                WishList.objects.create(user=request.user, book=book)
                data['detalist']['add'] = True
                data['detalist']['status'] = "Yoqtirgan kitoblaringizga qo'shildi"
                return JsonResponse(data)
        except Book.DoesNotExist:
            return JsonResponse({'ok':False, 'error': 'Kitob Topilmadi'})
        except Exception as e:
            return JsonResponse({'ok':False, 'error': str(e)})
    else:
        return redirect('home')

@login_required
def homePage(request):
    recbooks = Book.objects.filter(recommended=True).order_by('-id')[:2]
    books = Book.objects.all().order_by('-id')[:8]
    wishlist = WishList.objects.all()
    wlt = []
    for i in wishlist:
        wlt.append(i.book.id)
    context = {
        'rbooks': recbooks,
        'books': books,
        'wishlist': wlt,
    }
    return render(request, 'index.html', context)



#Book Store
@login_required
@csrf_exempt
def pageSearch(request):
    recbook = Book.objects.filter(recommended=True).order_by('-id')[:9]
    data = {'recbook': recbook}
    if 'q' in request.GET:
        print("#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n#\n")
        try:
            query = request.GET['q']
            data['query'] = query
            books = Book.objects.filter(
                Q(name__icontains=query) | Q(author__name__icontains=query) | Q(description__icontains=query)
            )
        except Book.DoesNotExist:
            books = None
            
        data['books'] = books
    else:
        print("!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n")
        books = Book.objects.all().order_by('-id')
        data['books'] = books
        
    return render(request, 'category.html', data)

def contact(request):
    if request.method == 'POST':
        person = Person.objects.get(user=request.user.id)
        user = request.user
        application = request.POST['application']
        msg = request.POST['msg']
        res = send_message("💡 <b>{}\n\nUser: {}\nXabari:</b><i>{}</i>".format(application, user, msg))
        if res['ok']:
            messages.success(request, 'Xabaringiz adminlarga yuborildi')
        else:
            messages.error(request, res['error'])
    return render(request, 'contact.html')

def pfn404(request):
    return render(request, 'pages-error.html')

@login_required
def html_viewer(request, html):
    return render(request, html)


