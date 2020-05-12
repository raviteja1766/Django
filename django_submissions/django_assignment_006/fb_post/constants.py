from django.db import models

class ReactType(models.TextChoices):
    WOW = 'WOW'
    LIT = 'LIT'
    LOVE = 'LOVE'
    HAHA = 'HAHA'
    THUMBS_UP = 'THUMBS-UP'
    THUMBS_DOWN = 'THUMBS-DOWN'
    ANGRY = 'ANGRY'
    SAD = 'SAD'