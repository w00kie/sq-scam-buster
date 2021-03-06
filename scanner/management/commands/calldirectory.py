from tqdm import tqdm
from time import sleep
from typing import Any, Optional
import requests
from django.db.models import Count
from django.core.management.base import BaseCommand

from scanner.models import StellarAccount

# from pprint import pprint


class Command(BaseCommand):
    help = "Calls the stellar.expert directory for accounts with many received payments."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        big_payees = StellarAccount.objects.annotate(num_received=Count("received_payments")).filter(
            num_received__gte=10
        )

        progress_bar = tqdm(desc="Processing", total=big_payees.count())

        for account in big_payees:
            try:
                resp = requests.get(f"https://api.stellar.expert/explorer/directory/{account.public_key}")
                resp.raise_for_status()
                data = resp.json()
                account.directory_name = data.get("name", "")
                account.directory_tags = data.get("tags", [])
                account.save()
                sleep(1)
            except requests.exceptions.HTTPError:
                pass
            except Exception as e:
                tqdm.write(self.style.ERROR(f"Hit an error: {e}"))
                pass
            progress_bar.update(1)
