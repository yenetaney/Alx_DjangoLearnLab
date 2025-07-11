# UPDATE Operation

## Step-by-Step (Interactive Django Shell)

```python
>>> from library.models import Book
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> book.title
'Nineteen Eighty-Four'