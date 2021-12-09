from search.models import Document


def run():
    print(len(Document.objects.all()))
