from Core.Model import Model
from Core.Model.Fields import IntegerField, TextField, DateTimeField


class User(Model):

    id = IntegerField(primary_key=True, auto_increment=True, null=False)
    username = TextField(unique=True, null=False)
    password = TextField(null=False)
    created_at = DateTimeField(auto_now_add=True)

    _table_name = "usuario"
