from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import Store, Product, Sale
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    StoreSerializer,
    ProductSerializer,
    SaleSerializer,
    UserLoginSerializer,
)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()  # In case you are using token authentication
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


from django.db.models import Sum, F


class DashboardView(APIView):
    def get(self, request):
        # Get filter parameters from the request
        store_name = request.GET.get("store_name")
        city = request.GET.get("city")
        zip_code = request.GET.get("zip_code")
        county_number = request.GET.get("county_number")
        category = request.GET.get("category")
        vendor_number = request.GET.get("vendor_number")
        item_number = request.GET.get("item_number")
        city_level = request.GET.get("cityLevel")
        county_level = request.GET.get("countyLevel")
        zip_code_level = request.GET.get("zip_codeLevel")

        # Start the queryset
        sales_query = Sale.objects.select_related("product", "store")

        # Apply filters
        if store_name:
            sales_query = sales_query.filter(store__store_name=store_name)
        if city:
            sales_query = sales_query.filter(store__city=city)
        if zip_code:
            sales_query = sales_query.filter(store__zip_code=zip_code)
        if county_number:
            sales_query = sales_query.filter(store__county_number=county_number)
        if category:
            sales_query = sales_query.filter(product__category_name=category)
        if vendor_number:
            sales_query = sales_query.filter(product__vendor_number=vendor_number)
        if item_number:
            sales_query = sales_query.filter(product__item_number=item_number)

        city_aggregated_data = []
        county_aggregated_data = []
        zip_code_aggregated_data = []
        # Aggregate data by city
        if city_level == "true":
            city_aggregated_data = sales_query.values("store__city").annotate(
                total_stock=Sum(F("bottles_sold")),
                total_sales=Sum("sale_dollars"),
                total_profit=Sum("sale_dollars")
                - Sum(F("product__state_bottle_cost") * F("bottles_sold")),
            )
            print(f"{city_aggregated_data=}")

        if county_level == "true":  # Aggregate data by county
            county_aggregated_data = sales_query.values("store__county").annotate(
                total_stock=Sum(F("bottles_sold")),
                total_sales=Sum("sale_dollars"),
                total_profit=Sum("sale_dollars")
                - Sum(F("product__state_bottle_cost") * F("bottles_sold")),
            )
            print(f"{county_aggregated_data=}")

        if zip_code_level == "true":
            # Aggregate data by zip code
            zip_code_aggregated_data = sales_query.values("store__zip_code").annotate(
                total_stock=Sum(F("bottles_sold")),
                total_sales=Sum("sale_dollars"),
                total_profit=Sum("sale_dollars")
                - Sum(F("product__state_bottle_cost") * F("bottles_sold")),
            )
            print(f"{zip_code_aggregated_data=}")

        # Combine all levels of data into a response
        aggregated_data = {
            "city_data": city_aggregated_data,
            "county_data": county_aggregated_data,
            "zip_code_data": zip_code_aggregated_data,
        }

        return Response(aggregated_data, status=status.HTTP_200_OK)


from django.http import JsonResponse
from .models import Store


def get_zip_codes(request):
    zip_codes = Store.objects.values_list("zip_code", flat=True).distinct()
    return JsonResponse(list(zip_codes), safe=False)


def get_cities(request):
    cities = Store.objects.values_list("city", flat=True).distinct()
    return JsonResponse(list(cities), safe=False)


def get_county_numbers(request):
    county_numbers = Store.objects.values_list("county_number", flat=True).distinct()
    return JsonResponse(list(county_numbers), safe=False)


def get_categories(request):
    categories = Product.objects.values_list("category_name", flat=True).distinct()
    return JsonResponse(list(categories), safe=False)


def get_vendor_numbers(request):
    vendor_numbers = Product.objects.values_list("vendor_number", flat=True).distinct()
    return JsonResponse(list(vendor_numbers), safe=False)


def get_item_numbers(request):
    item_numbers = Product.objects.values_list("item_number", flat=True).distinct()
    return JsonResponse(list(item_numbers), safe=False)
