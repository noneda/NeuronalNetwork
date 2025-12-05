## **Basic Example How Use**

```python
class User(Model):
    _table_name = "users"

    id = IntegerField(primary_key=True, auto_increment=True)
    name = TextField(max_length=100, null=False)
    email = TextField(max_length=255, unique=True, null=False)
    age = IntegerField(null=True)
    active = BooleanField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Post(Model):
    _table_name = "posts"

    id = IntegerField(primary_key=True, auto_increment=True)
    title = TextField(max_length=200, null=False)
    content = TextField()
    user_id = IntegerField(null=False)
    published = BooleanField(default=0)
    created_at = DateTimeField(auto_now_add=True)


if __name__ == "__main__":
    db = sqlite3.connect('app.db')

    User.setup_db(db)
    Post.setup_db(db)

    User.create_table()
    Post.create_table()

    user1 = User.create(name="Juan", email="juan@example.com", age=25)
    user2 = User.create(name="Maria", email="maria@example.com", age=30)
    user3 = User.create(name="Pedro", email="pedro@example.com", age=28)

    for user in User.all():
        print(user)

    older = User.filter(age__gt=26)
    for u in older:
        print(f"{u.name} ({u.age})")

    with_ar = User.filter(name__contains="ar")
    for u in with_ar:
        print(f"{u.name}")

    by_age = User.all().order_by('-age')
    for u in by_age:
        print(f"{u.name}: {u.age}")

    juan = User.get(name="Juan")
    print(f"Found: {juan}")

    juan.age = 26
    juan.save()
    print(f"Updated: {juan}")

    total = User.all().count()
    print(f"Total users: {total}")

    first_two = User.all().order_by('id')[:2]
    for u in first_two:
        print(f"{u.name}")

    Post.create(title="First post", content="Hello world", user_id=user1.id, published=True)
    Post.create(title="Second post", content="More content", user_id=user1.id)
    Post.create(title="Maria's post", content="Maria content", user_id=user2.id, published=True)

    published = Post.filter(published=True)
    for post in published:
        print(f"{post.title}")

    user3.delete()
    print(f"User deleted. Total now: {User.all().count()}")

    db.close()

```
