from django.db import models
from django.contrib.auth.models import User

class UserC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=18)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name +" " + self.last_name

# Type
class Type(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to="pet_imgs/")

    def __str__(self):
        return self.name

# Breed
class Breed(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=300)
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

# Gender of pet
class Gender(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name

# Pet
class Pet(models.Model):
    name = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    birthday_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="pet_imgs/")
    comment = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

    def __delete__(self, instance):
        return self.breed

class PetsByUser(models.Model):
    user = models.ForeignKey(UserC, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + " added "+self.pet.name

# Image
class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="pet/images/")

    def __str__(self):
        return self.pet.name

# Cart
class Cart(models.Model):
    user =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " +str(self.id)

# Basket
class Basket(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "Basket: " + str(self.id)

