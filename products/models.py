from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.FileField(upload_to='product/',
                             max_length=500, blank=False, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, max_length=50, null=False, blank=False)
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_length=1,
        max_digits=5, decimal_places=0, blank=True, default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(null=True, blank=True, default=0)
    discount = models.IntegerField(default=0,)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_recommended_products():
        return Product.objects.order_by('-rating')[:9]

    def update_rating(self):
        reviews = self.review_set.all()
        total_rating = sum(review.rating for review in reviews)
        num_reviews = len(reviews)
        if num_reviews > 0:
            average_rating = total_rating / num_reviews
            self.rating = average_rating
            self.save()

    def update_price(self):
        discountPrice = self.price-(self.price/100*self.discount)
        if self.discount < 0:
            return self.price
        self.price = discountPrice
        self.save()

    class Meta:
        ordering = ['id']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    rating = models.DecimalField(
        max_digits=5, decimal_places=0, max_length=1, null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(
        max_length=13)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.IntegerField(
        null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # OrderItem'lar jamlanadigan totalPrice'ni hisoblash
    #     total_price = sum(item.price for item in self.orderitem_set.all())

    #     # totalPrice'ni yangilash
    #     self.totalPrice = total_price

    #     # Asosiy save metodni chaqirish
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self,  str(self.createdAt)}"

    class Meta:
        ordering = ['-createdAt']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(
        null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price and self.product:
            self.price = int(self.product.price) * int(self.qty)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.address)


class Feedback(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    message = models.CharField(max_length=500)
