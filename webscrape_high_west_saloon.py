"""
Information
---------------------------------------------------------------------
Name        : webscrape_high_west_saloon.py
Location    : ~/
Author      : Tom Eleff
Published   : 2023-10-23
Revised on  : 2023-12-02

Description
---------------------------------------------------------------------
Webscrapes the cocktail recipes from the High West Saloon and
generates the High West Saloon bar menu.
"""

import os
from barpy.webscraper import high_west_saloon as WebScraper
import barpy.utils as utils
import barpy.readme as readme


if __name__ == '__main__':

    # Initialize the High West Saloon Web-Scraper
    hws = WebScraper.HighWestSaloon(
        outPath=os.path.join(
            os.path.dirname(__file__),
            'community'
        )
    )

    # Create cocktail collection
    for category in list(hws.categories.keys()):
        collection = hws.create_cocktail_collection(
            name=str(category),
            cocktails=hws.categories[category]['path']
        )

        # Normalize collection from compliance
        # compliance.normalize(
        #     collection=collection.to_dict()
        # )

        # Output cocktail collection
        utils.write_config(
            configLoc=os.path.join(
                hws.config['outputs']['path'],
                hws.config['outputs']['root'],
                'db',
                '%s.json' % (
                    str(category).lower().replace(' ', '-')
                )
            ),
            config=collection.to_dict()
        )

        # Output to console
        print(collection)

    # Write bar menu README.md
    readme.Write(
        rmLoc=os.path.join(
            hws.config['outputs']['path'],
            hws.config['outputs']['root']
        )
    ).write()
