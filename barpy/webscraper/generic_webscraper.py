"""
Information
---------------------------------------------------------------------
Name        : generic_webscraper.py
Location    : ~/barpy/webscraper/
Author      : Tom Eleff
Published   : 2023-10-23
Revised on  : ~

Description
---------------------------------------------------------------------
Contains the generic web-scraper class.
"""

import re
import unicodedata
import numpy as np
import nltk
# import wordtodigits as w2d
# from text_to_num import alpha2digit as a2d
from fractions import Fraction


# Define the Generic Webscraper class
class GenericWebscraper(object):

    class Collection():

        def __init__(
            self,
            name=None,
            description=None,
            cocktails=[]
        ):
            """
            Variables
            ---------------------------------------------------------------------
            name                    = <str> Name of the cocktail collection
            description             = <str> Description of the cocktail
                                        collection
            cocktails               = <list> List object of cocktail
                                        class objects

            Description
            ---------------------------------------------------------------------
            Initializes an instance of the Collection class.
            """

            self.name = name
            self.description = description
            self.cocktails = cocktails

        def __repr__(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Collection class as a <str>.
            """

            return (
                "%s <class>" +
                "\n    %s: %s," +
                "\n    %s: %s," +
                "\n    %s: %s"
            ) % (
                'Collection',
                'Name',
                self.name,
                'Description',
                self.description,
                'Num. Cocktails',
                len(self.cocktails)
            )

        def to_dict(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Collection class as a <dictionary>.
            """

            return self.__dict__

    class Cocktail():

        def __init__(
            self,
            name=None,
            source=None,
            instructions=None,
            garnish=None,
            description=None,
            tags=[],
            glass=None,
            method=None,
            images=[],
            ingredients=[]
        ):
            """
            Variables
            ---------------------------------------------------------------------
            name                    = <str> Name of the cocktail
            source                  = <str> URL web-address to the cocktail
                                        recipe web-page
            instructions            = <str> Cocktail recipe instructions
            garnish                 = <str> Cocktail garnish
            description             = <str> Cocktail recipe description
            tags                    = <list> List object of cocktail recipe
                                        tags
            glass                   = <str> Name of the cocktail glass
            method                  = <str> Name of the cocktail method
            images                  = <list> List object of cocktail Image
                                        class objects
            ingredients             = <list> List object of cocktail ingredient
                                        class objects

            Description
            ---------------------------------------------------------------------
            Initializes an instance of the Cocktail class.
            """

            self.name = name
            self.source = source
            self.instructions = instructions
            self.garnish = garnish
            self.description = description
            self.tags = tags
            self.glass = glass
            self.method = method
            self.images = images
            self.ingredients = ingredients

        def __repr__(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Cocktail class as a <str>.
            """

            return (
                "%s <class>" +
                "\n    %s: %s," +
                "\n    %s: %s," +
                "\n    %s: %s," +
                "\n    %s: %s"
            ) % (
                'Cocktail',
                'Name',
                self.name,
                'Source',
                self.source,
                'Description',
                self.description,
                'Num. Ingredients',
                len(self.ingredients)
            )

        def to_dict(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Cocktail class as a <dictionary>.
            """

            return self.__dict__

    class Ingredient():

        def __init__(
            self,
            sort=None,
            name=None,
            amount=None,
            units=None,
            category=None,
            description=None,
            strength=None,
            origin=None,
            substitutes=[],
            optional=False
        ):
            """
            Variables
            ---------------------------------------------------------------------
            sort                    = <int> Unique sort id
            name                    = <str> Name of the ingredient
            amount                  = <float> Amount of the ingredient
            units                   = <str> Unit of measure of the ingredient
            category                = <str> Ingredient category
            description             = <str> Ingredient description
            strength                = <float> Ingredient ABV percentage
            origin                  = <str> Ingredient country of origin
            substitutes             = <list> List object of alternative
                                        ingredient names
            optional                = <bool> Identifyer for whether the
                                        ingredient is required

            Description
            ---------------------------------------------------------------------
            Initializes an instance of the Ingredient class.
            """

            self.sort = sort
            self.name = name
            self.amount = amount
            self.units = units
            self.category = category
            self.description = description
            self.strength = strength
            self.origin = origin
            self.substitutes = substitutes
            self.optional = optional

        def __repr__(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Ingredient class as a <str>.
            """

            return (
                "%s <class>" +
                "\n    %s: %s," +
                "\n    %s: %s," +
                "\n    %s: %s," +
                "\n    %s: %s"
            ) % (
                'Ingredient',
                'Name',
                self.name,
                'Amount',
                self.amount,
                'Unit',
                self.units,
                'Description',
                self.description
            )

        def to_dict(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Ingredient class as a <dictionary>.
            """

            return self.__dict__

    class Image():

        def __init__(
            self,
            url=None,
            copyright=None,
            sort=0
        ):
            """
            Variables
            ---------------------------------------------------------------------
            url                     = <str> URL web-address to the cocktail
                                        recipe image
            copyright               = <str> Copyright of the image
            sort                    = <int> Unique sort id

            Description
            ---------------------------------------------------------------------
            Initializes an instance of the Image class.
            """

            self.url = url
            self.copyright = copyright
            self.sort = sort

        def __repr__(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Image class as a <str>.
            """

            return (
                "%s <class>" +
                "\n    %s: %s," +
                "\n    %s: %s,"
            ) % (
                'Image',
                'Source',
                self.url,
                'Copyright',
                self.copyright
            )

        def to_dict(self):
            """
            Description
            ---------------------------------------------------------------------
            Returns the attributes of the Image class as a <dictionary>.
            """

            return self.__dict__

    # Recipe parsing function(s)
    def split_lines(
        self,
        text,
        filtr=False
    ):
        """
        Variables
        ---------------------------------------------------------------------
        text                    = <str> Recipe text converted from the HTML
                                    request
        filtr                   = <list> List of strings, where if found in
                                    any line of the {recipe}, remove that
                                    line from the {recipe}.

        Description
        ---------------------------------------------------------------------
        Applies cleansing to the {recipe} text and converts it to a list of
        ingredients and instructions.
        """

        # Cleanse recipe text and split-lines
        lst = self.cleanse_cocktail_recipe(s=text).split('|')

        # Cleanse recipe split-lines
        lst = self.cleanse_html_tags_from_list(lst=lst)
        lst = self.cleanse_leading_and_trailing_from_list(lst=lst)
        lst = self.cleanse_empty_lines_from_list(lst=lst)

        # Filter recipe split-lines
        if filtr:
            lst = self.filter_unwanted_phrases(lst=lst, filtr=filtr)

        return lst

    # Recipe cleansing function(s)
    def cleanse_cocktail_recipe(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to cleanse

        Description
        ---------------------------------------------------------------------
        Normalizes {s} to ASCII characters and cleanses it of unwanted
        characters, line breaks and written numbers, e.g., "two".
        """

        # Normalize unicode
        s = self.normalize_unicode(s=s)

        # Cleanse non-standard characters
        s = self.cleanse_ampersand(s=s)
        s = self.cleanse_empty_strings(s=s)

        # Cleanse html tag elements
        s = self.cleanse_line_break(s=s)

        # Convert written numbers, 'two', to digits, '2'
        # s = self.convert_written_numbers(s=s)

        return s

    # String cleansing function(s)
    def normalize_unicode(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to normalize

        Description
        ---------------------------------------------------------------------
        Normalizes {s} to ASCII characters.
        """

        return unicodedata.normalize(
            'NFKD',
            str(s)
        ).replace('⁄', '/').encode(
            'latin-1',
            'ignore'
        ).decode('utf-8')

    def cleanse_ampersand(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses {s} of ampersand characters.
        """

        return re.sub('&amp;|&', 'and', str(s))

    def cleanse_empty_strings(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses {s} of empty string characters.
        """

        return re.sub('\xa0', ' ', str(s))

    def cleanse_line_break(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to cleanse

        Description
        ---------------------------------------------------------------------
        Converts end-of-line breaks to standard characters.
        """

        return re.sub(
            '\n|<br([A-Za-z0-9 -=\"\'/]|)+>',
            '|',
            str(s)
        )

    # Ingredient cleansing function(s)
    # def convert_written_numbers(self, s):
    #     """
    #     Variables
    #     ---------------------------------------------------------------------
    #     s                       = <str> String to convert

    #     Description
    #     ---------------------------------------------------------------------
    #     Converts written numbers, e.g., 'two', within {s} to digits, e.g., 2.
    #     """

    #     numbers = w2d.convert(s)
    #     ordinals = a2d(text=s, lang="en")

    #     if re.sub(r'[^\d]+', '', numbers):
    #         return numbers
    #     else:
    #         if re.sub(r'[^\d]+', '', ordinals):
    #             return ordinals
    #         else:
    #             return str(s)

    def convert_amount_to_numeric(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to convert

        Description
        ---------------------------------------------------------------------
        Converts {s}, as either ranges or fractions, e.g., '1-2' or '1/2', to
        float, e.g., 2 or 1.5.
        """

        # Convert to float
        if s:
            # For ranges, take the average then round-up
            if ('-' in str(s)) or ('TO' in str(s).strip().upper()):
                s = np.ceil(
                    np.mean(
                        [
                            float(
                                num
                            ) for num in str(s).replace(
                                ' ',
                                ''
                            ).split('-')
                        ]
                    )
                )

            # Otherwise, treat values as fractions
            else:
                try:
                    if ' ' in str(s).replace(' / ', '/'):
                        s = sum(Fraction(d) for d in str(s).split())
                    else:
                        s = Fraction(str(s))
                except ValueError:
                    s = s

            return float(s)

        # Otherwise, return a default
        else:
            return float(1)

    def cleanse_leading_and_trailing_period(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses {s} of any leading or trailing periods.
        """

        return re.sub(r'((^\.)|(\.$))', '', str(s).strip()).strip()

    # List comprehension function(s)
    def cleanse_html_tags_from_list(self, lst):
        """
        Variables
        ---------------------------------------------------------------------
        lst                     = <list> List to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses each item in {lst} of any HTML content tags.
        """

        return [re.sub('<[^>]*>', '', str(s)) for s in lst]

    def cleanse_leading_and_trailing_from_list(self, lst):
        """
        Variables
        ---------------------------------------------------------------------
        lst                     = <list> List to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses each item in {lst} of any leading or trailing spaces.
        """

        return [str(s).strip() for s in lst]

    def cleanse_empty_lines_from_list(self, lst):
        """
        Variables
        ---------------------------------------------------------------------
        lst                     = <list> List to cleanse

        Description
        ---------------------------------------------------------------------
        Cleanses each item in {lst} of any empty items.
        """

        return [line for line in lst if line]

    def filter_unwanted_phrases(self, lst, filtr):
        """
        Variables
        ---------------------------------------------------------------------
        lst                     = <list> List to filter
        filtr                   = <list> List of strings, where if found in
                                    any item of {lst}, remove the item from
                                    {lst}.

        Description
        ---------------------------------------------------------------------
        Filters out any item in {list} that contains any string in {filter}.
        """

        return [
            line for line in lst if not re.match(
                ''.join([
                    r'^',
                    r'(%s)' % (
                        '|'.join(
                            filtr
                        )
                    ),
                    r'$'
                ]),
                string=line,
                flags=re.IGNORECASE
            )
        ]

    # Text formatting function(s)
    def title_case(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to format

        Description
        ---------------------------------------------------------------------
        Converts {s} to title-case.
        """

        if s:
            return ' '.join(
                [word.capitalize() for word in nltk.tokenize.TweetTokenizer(
                ).tokenize(s)]
            ).replace(
                ' .',
                '.'
            ).replace(
                ' :',
                ':'
            ).replace(
                '( ',
                '('
            ).replace(
                ' )',
                ')'
            ).replace(
                " ' ",
                "'"
            ).replace(
                " '",
                "'"
            )
        else:
            return None

    def proper_case(self, s):
        """
        Variables
        ---------------------------------------------------------------------
        s                       = <str> String to format

        Description
        ---------------------------------------------------------------------
        Converts {s} to proper sentence-case.
        """

        if s:
            return ' '.join(
                [sentence.capitalize() for sentence in nltk.sent_tokenize(s)]
            )
        else:
            return None
