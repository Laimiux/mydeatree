from django.db.models.signals import pre_delete

from favorites.models import FavoriteItem

def remove_favorite_items(sender, instance, using, **kwargs):
    """
    Removes all the favorite items when the instance is deleted
    """
    FavoriteItem.objects.filter(content_object=instance).delete()
    
def remove_favorite_items(instance):
    """
    Removes all the favorite items when the instance is deleted
    """
    FavoriteItem.objects.filter(object_id=instance.pk ).delete()