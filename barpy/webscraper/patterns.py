"""
Information
---------------------------------------------------------------------
Name        : patterns.py
Location    : ~/barpy/webscraper/
Author      : Tom Eleff
Published   : 2023-10-23
Revised on  : ~

Description
---------------------------------------------------------------------
Contains the Patterns class.
"""

import re
import nltk


# Define the Patterns class
class Patterns():

    # Regex compiler function(s)
    def all_ingredients():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for cocktail ingredients.
        """

        return r'(%s)' % (
            '|'.join([
                Patterns.ingredients_amount_start(),
                Patterns.ingredients_unit_start(),
                Patterns.ingredients_missing_unit()
            ])
        )

    def ingredients_amount_start():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for cocktail ingredient that begin with
        the amount.
        """

        return ''.join([
            r'^',
            r'(%s)' % (
                '|'.join(
                    Patterns.Amounts.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Separators.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    [r'\b'+i+r'\b' for i in Patterns.Units.all()]
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Separators.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Ingredients.all()
                )
            )
        ])

    def ingredients_unit_start():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for cocktail ingredient that begin with
        the unit.
        """

        return ''.join([
            r'^',
            r'(%s)' % (
                '|'.join(
                    [r'\b'+i+r'\b' for i in Patterns.Units.all()]
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Separators.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Ingredients.all()
                )
            )
        ])

    def ingredients_missing_unit():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for cocktail ingredient that are missing
        the unit.
        """

        return ''.join([
            r'^',
            r'(%s)' % (
                '|'.join(
                    Patterns.Amounts.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Separators.all()
                )
            ),
            r'(%s)' % (
                '|'.join(
                    Patterns.Ingredients.all()
                )
            )
        ])

    def ingredients_as_garnishes():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for garnishes listed within the cocktail
        ingredients.
        """

        return r'^(%s)$' % (
            '|'.join(
                Patterns.Garnishes.ingredients
            )
        )

    def all_amounts():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for amounts.
        """

        return r'^(%s)' % (
            '|'.join(
                Patterns.Amounts.all()
            )
        )

    def all_units():
        """
        Description
        ---------------------------------------------------------------------
        Compiles all regex-patterns for units.
        """

        return r'(^%s)' % (
            '|'.join(
                [r'\b'+i+r'\b' for i in Patterns.Units.all()]
            )
        )

    # Generic match function(s)
    def match(
        pattern,
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        pattern                 = <str> Regex-pattern
        s                       = <str> String to match

        Description
        ---------------------------------------------------------------------
        Returns whether {s} matches {pattern}.
        """

        return re.match(
            pattern=pattern,
            string=s,
            flags=re.IGNORECASE
        )

    # Cocktail attribute extraction function(s)
    def extract_amount(
        pattern,
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        pattern                 = <str> Regex-pattern
        s                       = <str> String to search

        Description
        ---------------------------------------------------------------------
        Returns the amount that matches {pattern} from {s}. If no match is
        found, the default amount is returned.
        """

        if re.search(
            pattern=pattern,
            string=s,
            flags=re.IGNORECASE
        ):
            return re.search(
                pattern=pattern,
                string=s,
                flags=re.IGNORECASE
            ).group(1)

        else:
            return Patterns.Amounts.default()

    def extract_unit(
        pattern,
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        pattern                 = <str> Regex-pattern
        s                       = <str> String to search

        Description
        ---------------------------------------------------------------------
        Returns the unit that matches {pattern} from {s}. If no match is
        found, the default unit is returned.
        """

        if re.search(
            pattern=pattern,
            string=s,
            flags=re.IGNORECASE
        ):
            return re.search(
                pattern=pattern,
                string=s,
                flags=re.IGNORECASE
            ).group(1)
        else:
            return Patterns.Units.default()

    def extract_ingredient(
        amount,
        units,
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        amount                  = <str> Ingredient smount
        units                   = <str> Ingredient unit
        s                       = <str> String to parse

        Description
        ---------------------------------------------------------------------
        Returns {s} after removing any substrings that match {amount} or
        {units}.
        """

        # Remove amount
        if amount:
            s = re.sub(
                pattern=r'\b%s\b' % (amount),
                repl='',
                string=str(s),
                count=1,
                flags=re.IGNORECASE
            )

        # Remove units
        if units:
            s = re.sub(
                pattern=r'\b%s\b' % (units),
                repl='',
                string=str(s),
                count=1,
                flags=re.IGNORECASE
            )

        # Cleanse and return the final ingredient
        return str(s)

    def extract_garnish(
        pattern,
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        pattern                 = <str> Regex-pattern
        s                       = <str> String to parse

        Description
        ---------------------------------------------------------------------
        Returns {s} after removing any substrings that match the {pattern}.
        """

        # Cleanse and return the final garnish
        return re.sub(
            pattern=pattern,
            repl='',
            string=re.sub(
                pattern=r'\b(%s)\b' % (
                    '|'.join(
                        Patterns.Garnishes.filtr
                    )
                ),
                repl='',
                string=str(s),
                flags=re.IGNORECASE
            ),
            flags=re.IGNORECASE
        ).strip().replace('  ', ' ')

    def extract_garnish_from_instructions(
        s
    ):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to parse

        Description
        ---------------------------------------------------------------------
        Returns the last garnish from the instructions when found within
        the sentence or its sentence fragments.
        """

        # Cleanse and return the last garnish from the instructions
        if s:
            try:
                return Patterns.extract_garnish(
                    pattern=r'(%s)' % (
                        '|'.join(
                            Patterns.Garnishes.as_instruction
                        )
                    ),
                    s=[
                        line for line in nltk.sent_tokenize(
                            str(s)
                        ) if re.search(
                            pattern=r'(%s)' % (
                                '|'.join(
                                    Patterns.Garnishes.as_instruction
                                )
                            ),
                            string=line.strip(),
                            flags=re.IGNORECASE
                        )
                    ][-1]
                )

            except IndexError:

                # If no garnish is found at first,
                #   try replacing commas with periods and retry
                #   searching within the sentence fragments
                try:
                    return Patterns.extract_garnish(
                        pattern=r'(%s)' % (
                            '|'.join(
                                Patterns.Garnishes.as_instruction +
                                Patterns.Garnishes.as_phrase
                            )
                        ),
                        s=[
                            line for line in nltk.sent_tokenize(
                                str(s).replace(',', '.')
                            ) if re.search(
                                pattern=r'(%s)' % (
                                    '|'.join(
                                        Patterns.Garnishes.as_instruction +
                                        Patterns.Garnishes.as_phrase
                                    )
                                ),
                                string=line.strip(),
                                flags=re.IGNORECASE
                            )
                        ][-1]
                    )

                except IndexError:

                    # If no garnish is found within phrases,
                    #   try replacing 'and' with periods and retry
                    #   searching within the sentence fragments
                    try:
                        return Patterns.extract_garnish(
                            pattern=r'(%s)' % (
                                '|'.join(
                                    Patterns.Garnishes.as_instruction +
                                    Patterns.Garnishes.as_phrase
                                )
                            ),
                            s=[
                                line for line in nltk.sent_tokenize(
                                    str(s).replace(' and', '.')
                                ) if re.search(
                                    pattern=r'(%s)' % (
                                        '|'.join(
                                            Patterns.Garnishes.as_instruction +
                                            Patterns.Garnishes.as_phrase
                                        )
                                    ),
                                    string=line.strip(),
                                    flags=re.IGNORECASE
                                )
                            ][-1]
                        )
                    except IndexError:
                        return Patterns.Garnishes.default()
        else:
            return Patterns.Garnishes.default()

    def extract_glass_from_instructions(
        s,
    ):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to parse

        Description
        ---------------------------------------------------------------------
        Returns the glass from the instructions when found. If no glass is
        found, the default glass is returned.
        """

        # Cleanse and return the first glass from the instructions
        if s:
            for glass in Patterns.Glasses.all():
                if re.search(
                    glass,
                    string=s,
                    flags=re.IGNORECASE
                ):
                    return glass
        else:
            return Patterns.Glasses.default()

    def extract_method_from_instructions(
        s,
    ):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to parse

        Description
        ---------------------------------------------------------------------
        Returns the cocktail method from the instructions when found. If no
        method is found, the default method is returned.
        """

        # Cleanse and return the first method from the instructions
        if s:
            for method in Patterns.Methods.all():
                if re.search(
                    method,
                    string=s,
                    flags=re.IGNORECASE
                ):
                    return method
        else:
            return Patterns.Methods.default()

    class Separators():

        spaces = [
            r' ',
            r''
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for separators.
            """

            return Patterns.Separators.spaces

    class Amounts():

        amount = [
            r'(\d+\.\d+)',
            r'(\d+\-\d+)',
            r'(\d+ \- \d+)',
            r'(\d+TO\d+)',
            r'(\d+ TO \d+)',
            r'(\d+\/\d+)',
            r'(\d+ \d+\/\d+)',
            r'(\d+ \d+\/ \d+)',
            r'(\d+ \d+ \/\d+)',
            r'(\d+ \d+ \/ \d+)',
            r'(\d+)',
            r'(\.\d+)'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for numeric Amounts.
            """
            return Patterns.Amounts.amount

        def default():
            """
            Description
            ---------------------------------------------------------------------
            Returns the default Amount value.
            """
            return '1'

    class Units():

        imperial = [
            'POUND',
            'POUNDS',
            'LB',
            'LB.',
            'STONE',
            'STONES',
            'OUNCE',
            'OUNCES',
            'OZ',
            'OZ.',
            'FLUID OUNCE',
            'FLUID-OUNCE',
            'FLUID OUNCES',
            'FLUID-OUNCES',
            'FL OZ',
            'FL-OZ',
            'FL. OZ.',
            'FL.-OZ.',
            'GALLON',
            'GALLONS',
            'GAL',
            'GAL.',
            'PINT',
            'PINTS',
            'PT',
            'PT.',
            'QUART',
            'QUARTS',
            'QT',
            'QT.',
            'BARREL',
            'BARRELS',
            'TEASPOON',
            'TEASPOONS',
            'TEA SPOON',
            'TEA SPOONS',
            'TEA-SPOON',
            'TEA-SPOONS',
            'TSP',
            'TSP.',
            'TSPN',
            'TSPN.',
            'T',
            'T.',
            'TABLESPOON',
            'TABLESPOONS',
            'TABLE SPOON',
            'TABLE SPOONS',
            'TABLE-SPOON',
            'TABLE-SPOONS',
            'TBS',
            'TBS.',
            'TBSP',
            'TBSP.'
        ]

        metric = [
            'GRAM',
            'GRAMS',
            'G',
            'G.',
            'CENTIGRAM',
            'CENTIGRAMS',
            'CG',
            'CG.',
            'MILLIGRAM',
            'MILLIGRAMS',
            'MG',
            'MG.',
            'KILOGRAM',
            'KILOGRAMS',
            'KG',
            'KG.',
            'LITER',
            'LITERS',
            'L',
            'L.',
            'CENTILITER',
            'CENTILITERS',
            'CL',
            'CL.',
            'MILLILITER',
            'MILLILITERS',
            'ML',
            'ML.',
            'KILOLITER',
            'KILOLITERS',
            'KL',
            'KL.'
        ]

        approximate = [
            'DASH',
            'DASHES',
            'SPRIG',
            'SPRIGS',
            'LEAF',
            'LEAVES',
            'DROP',
            'DROPS',
            'BARSPOON',
            'BARSPOONS',
            'BAR SPOON',
            'BAR SPOONS',
            'BAR-SPOON',
            'BAR-SPOONS',
            'SPOON',
            'SPOONS',
            'SLICE',
            'SLICES',
            'WHEEL',
            'WHEELS',
            'WHOLE',
            'CHUNK',
            'CHUNKS',
            'BLOCK',
            'BLOCKS',
            'PIECE',
            'PIECES',
            'BEAN',
            'BEANS',
            'WEDGE',
            'WEDGES',
            'STICK',
            'STICKS',
            'SPLASH',
            'SPLASHES',
            'PINCH',
            'PINCHES',
            'TOPUP',
            'TOP UP',
            'TOP-UP',
            'TOP WITH',
            'TOP-WITH'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for units of measure.
            """
            return (
                Patterns.Units.imperial +
                Patterns.Units.metric +
                Patterns.Units.approximate
            )

        def default():
            """
            Description
            ---------------------------------------------------------------------
            Returns the default Unit value
            """
            return 'Oz'

    class Ingredients():

        ingredients = [
            r'[A-Za-z\d ]+',
            r'[A-Za-z\d ]+\.'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for ingredients.
            """
            return Patterns.Ingredients.ingredients

    class Fruits():

        fruit = [
            'APPLE',
            'APPLES',
            'BANANA',
            'BANANAS',
            'ORANGE',
            'ORANGES',
            'LEMON',
            'LEMONS',
            'LIME',
            'LIMES',
            'STRAWBERRY',
            'STRAWBERRIES',
            'BLUEBERRY',
            'BLUEBERRIES',
            'RASPBERRY',
            'RASPBERRIES',
            'CHERRY',
            'CHERRIES',
            'GRAPE',
            'GRAPES',
            'PEACH',
            'PEACHES',
            'PLUM',
            'PLUMS',
            'KIWI',
            'KIWIS',
            'MANGO',
            'MANGOS',
            'MANGOES',
            'PINEAPPLE',
            'PINEAPPLES',
            'WATERMELON',
            'WATERMELONS',
            'CANTALOUPE',
            'CANTALOUPES',
            'PAPAYA',
            'PAPAYAS',
            'POMEGRANATE',
            'POMEGRANATES',
            'GRAPEFRUIT',
            'GRAPEFRUITS',
            'AVOCADO',
            'AVOCADOS',
            'FIG',
            'FIGS',
            'PASSION FRUIT',
            'PASSION FRUITS',
            'CRANBERRY',
            'CRANBERRIES',
            'APRICOT',
            'APRICOTS',
            'BLACKBERRY',
            'BLACKBERRIES',
            'NECTARINE',
            'NECTARINES',
            'LEMON SLICE',
            'LEMON SLICES',
            'LIME SLICE',
            'LIME SLICES'
        ]

        juice = [
            'APPLE JUICE',
            'ORANGE JUICE',
            'LEMON JUICE',
            'LIME JUICE',
            'STRAWBERRY JUICE',
            'BLUEBERRY JUICE',
            'RASPBERRY JUICE',
            'CHERRY JUICE',
            'GRAPE JUICE',
            'PEACH JUICE',
            'PLUM JUICE',
            'KIWI JUICE',
            'MANGO JUICE',
            'PINEAPPLE JUICE',
            'WATERMELON JUICE',
            'CANTALOUPE JUICE',
            'PAPAYA JUICE',
            'POMEGRANATE JUICE',
            'GRAPEFRUIT JUICE',
            'AVOCADO JUICE',
            'FIG JUICE',
            'PASSION FRUIT JUICE',
            'CRANBERRY JUICE',
            'APRICOT JUICE',
            'BLACKBERRY JUICE',
            'NECTARINE JUICE'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for fruits.
            """
            return Patterns.Fruits.fruit + Patterns.Fruits.juice

    class Garnishes():

        ingredients = [
            r'GARNISH [A-Za-z0-9 ]+',
            r'GARNISH [A-Za-z0-9 ]+\.',
            r'[A-Za-z0-9 ]+ GARNISH',
            r'[A-Za-z0-9 ]+ GARNISH\.'
        ]

        as_instruction = [
            r'^GARNISH WITH ',
            r'^GARNSIH WITH ',
            r'^FINISH WITH ',
            r'^SPRITZ WITH ',
            r'^EXPRESS WITH ',
            r'^EXPRESS ',
            r'^AND SPRINKLE '
        ]

        as_phrase = [
            r' TO GARNISH$',
            r'^TOP WITH ',
            r'^TOP OFF WITH',
            r'^TOP UP WITH',
            r' GARNISH$',
            r' GARNISH\.$'
        ]

        filtr = [
            r'OVER THE DRINK BEFORE SERVING',
            r'ON TOP',
            r'THE',
            r'A',
            r'AN'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for garnishes.
            """
            return (
                Patterns.Garnishes.ingredients +
                Patterns.Garnishes.as_instruction +
                Patterns.Garnishes.as_phrase
            )

        def default():
            """
            Description
            ---------------------------------------------------------------------
            Returns the default garnish value.
            """
            return None

    class Glasses():
        """
        Description
        ---------------------------------------------------------------------
        Order-dependent. The first match is returned.
        """

        cocktail = [
            'MARTINI',
            'CHAMPAIGNE GLASS',
            'CHAMPAIGNE FLUTE',
            'COUPE GLASS',
            'WINE GLASS',
            'COPPER MUG',
            'MULE',
            'MULE MUG',
            'MOSKOW MULE MUG',
            'GLASS MUG',
            'GOBLET',
            'FIZZIO',
            'HIGHBALL',
            'HURRICANE',
            'MINT JULEP',
            'LOWBALL',
            'MARGARITA',
            'NICK AND NORA',
            'SHOT',
            'TIKI',
            'COLLINS',
            'COLINS',
            'IRISH COFFEE',
            'PUNCH BOWL',
            'GLENCAIRN',
            'GLENCAIRN WHISKEY',
            'GLENCAIRN WHISKY',
            'ROCKS',
            'POCO GRANDE',
            'PARFAIT',
            'ZOMBIE',
            'OLD FASHIONED GLASS',
            'JULEP',
            'MASON JAR',

            # Add glasses that can be ingredients last
            'CHAMPAGNE',
            'BRANDY',
            'ABSINTHE GLASS',
            'WINE',
            'SOUR',
            'PUNCH'
        ]

        beer = [
            'PILSNER',
            'PINT',
            'STEIN',
            'BEER STEIN',
            'WEIZEN',
            'TULIP'
        ]

        general = [
            'COUPE',
            'SNIFTER',
            'MUG',
            'FLUTE',
            'COCKTAIL'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for glasses.
            """
            return (
                Patterns.Glasses.cocktail +
                Patterns.Glasses.beer +
                Patterns.Glasses.general
            )

        def default():
            """
            Description
            ---------------------------------------------------------------------
            Returns the default glass value.
            """
            return None

    class Methods():
        """
        Description
        ---------------------------------------------------------------------
        Order-dependent. The first match is returned.
        """

        method = [
            'SHAKE',
            'SHAKEN',
            'STIR',
            'STIRRED',
            'BUILD',
            'BUILT',
            'BLEND',
            'BLENDED',
            'MUDDLE',
            'MUDDLED',
            'LAYER',
            'LAYERED'
        ]

        def all():
            """
            Description
            ---------------------------------------------------------------------
            Returns all regex-patterns for methods.
            """
            return Patterns.Methods.method

        def default():
            """
            Description
            ---------------------------------------------------------------------
            Returns the default method value.
            """
            return None
