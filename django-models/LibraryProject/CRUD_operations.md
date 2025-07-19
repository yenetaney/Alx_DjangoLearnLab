# Django Shell - CRUD Operations

## 🟩 CREATE
```python
>>> from library.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", published_year=1949)
>>> book
<Book: 1984>

>>> book = Book.objects.get(title="1984")
>>> book.title
'1984'
>>> book.author
'George Orwell'
>>> book.published_year
1949

>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> book.title
'Nineteen Eighty-Four'


>>> book.delete()
(1, {'library.Book': 1})
>>> Book.objects.all()
<QuerySet []>

