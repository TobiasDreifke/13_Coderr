from django.db import migrations
from django.contrib.auth.hashers import make_password


GUEST_USERS = [
    {
        "username": "andrey",
        "password": "asdasd",
        "type": "customer",
    },
    {
        "username": "kevin",
        "password": "asdasd24",
        "type": "business",
    },
]


def create_guest_users(apps, schema_editor):
    user_model = apps.get_model("auth", "User")
    profile_model = apps.get_model("user_auth_app", "UserProfile")

    for guest_user in GUEST_USERS:
        user, created = user_model.objects.get_or_create(
            username=guest_user["username"]
        )
        if created or not user.password:
            user.password = make_password(guest_user["password"])
            user.save(update_fields=["password"])

        profile_model.objects.get_or_create(
            username=user,
            defaults={"type": guest_user["type"]},
        )


def remove_guest_users(apps, schema_editor):
    user_model = apps.get_model("auth", "User")
    usernames = [guest_user["username"] for guest_user in GUEST_USERS]
    user_model.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user_auth_app", "0006_alter_userprofile_description_and_more"),
    ]

    operations = [
        migrations.RunPython(create_guest_users, remove_guest_users),
    ]
