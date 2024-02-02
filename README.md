<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

URLS FOR ACCOUNTS

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

1: http://127.0.0.1:8000/accounts/login/.

> request - POST.
> required-fiedls. email, password.

2: http://127.0.0.1:8000/accounts/register/.

> request - POST.
> required-fiedls. email, first_name, last_name, phone_number, password, password2

3: http://127.0.0.1:8000/accounts/profile/.

> permissions = IsAuthenticated

> request - GET.
> required-fiedls. none.

4: http://127.0.0.1:8000/accounts/profile-update/.

> request - PUT.
> required-fiedls. first_name, last_name, email, phone_number.

5: http://127.0.0.1:8000/accounts/send-otp/.

> permissions = IsAuthenticated

> email and user confirm for reset password
> request - POST.
> required-fiedls. email.

6: http://127.0.0.1:8000/accounts/reset-password/.

> permissions = IsAuthenticated

> request - POST.
> required-fiedls. email, otp_code, new_password, new_password2.

7: http://127.0.0.1:8000/accounts/token-refresh/.

> permissions = IsAuthenticated

> request - POST.
> required-fiedls. refresh

8: http://127.0.0.1:8000/accounts/logout/.

> permissions = IsAuthenticated

> request - POST.
> required-fiedls. refresh_token

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

URLS FOR PRODUCTS

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

9: http://127.0.0.1:8000/api/v1/products/

> permissions = AllowAny

> request - GET.
> required-fiedls. none

10: http://127.0.0.1:8000/api/v1/products/pk/

> permissions = AllowAny

> request - GET.
> required-fiedls. none

11: http://127.0.0.1:8000/api/v1/products/pk/create_review/

> permissions = IsAuthenticated

> request - POST.
> required-fiedls. name, product, rating, comment,

12: http://127.0.0.1:8000/api/v1/products/recommended/

> permissions = AllowAny

> request - GET.
> required-fiedls. none

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

> URLS FOR CATEGORIES

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

13: http://127.0.0.1:8000/api/v1/categories/

> permissions = AllowAny

> request - GET.
> required-fiedls. none

14: http://127.0.0.1:8000/api/v1/categories/pk/

> permissions = AllowAny

> request - DELETE.
> required-fiedls. none

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

> URLS FOR ORDERS

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

15: http://127.0.0.1:8000/api/v1/orders/

> permissions = IsOwner

> request - GET.
> required-fiedls. none

16: http://127.0.0.1:8000/api/v1/orders/pk/

> permissions = IsOwner

> request - GET.
> required-fiedls. none

17: http://127.0.0.1:8000/api/v1/orders/

> permissions = IsOwner

> request - POST.
> required-fiedls. orderItems = [{product,qty}], paymentMethod, shippingAddress ={address,city,postalCode}

18: http://127.0.0.1:8000/api/v1/orders/pk/

> permissions = IsOwner

> request - DELETE.
> required-fiedls.

19: http://127.0.0.1:8000/api/v1/orders/1/mark_as_paid/

> permissions = IsOwner

> request - PATCH.
> required-fiedls. none

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

> URLS FOR ADMINS

<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>

20: http://127.0.0.1:8000/accounts/users/.

> permissions = IsAdmin

> request - GET.
> required-fiedls. none

21: http://127.0.0.1:8000/accounts/users_staff/.

> permissions = IsAdmin

> request - GET.
> required-fiedls. none

22: http://127.0.0.1:8000/api/v1/products/

> permissions = IsAdmin

> request - POST.
> required-fiedls. name, image, category, description, price, countInStock.

23: http://127.0.0.1:8000/api/v1/products/pk/

> permissions = IsAdmin

> request - DELETE.
> required-fiedls. none

24: http://127.0.0.1:8000/api/v1/categories/

> permissions = IsAdmin

> request - POST.
> required-fiedls. name, image, category, description, price, countInStock.

25: http://127.0.0.1:8000/api/v1/categories/pk/

> permissions = IsAdmin

> request - DELETE.
> required-fiedls. none

26: http://127.0.0.1:8000/api/v1/orders/1/mark_as_delivered/

> permissions = IsAdmin

> request - PATCH.
> required-fiedls. none
