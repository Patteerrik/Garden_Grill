from django.db import models


# Model representing a menu category
class MenuCategory(models.Model):
    # Name of the category, maximum 100 characters
    name = models.CharField(max_length=100)
    # Optional description field
    description = models.TextField(blank=True)

    def __str__(self):
        # Returns the name of the category when represented as a string
        return self.name


# Model representing a menu item
class MenuItem(models.Model):
    # Name of the menu item, maximum 100 characters
    name = models.CharField(max_length=100)
    # Description of the menu item
    description = models.TextField()
    # Price field with up to 5 digits and 2 decimal places
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # Foreign key linking menu item to a category
    category = models.ForeignKey(
        MenuCategory,
        # Allows access to related menu items from the category
        related_name='menu_items',
        # Deletes menu items when the related category is deleted
        on_delete=models.CASCADE
        )

    def __str__(self):
        # Returns the name of the menu item when represented as a string
        return self.name
