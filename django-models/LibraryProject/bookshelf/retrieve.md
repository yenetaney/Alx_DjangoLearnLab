# RETRIEVE Operation

## Step-by-Step (Interactive Django Shell)

```python
>>> from library.models import Book
>>> book1 = Book.objects.get(title="1984")
>>> book1.title
'1984'
>>> book1.author
'George Orwell'
>>> book1.published_year
1949