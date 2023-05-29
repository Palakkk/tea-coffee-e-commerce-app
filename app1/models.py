from django.db import models

class Category(models.Model):
    categoryname = models.CharField(max_length=200)
    img=models.ImageField(upload_to='category')

    def __str__(self):
        return self.categoryname
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    img=models.ImageField(upload_to='product')
    price = models.IntegerField()
    description = models.TextField()
    quantity=models.IntegerField()


class UserRegister(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()



class Contactus(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    message=models.TextField()

class Feedback(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    feedback=models.TextField()

# orderModel = OrderModel()
#             orderModel.userId = request.session['shippingUserId']
#             orderModel.userName = request.session['shippingName']
#             orderModel.userEmail = request.session['shippingEmail']
#             orderModel.userContact = request.session['shippingContact']
#             orderModel.address = request.session['shippingAddress']
#             orderModel.orderAmount = request.session['shippingOrderAmount']
#             orderModel.paymentVia = request.session['shippingPaymentVia']
#             orderModel.paymentMethod = request.session['shippingPaymentMethod']
#             orderModel.transactionId = payment_id
#             orderModel.save()

class Ordermodel(models.Model):
    productid=models.CharField(max_length=200)
    productqty=models.CharField(max_length=200)
    userId = models.CharField(max_length=200)
    userName = models.CharField(max_length=200)
    userEmail = models.EmailField()
    userContact = models.IntegerField()
    address = models.CharField(max_length=200)
    orderAmount = models.IntegerField()
    paymentMethod = models.CharField(max_length=200)
    transactionId = models.CharField(max_length=200)
    orderDate = models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self):
        return self.userName

