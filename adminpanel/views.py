from store.models import *
from register.models import *
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from register.forms import PersonForm
from django.contrib.auth.models import User
from store.forms import AuthorForm, BookForm
from register.forms import NewUserForm
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def adminDashPage(request):
    ut = User.objects.count()
    bt = Book.objects.count()
    books = Book.objects.filter(recommended=True).order_by('-id')
    context = {
        'user_total': ut,
        'book_total': bt,
        'books': books,
    }
    return render(request, 'admin-dashboard.html', context)

#USER
@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def adminUser(request):
    data = dict()
    allUser = Person.objects.all().order_by('-id')  
    query = request.GET.get('q', 0)
    if query:
        allUser = Person.objects.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(phone__icontains=query) | Q(user__email__icontains=query) | Q(user__username__icontains=query)
            ).order_by('-id')  
        data['query_'] = query
    
    data['users'] = allUser
    return render(request, 'user-list.html', data)

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def addUserPage(request):
    form = NewUserForm()
    if request.method == 'POST':
        try:
            if len(User.objects.filter(username=request.POST['username'])) == 0:
                POST = request.POST.copy()
                uform = NewUserForm(POST)                
                if uform.is_valid():
                    uform.save()
                    newUser = User.objects.get(username=uform.cleaned_data['username'])
                    if request.POST.get('role', '1') == '2':
                        newUser.is_staff = True
                        newUser.is_superuser = True
                        newUser.save()
                    POST['user'] = newUser.id
                    form = PersonForm(POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Muvaffaqiyatli Yararildi")
                    else:
                        print(form.errors)
                        print(uform.errors)
                        messages.warning(request, "Malumotlarni to'g'ri kiriting")
                else:
                    print(form.errors)
                    print(uform.errors)
                    messages.warning(request, "Malumotlarni to'g'ri kiriting")
            else:
                messages.warning(request, "Bunday username bazada mavjud")
        except Exception as e:
            print(e)
            messages.warning(request, "Xatolik yuz berdi")
            
    return render(request, 'add-user.html', {'form': form})


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def editUserPage(request, pk):
    try:
        rp = Person.objects.get(pk=pk)
        ru = User.objects.get(username=rp.user)
        if request.method == "POST":
            POST = request.POST.copy()
            if request.POST.get('role', '1') == '1':
                ru.is_staff = False
                ru.is_superuser = False
                ru.save()
            elif request.POST.get('role', '1') == '2':
                ru.is_staff = True
                ru.is_superuser = True
                ru.save()
                
            POST['user'] = ru.id
            form = PersonForm(POST, request.FILES, instance=rp)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                if not(ru.check_password(POST['password1'])) and POST['password1'] == POST['password2']:
                    ru.set_password(POST['password2'])
                    ru.save()
                if POST['username'] != ru.username:
                    ru.username = POST['username']
                    ru.save()
                messages.success(request, "Muvaffaqiyatli O'zgartirildi")
            else:
                print(form.errors)
                messages.warning(request, "Malumotlarni to'g'ri kiriting")
            return redirect('adminUser')
        
        return render(request, 'admin-edit-user.html', {'data_person': rp,'data_user': ru})
    except User.DoesNotExist:
        messages.warning(request, "User topilmadi")
        return redirect('adminUser')
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        return redirect('adminUser')


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def delUserPage(request, pk):
    try:
        r = Person.objects.get(pk=pk)
        ru = User.objects.get(username=r.user)
        r.delete()
        ru.delete()
        messages.success(request, "Muvaffaqiyatli o'chirildi")
    except Book.DoesNotExist:
        messages.warning(request, "Kitob topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        
    return redirect('adminUser')

#BOOK
@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def adminBookPage(request):
    allBook = Book.objects.all().order_by('-id')
    return render(request, 'admin-books.html', {'books': allBook})


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def addBookPage(request):
    form = BookForm()
    if request.method == 'POST':
        try:
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Muvaffaqiyatli Yararildi")
            else:
                print(form.has_error)
                messages.warning(request, "Malumotlarni to'g'ri kiriting")
        except Exception as e:
            print(e)
            messages.warning(request, "Xatolik yuz berdi")
            
    categorys = Category.objects.all().order_by('-id')
    authors = Author.objects.all().order_by('-id')
    return render(request, 'admin-add-book.html', {'form': form, 'categorys':categorys, 'authors':authors})

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def editBookPage(request, id):
    try:
        r = Book.objects.get(pk=id)
        if request.method == "POST":
            form = BookForm(request.POST, request.FILES, instance=r)
            if form.is_valid():
                form.save()
                messages.success(request, "Muvaffaqiyatli O'zgartirildi")
            else:
                messages.warning(request, "Malumotlarni to'g'ri kiriting")
            return redirect('adminBook')
        
        categorys = Category.objects.all().order_by('-id')
        authors = Author.objects.all().order_by('-id')
        return render(request, 'admin-edit-book.html', {'book': r, 'form':BookForm(), 'categorys':categorys, 'authors':authors})
    except Book.DoesNotExist:
        messages.warning(request, "Muallif topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        
@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def delBookPage(request, id):
    try:
        r = Book.objects.get(pk=id)
        r.delete()
        messages.success(request, "Muvaffaqiyatli o'chirildi")
    except Book.DoesNotExist:
        messages.warning(request, "Kitob topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        
    return redirect('adminBook')

#AUTHOR
@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def adminAuthorPage(request):
    allAuthor = Author.objects.all().order_by('-id')
    return render(request, 'admin-author.html', {'authors': allAuthor})

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def addAuthorPage(request):
    if request.method == 'POST':
        try:
            form = AuthorForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Muvaffaqiyatli Yararildi")
            else:
                print(form.has_error)
                messages.warning(request, "Malumotlarni to'g'ri kiriting")
        except Exception as e:
            print(e)
            messages.warning(request, "Xatolik yuz berdi")
    
    f = AuthorForm()    
    return render(request, 'admin-add-author.html', {'form_author': f})

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def editAuthorPage(request, id):
    try:
        r = Author.objects.get(pk=id)
        if request.method == "POST":
            form = AuthorForm(request.POST, request.FILES, instance=r)
            if form.is_valid():
                form.save()
                messages.success(request, "Muvaffaqiyatli O'zgartirildi")
            else:
                messages.warning(request, "Malumotlarni to'g'ri kiriting")
            return redirect('adminAuthor')
            
        return render(request, 'admin-edit-author.html', {'author': r, 'form':AuthorForm()})
    except Author.DoesNotExist:
        messages.warning(request, "Muallif topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def delAuthorPage(request, id):
    try:
        r = Author.objects.get(pk=id)
        r.delete()
        messages.success(request, "Muvaffaqiyatli o'chirildi")
    except Author.DoesNotExist:
        messages.warning(request, "Muallif topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        
    return redirect('adminAuthor')



#CATEGORY
@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def adminCatPage(request):
    allCategory = Category.objects.all().order_by('-id')
    return render(request, 'admin-category.html', {'categorys': allCategory})

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def addCatPage(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            description = request.POST['description']
            Category.objects.create(name=name, description=description)
            messages.success(request, "Muvaffaqiyatli Yararildi")
        except:
            messages.warning(request, "Xatolik yuz berdi")
    return render(request, 'admin-add-category.html')

@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def editCatPage(request, id):
    try:
        r = Category.objects.get(pk=id)
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            r.name = name
            r.description = description
            r.save()
            messages.success(request, "Muvaffaqiyatli O'zgartirildi")
            return redirect('adminCat')
            
        return render(request, 'admin-edit-category.html', {'category': r})
    except Category.DoesNotExist:
        messages.warning(request, "Kategoriya topilmadi")
        return redirect('adminCat')
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        return redirect('adminCat')


@permission_required('auth.view_user', login_url='/404/')
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def delCatPage(request, id):
    try:
        r = Category.objects.get(pk=id)
        r.delete()
        messages.success(request, "Muvaffaqiyatli o'chirildi")
    except Category.DoesNotExist:
        messages.warning(request, "Kategoriya topilmadi")
    except Exception as e:
        messages.warning(request, f"Xatolik yuz berdi: {str(e)}")
        
    return redirect('adminCat')

