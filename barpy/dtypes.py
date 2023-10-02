"""
Information
---------------------------------------------------------------------
Name        : dtypes.py
Location    : ~/barpy/
Author      : Tom Eleff
Published   : 2023-09-30
Revised on  : ~

Description
---------------------------------------------------------------------
Contains dtype dictionaries for validation.
"""

# Define dtypes
bar = {
    'setup': {
        'api': 'str',
        'username': 'str',
        'password': 'str',
    }
}

cocktail = {
    "json": {
        "name": "str",
        "instructions": "str",
        "garnish": "str",
        "description": "str",
        "source": "str",
        "images": "list",
        "tags": "list",
        "glass_id": "int",
        "ingredients": "list"
    }
}

ingredient = {
    "json": {
        "name": "str",
        "strength": "int",
        "description": "str",
        "origin": "str",
        "images": "list",
        "ingredient_category_id": "int",
        "color": "str",
        "parent_ingredient_id": "int"
    }
}
