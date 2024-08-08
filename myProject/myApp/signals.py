from django.core.mail import send_mail

from myApp.models import Order, Products
from django.dispatch import receiver
from django.db.models.signals import post_save

from myProject import settings


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        remaining_product_inventory = instance.productId.inventory - instance.noOfItems
        update_inventory = Products.objects.filter(id=instance.productId.id).\
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
