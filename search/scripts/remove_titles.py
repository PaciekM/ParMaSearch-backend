from search.models import Document


def run():
    Document.objects.all().delete()
