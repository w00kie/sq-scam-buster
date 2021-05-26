from django.db import models
from django.contrib import admin
from django.utils.html import format_html


def shorten(public_key: str) -> str:
    return f"{public_key[:5]}...{public_key[-5:]}"


class StellarAccount(models.Model):
    public_key = models.CharField(primary_key=True, max_length=56)
    has_sq_badges = models.BooleanField(default=False)
    badges = models.JSONField(default=list)
    suspect = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    nickname = models.CharField(max_length=64, blank=True)
    directory_name = models.CharField(max_length=64, blank=True)
    directory_tags = models.JSONField(default=list)

    def __str__(self) -> str:
        if self.directory_name:
            return f"[{self.directory_name}] {shorten(self.public_key)}"
        else:
            return shorten(self.public_key)

    @admin.display(description="Account ID")
    def account_id_identicon(self):
        return format_html(
            '<img src="https://id.lobstr.co/{}.png" class="identicon"> {}',
            self.public_key,
            self,
        )

    def account_id_identicon_link(self):
        return format_html(
            """
            <a href='https://stellar.expert/explorer/public/account/{}'>
            <img src='https://id.lobstr.co/{}.png' class='identicon'> {}</a>
            """,
            self.public_key,
            self.public_key,
            self,
        )

    def sorted_badges(self):
        return sorted(self.badges)


class Payment(models.Model):
    transaction_hash = models.CharField(max_length=64)
    from_account = models.ForeignKey(to=StellarAccount, on_delete=models.CASCADE, related_name="issued_payments")
    to_account = models.ForeignKey(to=StellarAccount, on_delete=models.CASCADE, related_name="received_payments")
    amount = models.CharField(max_length=120, help_text="Decimal amount including Asset Code")
    memo = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.from_account} ▶︎ {self.to_account} {self.amount}"

    @admin.display(description="From Account ID")
    def from_account_id_identicon(self):
        return format_html(
            '<img src="https://id.lobstr.co/{}.png" class="identicon"> {}',
            self.from_account.public_key,
            self.from_account,
        )

    @admin.display(description="To Account ID")
    def to_account_id_identicon(self):
        return format_html(
            '<img src="https://id.lobstr.co/{}.png" class="identicon"> {}',
            self.to_account.public_key,
            self.to_account,
        )


class Badge(models.Model):
    asset_code = models.CharField(max_length=6)
    asset_issuer = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.asset_code
