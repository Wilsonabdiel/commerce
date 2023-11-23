from django.apps import AppConfig


class AuctionsConfig(AppConfig):
    name = 'auctions'
    # Added to resolve sign in bug I think
    default_auto_field = 'django.db.models.BigAutoField'

# apps.py

