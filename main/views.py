from django.shortcuts import render , redirect
from django.views.generic import TemplateView
from django.views.generic import View, CreateView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from .utils import password_reset_token
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pets = Pet.objects.all().order_by("-id")
        paginator = Paginator(all_pets,8)
        page_number = self.request.GET.get('page')
        pet_list = paginator.get_page(page_number)
        context['types'] = Type.objects.all()
        context['pet_list'] = pet_list
        return context

class ContactView(TemplateView):
    template_name = "contactus.html"

class TypesView(TemplateView):
    template_name = "types.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context

class PetDetailView(TemplateView):
    template_name = "petdetail.html"
    success_url = reverse_lazy('/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_pk = kwargs['pk']
        pet = Pet.objects.get(pk = url_pk)
        pet_by_u = PetsByUser.objects.get(pet = pet)
        phone =pet_by_u.user.phone
        email = pet_by_u.user.email
        # pet.view_count += 1
        # pet.save()
        context['pet'] = pet
        context['phone'] = phone
        context['email'] =email
        born = pet.birthday_date
        today = date.today()
        age = (today- born)
        year = today.year - born.year
        month = today.month - born.month
        if today.month<born.month:
            month = 12 + int(today.month)-int(born.month)
        day = today.day-born.day
        if today.day < born.day:
            day = 30 - int(day)
        context['age_year'] = year
        context['age_m'] = month
        context['age_day'] = day
        return context

class ProfileView(TemplateView):
    template_name = 'profile.html'

class ProfileEditView(TemplateView):
    template_name = 'editprofile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs['pk']
        u_r = User.objects.get(pk =pk)
        if self.request.method == "GET":
            u_name = self.request.GET.get('username')
            e_mail = self.request.GET.get('email')
            p_word = self.request.GET.get('password')

            if u_name == None or u_name== '':
                u_name = u_r.username
            if e_mail== None or e_mail == '':
                e_mail = u_r.email
            if p_word != None and p_word != '':
                u_r.set_password(p_word)
            # u_r.set_password(password)
            u_r.email = e_mail
            #
            print("pass woooooord" ,u_r.password)
            u_r.username = u_name
            u_r.save()
            return context

class PetEditView(TemplateView):
    template_name = 'editpet.html'
    success_url = reverse_lazy('main:editpet')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_pk = kwargs['pk']
        edit_pet = Pet.objects.get(pk =p_pk )
        context['edit_pet'] = edit_pet
        cities = City.objects.all()
        context['cities'] =cities
        if self.request.method == "GET":
            p_price = self.request.GET.get('price')
            p_city = self.request.GET.get('city')
            p_comment = self.request.GET.get('comment')

            if p_price is None or p_price == '':
                p_price = edit_pet.price
            if p_city is None or p_city == '' or  p_city == '-':
                p_city = edit_pet.city
            if p_comment is None or p_comment == '' or p_comment == edit_pet.comment:
                p_comment = edit_pet.comment
            edit_pet.price = p_price
            edit_pet.city = City.objects.get(name = p_city)
            edit_pet.comment = p_comment
            edit_pet.save()
            return context

class FilterView(TemplateView):
    template_name = 'filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_id = kwargs['td']
        type= Type.objects.get(pk = url_id)
        context['type'] = type
        pets = type.pet_set.all()
        all_breed = Breed.objects.filter(type = type)
        all_gender = Gender.objects.all()
        all_city = City.objects.all()
        context['breed'] = all_breed
        context['gender'] = all_gender
        context['city'] = all_city

        if self.request.method =="GET":
            min_p = self.request.GET.get('minprice')
            max_p = self.request.GET.get('maxprice')
            db_f = self.request.GET.get('db_f')
            db_t = self.request.GET.get('db_t')

            breeds_list =[]
            genders_list =[]
            cities_list = []
            if min_p == None or min_p=='':
                min_p = 0
            if max_p == None or max_p=='':
                max_p = 1000000000
            if db_t == None or db_t == '':
                db_t = date.today()
            if db_f == None or db_f == '':
                db_f = date(1900,1,1)
            pets = type.pet_set.filter(price__range=(min_p, max_p), birthday_date__range=(db_f, db_t) )

            for breed in all_breed:
                br = self.request.GET.get(breed.name)
                if br != None and br != '':
                    breeds_list.append(breed)
            if len(breeds_list)==0:
                breeds_list= all_breed
            pets = pets.filter(breed_id__in=breeds_list)

            for gender in all_gender:
                gen = self.request.GET.get(gender.name)
                if gen != None and gen != '':
                    genders_list.append(gender)
            if len(genders_list)==0:
                genders_list= all_gender
            pets = pets.filter(gender_id__in=genders_list)

            for city in all_city:
                c = self.request.GET.get(city.name)
                if c != None and c != '':
                    cities_list.append(city)
            if len(cities_list)==0:
                cities_list= all_city
            pets = pets.filter(city_id__in=cities_list)

        paginator = Paginator(pets, 4)
        page_number = self.request.GET.get('page')
        pet_list = paginator.get_page(page_number)
        context['pet_list'] = pet_list
        return context

class VolunteerView(TemplateView):
    template_name = "volunteer.html"

class BasketView(TemplateView):
    template_name = "basket.html"

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pet_id = self.kwargs['pet_id']
        pet_object = Pet.objects.get(id=pet_id)
        context['pet_list'] = pet_object
        cart_id = self.request.session.get("cart_id", None)

        if cart_id:
            cart_object = Cart.objects.get(id = cart_id)
            this_pet_in_cart = cart_object.basket_set.filter(pet = pet_object)

            if this_pet_in_cart.exists():
               basket = this_pet_in_cart.last()
               basket.quantity += 1
               basket.subtotal = pet_object.price
               basket.save()
               cart_object.save()
            else:
                basket  = Basket.objects.create(cart=cart_object, pet = pet_object,
                                                quantity=1, subtotal=pet_object.price)
                cart_object.save()
        else :
            cart_object = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_object.id
            basket = Basket.objects.create(cart=cart_object, pet=pet_object, quantity=1, subtotal=pet_object.price)
            cart_object.save()
        return context

class MyBasketView(TemplateView):
    template_name = "mybasket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_id = self.request.session.get("cart_id",None)
        if card_id:
            cart = Cart.objects.get(id = card_id)
        else:
            cart =None
        context['cart'] = cart
        return context

class ManageBasketView(View):
    def get(self, request, *args, **kwargs):
        b_id = self.kwargs["b_id"]
        action = request.GET.get("action")
        b_object = Basket.objects.get(id = b_id)

        if action =="rmv":
            b_object.delete()
        else:
            pass

        return redirect("main:mybasket")

class UserRegistrationView(CreateView):
    template_name = "userregistration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = "userlogin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        user_name = form.cleaned_data.get("username")
        pass_word = form.cleaned_data["password"]
        user_l = authenticate(username = user_name , password = pass_word )

        if user_l is not None and UserC.objects.filter(user=user_l).exists():
            login(self.request, user_l)
        else :
            return render(self.request, self.template_name,
                          {"form": self.form_class, "error": " Введен неверный логин или пароль"})

        return super().form_valid(form)

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("main:home")

class PetCreateView(CreateView):
    template_name = "petcreate.html"
    form_class = PetForm
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        p = form.save()
        user_pk = self.kwargs["pk"]
        user = UserC.objects.get(pk=user_pk)
        PetsByUser.objects.create(user=user, pet=p)
        images = self.request.FILES.getlist("more_images")
        for i in images:
            PetImage.objects.create(pet = p, image = i)
        return super().form_valid(form)

class PasswordForgotView(FormView):
    template_name = 'forgotpassword.html'
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        url = self.request.META['HTTP_HOST']
        userc = UserC.objects.get(user__email=email)
        user = userc.user
        # send mail to the user with email
        text_content = 'Пожалуйста, перейдите по ссылке, чтобы сбросить свой пароль. Ссылка: '
        html_content = "http://"+url + "/reset-password/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            "Password Reset Link | Django Pet Store",
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        return super().form_valid(form)

class ResetPasswordView(FormView):
    template_name = "resetpassword.html"
    form_class = ResetPasswordForm
    success_url ='/login/'

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        update_session_auth_hash(self.request, user)

        return super().form_valid(form)

class MyPetView(TemplateView):
    template_name = "petsbyuser.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        pets = PetsByUser.objects.all()
        pet = []
        for p in pets:
            if p.user.pk == pk:
                pet.append(p)
        context['pets'] = pet
        return context

class ManagePetView(View):
    def get(self, request, *args, **kwargs):
        p_pk = self.kwargs["p_pk"]
        pp = PetsByUser.objects.get(pet__pk = p_pk)
        user = pp.user
        action = request.GET.get("action")
        if action =="rmv":
            Pet.objects.get(pk = p_pk).delete()
        else:
            pass

        return redirect(reverse('main:petsbyuser', kwargs ={'pk' : user.pk}))