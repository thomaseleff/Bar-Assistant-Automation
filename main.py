"""
Information
---------------------------------------------------------------------
Name        : main.py
Location    : ~/
Author      : Tom Eleff
Published   : 2023-09-30
Revised on  : ~

Description
---------------------------------------------------------------------
Posts cocktail recipes and ingredients to the bar-assistant DB.
"""

# Import modules
import os
import barpy as bp

if __name__ == '__main__':

    # Retrieve .env parameters
    bar = {
        'setup': {
            'api': bp.utils.load_parameter(
                envLoc=os.path.dirname(__file__),
                envParameter='BARPY_API'
            ),
            'username': bp.utils.load_parameter(
                envLoc=os.path.dirname(__file__),
                envParameter='BARPY_USERNAME'
            ),
            'password': bp.utils.load_parameter(
                envLoc=os.path.dirname(__file__),
                envParameter='BARPY_PASSWORD'
            )
        }
    }

    # Validate .env parameters
    bp.utils.validate_config(
        bar,
        bp.dtypes.bar
    )

    # Punch in the barkeeper
    barkeeper = bp.automation.Barkeeper(
        **bar['setup']
    )

    # Create cocktail
    barkeeper.create_cocktail(
        json={
            "name": "Cocktail example",
            "instructions": "1. Step\n2. Step",
            "garnish": "Lemon wheel",
            "description": "A short cocktail description",
            "source": "http://wikipedia.org",
            "images": [
                1,
                2
            ],
            "tags": [
                "Gin",
                "IBA Official"
            ],
            "glass_id": 1,
            "ingredients": [{
                "ingredient_id": 1,
                "amount": 30,
                "units": "ml",
                "optional": False,
                "sort": 0
            }]
        }
    )

    # Create ingredient
    barkeeper.create_ingredient(
        json={
            "name": "Oloroso Sherry",
            "strength": 20,
            "description": (
                "Made in a strictly oxidative style, " +
                "olorosos are quite dark in appearance."
            ),
            "origin": "Spain",
            "ingredient_category_id": 7,
        }
    )

    # Clock out
    barkeeper.clock_out()
