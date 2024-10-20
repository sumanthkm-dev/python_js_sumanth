import pandas as pd
from django.core.management.base import BaseCommand
from salesapp.models import Store, Product, Sale


class Command(BaseCommand):
    help = "Import data from CSV file using Pandas"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The CSV file to import")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        data = pd.read_csv(csv_file)

        # Clean numeric columns to remove commas and convert to appropriate types
        data["Sale (Dollars)"] = (
            data["Sale (Dollars)"].str.replace(",", "").astype(float)
        )
        data["Volume Sold (Liters)"] = (
            data["Volume Sold (Liters)"].str.replace(",", "").astype(float)
        )
        data["Bottle Volume (ml)"] = (
            data["Bottle Volume (ml)"].str.replace(",", "").astype(float)
        )
        data["State Bottle Cost"] = (
            data["State Bottle Cost"].str.replace(",", "").astype(float)
        )
        data["State Bottle Retail"] = (
            data["State Bottle Retail"].str.replace(",", "").astype(float)
        )
        data["Bottles Sold"] = data["Bottles Sold"].str.replace(",", "").astype(int)

        # Convert volume_sold_gallons and handle blanks
        data["Volume Sold (Gallons)"] = pd.to_numeric(
            data["Volume Sold (Gallons)"].str.replace(",", ""), errors="coerce"
        )

        for _, row in data.iterrows():
            # Get or create the store
            store, _ = Store.objects.get_or_create(
                store_number=row["Store Number"],
                defaults={
                    "store_name": (
                        row["store_name"]
                        if pd.notna(row["store_name"]) and row["store_name"] != ""
                        else "Unknown Store"
                    ),
                    "address": (
                        row["Address"]
                        if pd.notna(row["Address"]) and row["Address"] != ""
                        else ""
                    ),
                    "city": (
                        row["City"]
                        if pd.notna(row["City"]) and row["City"] != ""
                        else "Unknown City"
                    ),
                    "zip_code": (
                        row["Zip Code"]
                        if pd.notna(row["Zip Code"]) and row["Zip Code"] != ""
                        else "0"
                    ),
                    "store_location": (
                        row["Store Location"]
                        if pd.notna(row["Store Location"])
                        and row["Store Location"] != ""
                        else ""
                    ),
                    "county_number": (
                        row["County Number"]
                        if pd.notna(row["County Number"]) and row["County Number"] != ""
                        else 0
                    ),
                    "county": (
                        row["County"]
                        if pd.notna(row["County"]) and row["County"] != ""
                        else "Unknown County"
                    ),
                },
            )

            # Get or create the product
            product, _ = Product.objects.get_or_create(
                item_number=row["Item Number"],
                defaults={
                    "item_desc": (
                        row["item_desc"]
                        if pd.notna(row["item_desc"]) and row["item_desc"] != ""
                        else "Unknown Item"
                    ),
                    "category": (
                        row["Category"]
                        if pd.notna(row["Category"]) and row["Category"] != ""
                        else 0
                    ),
                    "category_name": (
                        row["category_name"]
                        if pd.notna(row["category_name"]) and row["category_name"] != ""
                        else "Unknown Category"
                    ),
                    "vendor_number": (
                        row["Vendor Number"]
                        if pd.notna(row["Vendor Number"]) and row["Vendor Number"] != ""
                        else 0
                    ),
                    "vendor_name": (
                        row["vendor_name"]
                        if pd.notna(row["vendor_name"]) and row["vendor_name"] != ""
                        else "Unknown Vendor"
                    ),
                    "pack": (
                        row["Pack"]
                        if pd.notna(row["Pack"]) and row["Pack"] != ""
                        else 1
                    ),
                    "bottle_volume_ml": (
                        row["Bottle Volume (ml)"]
                        if pd.notna(row["Bottle Volume (ml)"])
                        and row["Bottle Volume (ml)"] != ""
                        else 1
                    ),
                    "state_bottle_cost": (
                        row["State Bottle Cost"]
                        if pd.notna(row["State Bottle Cost"])
                        and row["State Bottle Cost"] != ""
                        else 0.0
                    ),
                    "state_bottle_retail": (
                        row["State Bottle Retail"]
                        if pd.notna(row["State Bottle Retail"])
                        and row["State Bottle Retail"] != ""
                        else 0.0
                    ),
                },
            )

            # Handle volume sold gallons
            volume_sold_gallons = row["Volume Sold (Gallons)"]
            if pd.isna(volume_sold_gallons) or volume_sold_gallons == "":
                volume_sold_gallons = 0.0  # or set a default value

            # Create the Sale object
            Sale.objects.create(
                invoice_number=(
                    row["Invoice/Item Number"]
                    if pd.notna(row["Invoice/Item Number"])
                    and row["Invoice/Item Number"] != ""
                    else "Unknown Invoice"
                ),
                product=product,
                store=store,
                date=(
                    row["Date"]
                    if pd.notna(row["Date"]) and row["Date"] != ""
                    else pd.to_datetime("today")
                ),  # Use today if date is missing
                bottles_sold=(
                    row["Bottles Sold"]
                    if pd.notna(row["Bottles Sold"]) and row["Bottles Sold"] != ""
                    else 1
                ),
                sale_dollars=(
                    row["Sale (Dollars)"]
                    if pd.notna(row["Sale (Dollars)"]) and row["Sale (Dollars)"] != ""
                    else 1
                ),
                volume_sold_liters=(
                    row["Volume Sold (Liters)"]
                    if pd.notna(row["Volume Sold (Liters)"])
                    and row["Volume Sold (Liters)"] != ""
                    else 1
                ),
                volume_sold_gallons=volume_sold_gallons,  # Use the processed variable
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
