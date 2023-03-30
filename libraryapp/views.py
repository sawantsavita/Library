from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Book

# Create your views here.

# function based views --------------------------------------------------------
@csrf_exempt
def welcome(request):
    # print(request.method)
    if request.method == 'POST':
        print("In welcome POST method", request.method)
        print(request.POST)                 # [20/Dec/2022 12:11:35] "POST /welcome/ HTTP/1.1" 200 7  # 200- Successful, 7 characters  
        bid = request.POST.get('book_id')                         
        name = request.POST.get('book_name')
        qty = request.POST.get('book_qty')
        price = request.POST.get('book_price')
        author = request.POST.get('book_author')
        is_published = request.POST.get('book_is_published')
        print(bid, name, qty, price, author, is_published)
        if is_published == "Yes":
            is_published = True
        else:
            is_published = False
        if name and qty and price and author and is_published:
            if not bid:           
                Book.objects.create(name = name, qty = qty, price = price, author = author, is_published = is_published)        
            else:
                book_obj = Book.objects.get(id = bid)
                book_obj.name = name
                book_obj.qty = qty
                book_obj.price = price
                book_obj.author = author
                book_obj.is_published = is_published
                book_obj.save()
        else:
            print("Please provide valid values for Book...")
        return redirect('home_page')
        # return HttpResponse("Success")           
    elif request.method == 'GET':   
        print("In welcome GET method",request.method)        
        print(request.GET)                  # [20/Dec/2022 12:11:13] "GET /welcome/ HTTP/1.1" 200 810
        return render(request, "home.html")     # context = {"all_books":Book.objects.all()})
        

@csrf_exempt    
def show_books(request):
    print("In show_books method", request.method)
    return render(request, "show_books.html", {"books":Book.objects.filter(is_active = True), "inactive": False })

@csrf_exempt
def update_book(request, id):
    # print(request.method)
    print("In update method", request.method)
    book_obj = Book.objects.get(id=id)
    return render(request, "home.html", context= {"single_book": book_obj})

@csrf_exempt
def harddelete_book(request, id):
    print("In delete method", request.method)
    Book.objects.get(id = id).delete()
    return redirect('active_books')

def softdelete_book(request, id):
    book_obj = Book.objects.get(id = id)
    book_obj.is_active = False
    book_obj.save()
    return redirect('active_books')

def show_inactive_books(request):
    return render(request, "show_books.html", {"books":Book.objects.filter(is_active = False), "inactive": True})

def restore_book(request, id):
    book_obj = Book.objects.get(id = id)
    book_obj.is_active = True
    book_obj.save()
    return redirect('active_books')

# django forms
from .forms import BookForm

def book_form(request):
    form = BookForm()
    print(form)
    return render(request, 'book_form.html', {"form": BookForm()})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    '''Creating pagination with 3 books in one page'''
    book_list = Book.objects.all()
    page = request.GET.get('page', 1)
    # print(page)
    paginator = Paginator(book_list, 3)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    # print(books)
    # print(books.start_index())
    # print(books.end_index())
    return render(request, 'index.html', { 'books': books })


# class based views--------------------------------------------------------------

from django.views.generic.edit import CreateView    
class BookCreate(CreateView):  
    model = Book    
    fields = '__all__'  
    success_url = "cbv-book-create"
    
'''
Retrieve View:
1. ListView - Display all books data (so no need of id)
2. DetailView - Display single book data ( so id is required)
'''  
# implementation of retrieve using ListView    
from django.views.generic import ListView
'''need to import ListView to display all book details'''

class BookRetrieve(ListView):
    model = Book
    # context_object_name = "all_books"     # we can change object_list as all_books ( used in book_list.html)
    # queryset = Book.objects.filter(is_active=True) # we can change our query. by default query is Book.objects.all()
    # queryset = Book.objects.filter(is_active=False) # we can change our query. by default query is Book.objects.all()
    
# implementation of retrieve using DetailView  -showing single book record  

from django.views.generic.detail import DetailView  
  
class BookDetail(DetailView):  
    model = Book 

# UpdateView
from django.views.generic.edit import UpdateView  

class BookUpdate(UpdateView):  # no need to create new html file for this view, using book_form.html
    model = Book
    
# DeleteView- This is hard delete
from django.views.generic.edit import DeleteView  
from django.urls import reverse_lazy
  
class BookDelete(DeleteView):  
    model = Book    
    # here we can specify the URL   
    # to redirect after successful deletion  
    # success_url = '/retrieve/' 
    success_url = reverse_lazy('BookRetrieve')  # showing error


# TemplateView
from django.views.generic import TemplateView
class BookTemplate(TemplateView):
    template_name = "home.html"
    # extra_context = {"name": "Akash"} # we can pass additional parameters to home.html
    




    