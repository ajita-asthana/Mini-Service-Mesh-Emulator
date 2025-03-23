class ProductCatalog:
    def __init__(self):
        """
        Initialize an empty catalog
        """
        self.catalog = {}

    def add_product(self, product_id, name, price):
        """
        Add a new product to the catalog.
        """
        self.catalog[product_id] = {"name": name, "price": price}
        print(f"Product {name} added with price ${price}.")

    def apply_disocunt(self, discount_percentage):
        """
        Apply a discount to all products in the catalog. 
        """
        for product in self.catalog.values():
            product['price'] *= (1 - discount_percentage / 100)
        print(f"Discount of {discount_percentage}% applied to all products.")

    def get_products_above_price(self, price):
        """
        Return a list of products with a price above a given threshold.
        """
        return [product["name"] for product in self.catalog.values() if product["price"] > price]
    
    def __str__(self):
        """
        Return a string representation of the product catalog.
        """
        return '\n'.join(
            [f"{product['name']} (ID: {product_id}): ${product['price']:.2f}"
                for product_id, product in self.catalog.items()
            ]
        )
    
# Example Usage
catalog = ProductCatalog()
catalog.add_product(1, "Laptop", 1000)
catalog.add_product(2, "Smartphone", 1600)
catalog.add_product(3, "Headphones", 300)

# Apply a 10% discount to all products
catalog.apply_disocunt(10)

#Get product with price above $500
print(f"Products above $500: {catalog.get_products_above_price(500)}")

# Print all products in the catalog
print("\n Product Catalog:")
print(catalog)