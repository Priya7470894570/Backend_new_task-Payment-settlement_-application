from django.db import models
class new_payment(models.Model):
    sender_id= models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=255)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.sender_id)  
    
class Settlement(models.Model):
    payment_ids = models.ManyToManyField('new_payment')
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.payment_ids)
    

