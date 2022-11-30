from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path("", HomeView.as_view(), name = "home"),
    path("contact-us/", ContactView.as_view(), name = "contact"),
    path("types/",TypesView.as_view(), name = "types"),
    path("pet/<int:pk>/", PetDetailView.as_view(), name ="petdetail"),
    path("volunteer/", VolunteerView.as_view(), name = "volunteer"),
    path("basket-<int:pet_id>/",BasketView.as_view(), name = "basket"),
    path("my-basket/", MyBasketView.as_view(), name = "mybasket"),
    path("manage-basket/<int:b_id>/", ManageBasketView.as_view(), name="managebasket"),
    path("register/", UserRegistrationView.as_view(), name="userregistration"),
    path("login/", UserLoginView.as_view(), name = "userlogin"),
    path("logout/", UserLogoutView.as_view(), name = "userlogout"),
    path("home/<int:pk>/add/", PetCreateView.as_view(), name = "petcreate"),
    path("pets/<int:td>/", FilterView.as_view(), name = "filter" ),
    path("forgot-password/", PasswordForgotView.as_view(), name = "forgotpassword"),
    path("reset-password/<email>/<token>/", ResetPasswordView.as_view(), name = "resetpassword"),
    path("profile/<int:pk>/pets/", MyPetView.as_view(), name = "petsbyuser"),
    path("manage-pets/<int:p_pk>/", ManagePetView.as_view(), name = "managepet"),
    path("profile/<int:pk>", ProfileView.as_view(), name = "profile"),
    path("profile/edit/<int:pk>/", ProfileEditView.as_view(), name = "editprofile"),
    path("pet/edit/<int:pk>/", PetEditView.as_view(), name = "editpet"),

]