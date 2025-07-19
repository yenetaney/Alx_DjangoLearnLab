# CREATE Operation

## Step-by-Step (Interactive Django Shell)

```python
>>> from library.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", published_year=1949)
>>> book
<Book: 1984>
