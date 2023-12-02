"""
Information
---------------------------------------------------------------------
Name        : readme.py
Location    : ~/barpy/
Author      : Tom Eleff
Published   : 2023-10-16
Revised on  : 2023-12-02

Description
---------------------------------------------------------------------
Contains the readme class to generate markdown documents from the set
of cocktail collections for a bar.
"""

import os
import barpy.utils as utils


# Define the Readme Write Class
class Write():

    def __init__(
        self,
        rmLoc
    ):

        """
        Variables
        ---------------------------------------------------------------------
        rmLoc                   = <str> Folder path to output the markdown
                                    bar menu document.

        Description
        ---------------------------------------------------------------------
        Initializes an instance of the Readme class.
        """

        self.rmLoc = rmLoc

    # Readme function(s)
    def write(
        self
    ):
        """
        Description
        ---------------------------------------------------------------------
        Writes a markdown document from the set of cocktail collections for a
        bar.
        """

        # Manage files
        self.manage_readme()

        # Import bar metadata
        metadata = utils.read_config(
            configLoc=os.path.join(
                self.rmLoc,
                'metadata.json'
            )
        )['metadata']

        # Write bar header
        self.write_line(
            string='# %s\n' % (metadata['name'])
        )
        self.write_line(string='- Address: %s\n' % (
            ', '.join([
                metadata['address'],
                metadata['city'],
                metadata['stateCode']
            ])
        ))
        self.write_line(string='- Source: (%s)\n' % (
            metadata['url']
        ))
        self.write_line(string='\n')

        # Write collection navigation
        self.write_line(
            string='## %s\n' % ('Cocktail Collections')
        )
        self.write_line(string='\n')
        for file in [collection for collection in os.listdir(
            os.path.join(
                self.rmLoc,
                'db'
            )
        ) if collection.split('.')[-1].strip().upper() == 'JSON']:

            config = utils.read_config(
                configLoc=os.path.join(
                    self.rmLoc,
                    'db',
                    file
                )
            )

            # Write collection navigation
            self.write_line(
                string='- [%s](#%s)\n' % (
                    config['name'],
                    config['name'].replace(' ', '-').lower()
                )
            )
        self.write_line(string='\n')

        # Write collection
        for file in [collection for collection in os.listdir(
            os.path.join(
                self.rmLoc,
                'db'
            )
        ) if collection.split('.')[-1].strip().upper() == 'JSON']:

            config = utils.read_config(
                configLoc=os.path.join(
                    self.rmLoc,
                    'db',
                    file
                )
            )

            # Write collection header
            self.write_line(
                string='## %s\n' % (config['name'])
            )
            self.write_line(string='\n')

            # Write cocktails
            for cocktail in config['cocktails']:
                self.write_line(
                    string='### %s\n' % (cocktail['name'])
                )
                self.write_line(string='\n')
                self.write_line(
                    string='- Source: (%s)\n' % (
                        cocktail['source']
                    )
                )
                self.write_line(string='\n')
                self.write_line(string='![%s](%s)\n' % (
                    cocktail['images'][0]['copyright'],
                    cocktail['images'][0]['url']
                ))
                self.write_line(string='\n')
                self.write_line(string='Ingredients:\n')
                self.write_line(string='\n')
                for i in cocktail['ingredients']:
                    self.write_line(
                        string='- %s %s %s\n' % (
                            i['amount'],
                            i['units'],
                            i['name']
                        )
                    )
                self.write_line(string='\n')
                if cocktail['garnish']:
                    self.write_line(string='Garnish:\n')
                    self.write_line(string='\n')
                    self.write_line(string='- %s\n' % (cocktail['garnish']))
                    self.write_line(string='\n')
                if cocktail['glass']:
                    self.write_line(string='Glass:\n')
                    self.write_line(string='\n')
                    self.write_line(string='- %s\n' % (cocktail['glass']))
                    self.write_line(string='\n')
                if cocktail['method']:
                    self.write_line(string='Method:\n')
                    self.write_line(string='\n')
                    self.write_line(string='- %s\n' % (cocktail['method']))
                    self.write_line(string='\n')
                if cocktail['instructions']:
                    self.write_line(string='Instructions:\n')
                    self.write_line(string='\n')
                    for instruction in cocktail['instructions'].split('\n\n'):
                        self.write_line(string='%s  \n' % (instruction))
                    self.write_line(string='\n')
                self.write_line(string='%s\n' % ('-' * 3))
                self.write_line(string='\n')

    def manage_readme(
        self
    ):
        """
        Description
        ---------------------------------------------------------------------
        Removes the markdown menu if it exists within {self.rmLoc}.
        """

        if os.path.exists(
            os.path.join(
                self.rmLoc,
                'README.md'
            )
        ):
            os.remove(
                os.path.join(
                    self.rmLoc,
                    'README.md'
                )
            )

    def write_line(
        self,
        string
    ):
        """
        Variables
        ---------------------------------------------------------------------
        string                  = <str> String to write to the markdown menu
                                    bar document.

        Description
        ---------------------------------------------------------------------
        Writes {string} to the markdown menu in {self.rmLoc}.
        """

        with open(
            os.path.join(
                self.rmLoc,
                'README.md'
            ),
            '+a'
        ) as file:
            file.write(string)
