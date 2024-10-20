from django.urls import path
from .views import (
    StoreListCreateView,
    StoreRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    SaleListCreateView,
    SaleRetrieveUpdateDestroyView,
)
from .views import (
    LoginView,
    LogoutView,
    DashboardView,
    get_zip_codes,
    get_cities,
    get_county_numbers,
    get_categories,
    get_vendor_numbers,
    get_item_numbers,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("stores/", StoreListCreateView.as_view(), name="store-list-create"),
    path(
        "stores/<int:pk>/",
        StoreRetrieveUpdateDestroyView.as_view(),
        name="store-detail",
    ),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-detail",
    ),
    path("sales/", SaleListCreateView.as_view(), name="sale-list-create"),
    path(
        "sales/<int:pk>/", SaleRetrieveUpdateDestroyView.as_view(), name="sale-detail"
    ),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("zipcodes/", get_zip_codes, name="get_zip_codes"),
    path("cities/", get_cities, name="get_cities"),
    path("county_numbers/", get_county_numbers, name="get_county_numbers"),
    path("categories/", get_categories, name="get_categories"),
    path("vendor_numbers/", get_vendor_numbers, name="get_vendor_numbers"),
    path("item_numbers/", get_item_numbers, name="get_item_numbers"),
]
