#signals.py file is used as trigger to triger a model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Product_Rating
from django.db.models import Avg


@receiver(post_save,sender=Review)
def update_product_rating_on_save(sender,instance, **kwargs):
    product=instance.product
    review=product.reviews.all()
    total_review=review.count()
    averagerating=review.aggregate(Avg("rating"))["rating__avg"] or 0.0 #models.avg will return a dictionary with key "field_Avg"

    product_rating, created =Product_Rating.objects.get_or_create(product=product)
    product_rating.average_rating=averagerating
    product_rating.total_ratings=total_review
    product_rating.save()

    
@receiver(post_delete,sender=Review)
def update_product_rating_on_delete(sender,instance, **kwargs):
    product=instance.product
    review=product.reviews.all()
    total_review=review.count()
    averagerating=review.aggregate(Avg("rating"))["rating__avg"] or 0.0 #models.avg will return a dictionary with key "field_Avg"
    print(averagerating)
    product_rating, created =Product_Rating.objects.get_or_create(product=product)
    product_rating.average_rating=averagerating
    product_rating.total_ratings=total_review
    product_rating.save()
    