# DELETE Operation

## Step-by-Step (Interactive Django Shell)

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'library.Book': 1})

>>> Book.objects.all()
<QuerySet []>