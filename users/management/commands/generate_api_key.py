from django.core.management.base import BaseCommand
from rest_framework_api_key.models import APIKey


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-n",
            "--client_app_name",
            type=str,
            required=True,
            help="The name of the remote client application",
        )

    def handle(self, *args, **kwargs):
        client_app_name = kwargs["client_app_name"]

        current_key = APIKey.objects.filter(name=client_app_name)

        if current_key.exists():
            current_key.delete()

        _, api_key = APIKey.objects.create_key(name=client_app_name)

        with open("api_key.txt", "w") as f:
            f.write(f"{client_app_name} {api_key}")

        output = f"API_KEY={api_key}"
        return output
