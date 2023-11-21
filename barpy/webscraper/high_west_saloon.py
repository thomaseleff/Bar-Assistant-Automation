"""
Information
---------------------------------------------------------------------
Name        : high_west_saloon.py
Location    : ~/barpy/webscraper/
Author      : Tom Eleff
Published   : 2023-10-23
Revised on  : 2023-11-21

Description
---------------------------------------------------------------------
Contains the web-scraper class to generate the High-West Saloon
Bar Assistant DB.
"""

import requests
import os
import urllib.parse as up
import barpy.utils as utils
from bs4 import BeautifulSoup
from barpy.webscraper.generic_webscraper import GenericWebscraper
from barpy.webscraper.patterns import Patterns


# Define the High-West Saloon Bar Class
class HighWestSaloon(GenericWebscraper):

    # Define bar metadata
    metadata = {
        'name': 'High West Saloon',
        'address': '703 Park Ave.',
        'city': 'Park City',
        'stateCode': 'UT',
        'zipCode': '84060',
        'lat': '40.646519',
        'long': '-111.498573',
        'url': 'https://highwest.com/pages/saloon',
        'affiliation': 'High West Distillery',
        'notableBarkeepers': 'Christoper Benton Dorsey',
        'signature': 'Penicillin'
    }

    # Define bar base URL
    config = {
        'base': 'https://highwest.com/blogs/recipes/'
    }

    def __init__(
        self,
        outPath
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        Initializes an instance of the High-West Saloon bar class.
        """

        # Add output directory
        self.config['outputs'] = {
            'path': outPath,
            'root': self.metadata['name'].lower().replace(' ', '-'),
            'subFolders': ['db', 'html']
        }

        # Create output directory
        utils.generate_output_directory(
            config=self.config
        )

        # Output bar metadata config
        utils.write_config(
            configLoc=os.path.join(
                self.config['outputs']['path'],
                self.config['outputs']['root'],
                'metadata.json'
            ),
            config={'metadata': self.metadata}
        )

        # Create cocktail categories
        self.categories = self.create_collection_config()

        # Create html database
        self.create_html_database()

    def create_collection_config(
        self,
        categories={}
    ):
        """
        Variables
        ---------------------------------------------------------------------
        categories              = <dict> Dictionary object containing the
                                    bar menu categories.

        Description
        ---------------------------------------------------------------------
        Returns all High-West Saloon cocktail {categories} as a dictionary.

        E.g.,
            [
                "Summer Cocktails": {
                    "url": "tagged/cat-summer-cocktails",
                    "path": ["kings-peak"],
                }
            ]
        """

        # Create cocktail categories
        if not os.path.isfile(
            os.path.join(
                self.config['outputs']['path'],
                self.config['outputs']['root'],
                'config.json'
            )
        ):
            
            # Retrieve the cocktail recipe listing page web-object
            request = requests.get(self.config['base'])

            if request.status_code == 200:

                # Parse the html text content
                text = BeautifulSoup(request.text, 'lxml')

                # Parse the cocktail categories into a dictionary
                for category in text.find(
                    'select',
                    attrs={'class': 'blog-filter'}
                ).find_all('option'):

                    if not category.attrs['value'] == '':
                        categories[
                            category.get_text(strip=True)
                        ] = {
                            'url': up.urljoin(
                                'tagged/',
                                category.attrs['value']
                            )
                        }

            else:
                print('*** ERROR: Failed to request %s.' % (self.config['base']))
                exit()

            # For each category, parse cocktail names
            for category in categories.keys():

                categories[category]['path'] = (
                    self.parse_cocktail_recipe_pages(
                        url=up.urljoin(
                            self.config['base'],
                            categories[category]['url']
                        )
                    )
                )

            # Output cocktail categories
            utils.write_config(
                configLoc=os.path.join(
                    self.config['outputs']['path'],
                    self.config['outputs']['root'],
                    'config.json'
                ),
                config=categories
            )

        else:
            
            # Import cocktail categories
            categories = utils.read_config(
                configLoc=os.path.join(
                    self.config['outputs']['path'],
                    self.config['outputs']['root'],
                    'config.json'
                )
            )

        # Return the dictionary of cocktail categories
        return categories

    def parse_cocktail_recipe_pages(
        self,
        url,
        pages=[],
        n=1
    ):
        """
        Variables
        ---------------------------------------------------------------------
        url                     = <str> URL web-address to a cocktail
                                    category listing page.
        pages                   = <list> List object containing cocktail
                                    recipe names.
        n                       = <int> First listing page number.

        Description
        ---------------------------------------------------------------------
        Returns all High-West Saloon cocktail recipe {pages} associated with
        a cocktail category.
        """

        while True:

            # Retrieve the cocktail recipe listing page web-object
            request = requests.get('?'.join([url, '='.join(['page', str(n)])]))

            if request.status_code == 200:

                # Parse the html text content
                text = BeautifulSoup(request.text, 'lxml')

                # If the current listing page does not contain cocktails, break
                if text.find(
                    'h3',
                    attrs={'class': 'p-4 mt-9 mb-20'}
                ):
                    break

                # Otherwise, parse the cocktail recipe name into a list
                else:
                    pages = pages + [
                        i.attrs['href'].split('/')[-1] for i in text.find_all(
                            'a',
                            attrs={'class': 'mb-6 cursor-pointer'}
                        )
                    ]

            else:
                print(
                    '*** ERROR: Failed to request %s.' % (
                        '?'.join([url, '='.join(['page', str(n)])])
                    )
                )
                exit()

            # Increment the listing page number
            n += 1

        # Return the list of cocktail recipe pages
        return pages

    def create_html_database(
        self,
        cocktails=[]
    ):
        """
        Variables
        ---------------------------------------------------------------------
        cocktails               = <list> Empty list object containing cocktail
                                    recipe pages.
        Description
        ---------------------------------------------------------------------
        Downloads all High-West Saloon cocktail recipe pages to local html
        documents.
        """

        # Create a unique list of all cocktails
        for category in list(self.categories.keys()):
            cocktails = cocktails + self.categories[category]['path']

        # Sort and remove duplicates
        cocktails = sorted(set(cocktails))

        # Create html database
        for cocktail in cocktails:
            if not os.path.isfile(
                os.path.join(
                    self.config['outputs']['path'],
                    self.config['outputs']['root'],
                    'html',
                    '%s.html' % (cocktail)
                )
            ):

                # Retrieve the cocktail recipe page web-object
                request = requests.get(up.urljoin(self.config['base'], cocktail))

                if request.status_code == 200:
                    with open(
                        os.path.join(
                            self.config['outputs']['path'],
                            self.config['outputs']['root'],
                            'html',
                            '%s.html' % (cocktail)
                        ),
                        'wb'
                    ) as file:
                        file.write(request.content)

                else:
                    print('*** ERROR: Failed to request %s.' % (
                        up.urljoin(self.config['base'], cocktail)
                    ))
                    exit()

    def create_cocktail_collection(
        self,
        name,
        cocktails,
        failures=[]
    ):
        """
        Variables
        ---------------------------------------------------------------------
        name                    = <str> Name of the cocktail collection
        cocktails               = <list> List object containing cocktail
                                    recipe pages.

        Description
        ---------------------------------------------------------------------
        Creates a High-West Saloon bar cocktail collection.
        """

        # Create cocktail collection
        collection = self.Collection(
            name=name
        )

        # Add cocktails to cocktail collection
        for cocktail in cocktails:

            # Create cocktail
            try:
                collection.cocktails = collection.cocktails + [
                    self.parse_cocktail_recipe(
                        page=cocktail
                    )
                ]

            except IndexError:
                failures = failures + [cocktail]

        # Log
        for f in failures:
            print('*** ERROR: Parsing [%s] failed.' % (f))

        # Return collection
        return collection

    def parse_cocktail_recipe(
        self,
        page,
        sort=0,
        idx=0
    ):
        """
        Variables
        ---------------------------------------------------------------------
        page                    = <str> URL web-address path to a cocktail
                                    recipe page.
        sort                    = <int> Ingredient sort order
        idx                     = <int> Recipe line index

        Description
        ---------------------------------------------------------------------
        Parses the cocktail recipe from {page} and returns a dictionary from
        the Cocktail class object.
        """

        # Retrieve the cocktail recipe page web-object
        with open(
            os.path.join(
                self.config['outputs']['path'],
                self.config['outputs']['root'],
                'html',
                '%s.html' % (page)
            ),
            'rb'
        ) as file:

            # Parse the html text content
            text = BeautifulSoup(file.read().decode('utf8'), 'lxml')

            # Initialize cocktail
            cocktail = self.Cocktail()

            # Parse the cocktail recipe name
            cocktail.name = self.title_case(
                self.normalize_unicode(
                    s=text.find(
                        'div',
                        attrs={'class': 'p-8 pb-0'}
                    ).get_text(strip=True)
                )
            )

            # Parse the cocktail source
            cocktail.source = up.urljoin(self.config['base'], page)

            # Convert the recipe to a list
            recipe = self.split_lines(
                text=str(text.find(
                    'div',
                    attrs={'class': 'p-8 pb-0 blog-desc'}
                )),
                remove=[
                    'IF SHIPPING DOUBLE RYE TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING DOUBLE RYE AND/OR RENDEZVOUS RYE TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING DOUBLE RYE  OR HIGH WEST BOURBON TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING DOUBLE RYE OR HIGH WEST BOURBON TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING DOUBLE RYE OR HIGH WEST BOURBON  TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING RENDEZVOUS RYE TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING HIGH WEST BOURBON TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING CAMPFIRE TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM',
                    'IF SHIPPING A MIDWINTER NIGHTS DRAM TO CALIFORNIA VIEW PRODUCT AT SHIP.HIGHWEST.COM'
                ],
                filtr=[
                    'DOWNLOAD',
                    'WATCH A TUTORIAL',
                    'INGREDIENTS:',
                    'DIRECTIONS:',
                    (
                        'WATCH OUR US SKI AND SNOWBOARD TEAM ' +
                        'COCKTAIL HOW-TO VIDEO'
                    ),
                    'TRY THE OLD FASHIONED OLD FASHIONED',
                    'TRY THE MODERN OLD FASHIONED',
                    'ABSINTHE RINSED ROCKS GLASS',
                    'FEVER TREE SODA WATER',
                    'CHAMOMILE TEABAG',
                    'BOILING WATER',
                    'CHARTREUSE AND ABSINTHE WHIPPED CREAM (HAND SHAKEN)',
                    'CHILLED SODA WATER',
                    'LEMON TWIST',
                    'SODA WATER',
                    'PEATED SCOTCH FLOAT',
                    'ORANGE/LEMON TWIST GARNISH',
                    'FEVER TREE GINGER BEER',
                    "PEYCHAUD'S BITTERS GARNISH",
                    'CINNAMON STICK',
                    'BALLAST POINT HIGH WEST BARREL AGED VICTORY AT SEA',
                    'ROSEMARY SPRIG',
                    'RED ROCK DRIOMA',
                    'PINNEAPLE WEDGE',
                    'TONIC WATER',
                    'HOT WATER',
                    'GRAPEFRUIT TWIST',
                    'ABSINTHE RISE',
                    'LEMON',
                    'ORANGE',
                    'ORCHID',
                    'NUTMEG',
                    'ODELL BREWING CO. SIPPIN PRETTY',
                    'PELLEGRINO BLOOD ORANGE SODA',
                    'BLOOD ORANGE',
                    'THYME',
                    'FEVER TREE CLUB SODA',
                    'STAR ANISE',
                    'LUXARDO CHERRIES',
                    'MUDDLE 4 CUBES OF WATERMELON',
                    'ABSINTHE RINSE'
                ]
            )

            # Parse the cocktail recipe ingredients
            for index, line in enumerate(recipe):
                line = self.cleanse_trailing_period(s=line)

                # Parse egg ingredients
                if Patterns.match(
                    pattern=Patterns.default_ingredients(),
                    s=line
                ):

                    # Retrieve egg ingredient defaults
                    defaults = Patterns.extract_ingredient_defaults(
                        pattern=Patterns.default_ingredients(),
                        s=line,
                        lookup=Patterns.Defaults.defaults
                    )

                    # Add cocktail ingredient
                    for default in defaults:
                        cocktail.ingredients = cocktail.ingredients + [
                            self.Ingredient(
                                sort=sort,
                                name=self.title_case(
                                    default['name']
                                ),
                                amount=self.convert_amount_to_numeric(
                                    default['amount']
                                ),
                                units=self.title_case(
                                    default['units']
                                )
                            ).to_dict()
                        ]

                        # Increment sort
                        sort += 1

                    # Increment idx
                    idx += 1

                # Parse all other ingredients
                elif Patterns.match(
                    pattern=Patterns.all_ingredients(),
                    s=line
                ):
                    
                    # Retrieve ingredient amount
                    amount = Patterns.extract_amount(
                        pattern=Patterns.all_amounts(),
                        s=line
                    )

                    # Retrieve ingredient unit
                    units = Patterns.extract_unit(
                        pattern=Patterns.all_units(),
                        s=line
                    )

                    # Retrieve ingredient name
                    name = Patterns.extract_ingredient(
                        amount=amount,
                        units=units,
                        s=line
                    )

                    # Retain cocktail ingredient recipe instructions as description
                    if '(' in name:

                        name, description = self.cleanse_ingredient_with_recipe(
                            s=name,
                            filtr=[
                                'RECIPE BELOW',
                                'SEE WHISKEY LEMONADE FOR RECIPE'
                            ]
                        )
                    else:
                        description = None

                    # Add cocktail ingredient
                    cocktail.ingredients = cocktail.ingredients + [
                        self.Ingredient(
                            sort=sort,
                            name=self.title_case(
                                s=self.cleanse_leading_and_trailing_period(
                                    s=name
                                )
                            ),
                            amount=self.convert_amount_to_numeric(
                                s=amount
                            ),
                            units=self.title_case(s=units),
                            description=description
                        ).to_dict()
                    ]

                    # Increment sort and idx
                    sort += 1
                    idx += 1

                # Skip garnish if found in ingredients
                elif Patterns.match(
                    pattern=Patterns.ingredients_as_garnishes(),
                    s=line
                ) and (
                    index < len(recipe)
                ):
                    # cocktail.garnish = self.proper_case(
                    #     s=Patterns.extract_garnish(
                    #         pattern=Patterns.ingredients_as_garnishes(),
                    #         s=line
                    #     )
                    # )

                    # Increment idx
                    idx += 1

                else:
                    break

            # Parse the cocktail recipe instructions
            if recipe[idx:]:
                cocktail.instructions = self.proper_case(
                    '\n'.join(
                        recipe[idx:]
                    )
                )
            else:
                pass

            # Parse the garnish from the instructions
            if not cocktail.garnish:
                cocktail.garnish = self.proper_case(
                    s=self.cleanse_leading_and_trailing_period(
                        s=Patterns.extract_garnish_from_instructions(
                            s=cocktail.instructions
                        )
                    )
                )

            # Parse the glass from the instructions
            cocktail.glass = self.title_case(
                s=Patterns.extract_glass_from_instructions(
                    s=cocktail.instructions
                )
            )

            # Parse the method from the instructions
            cocktail.method = self.title_case(
                s=Patterns.extract_method_from_instructions(
                    s=cocktail.instructions
                )
            )

            # Parse the recipe image url
            cocktail.images = [
                self.Image(
                    url=self.parse_image_url(text=text),
                    copyright=self.metadata['name'],
                    sort=0
                ).to_dict()
            ]

            return cocktail.to_dict()

    def parse_image_url(
        self,
        text
    ):

        return up.urljoin(
            'https://',
            text.find(
                'div',
                attrs={'class': 'lg:w-3/6 lg:float-right'}
            ).find('img')['data-src'].replace(r'{width}', '600')
        )
