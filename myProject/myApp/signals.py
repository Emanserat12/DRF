from django.contrib.auth.models import User
from django.core.mail import send_mail

from myApp.models import Order, Products
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, pre_save

from myProject import settings

# custom signal
product_fetched = Signal()


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        remaining_product_inventory = instance.productId.inventory - instance.noOfItems
        update_inventory = Products.objects.filter(id=instance.productId.id). \
            update(inventory=remaining_product_inventory)
        if update_inventory:
            receiver_name = ' '.join(name.capitalize() for name in instance.userId.username.split('.'))
            subject = 'Order Confirmation'
            message = f'Dear {receiver_name},\n\n' \
                      f'Thank you for your order! Your order ID is {instance.orderId}.\n' \
                      'Your order has been confirmed and will be delivered within 3-4 working days.\n\n' \
                      f'Your Total Bill is {instance.totalBill} USD \n\n' \
                      'Thank you for shopping with us!'
            recipient_list = [instance.userId.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@receiver(product_fetched)
def check_product_inventory(sender, instance, **kwargs):
    for product in instance:
        if product.inventory < 5:
            print(f"Please restock the {product.name} inventory")
            user_queryset = User.objects.filter(is_active=True)
            user_ = [x for x in user_queryset if x.is_superuser]
            if user_:
                restock_product(instance=product)
                other_users = [x for x in user_queryset if not x.is_superuser]
                for user in other_users:
                    notify_users(sender=User, instance=product, user=user)


def restock_product(instance):
    instance.inventory += 10
    instance.save()
    print(f"{instance.name} has been restocked!")
    return instance.inventory


@receiver(pre_save, sender=User)
def notify_users(sender, instance, **kwargs):
    if instance.inventory >= 5:
        print(f"{instance.name} has been restocked!")
        receiver_name = ' '.join(name.capitalize() for name in kwargs.get('user').username.split('.'))
        subject = 'Product Restocked'
        message = f'Dear {receiver_name},\n\n' \
                  f'{instance.name} has been restocked.\n' \
                  'You can Go and grab your fav product Today.\n\n'
        recipient_list = [kwargs.get('user').email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

