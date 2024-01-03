from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    name = fields.CharField(max_length=64)
    age = fields.IntField(max_length=3)
    city = fields.CharField(max_length=255)
    sex = fields.CharField(max_length=32)
    look_for = fields.CharField(max_length=32)
    bio = fields.CharField(max_length=255)
    photo = fields.TextField()

    class Meta:
        table = "users"

    def __str__(self) -> str:
        return self.name