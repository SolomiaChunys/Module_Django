from celery import shared_task
from shop.models import Return


@shared_task
def accept_all():
    returns = Return.objects.all()

    for return_obj in returns:
        order = return_obj.order

        product = order.product
        user = order.user

        product.count += order.count
        user.wallet += product.price * order.count

        product.save()
        user.save()

        return_obj.delete()
        order.delete()


@shared_task
def refuse_all():
    returns = Return.objects.all()
    for return_obj in returns:
        return_obj.delete()
