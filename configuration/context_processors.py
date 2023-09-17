from configuration.models import Configuration

def configuration_hotel(request):
    # Obtenir le dernier objet Configuration en utilisant l'ordre par ID décroissant
    try:
        configuration = Configuration.objects.latest('id')
    except Configuration.DoesNotExist:
        configuration = None

    return {'configuration': configuration}
