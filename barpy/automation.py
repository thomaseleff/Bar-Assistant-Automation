"""
Information
---------------------------------------------------------------------
Name        : automation.py
Location    : ~/barpy/
Author      : Tom Eleff
Published   : 2023-09-30
Revised on  : ~

Description
---------------------------------------------------------------------
Contains a python wrapper class for the bar-assistant API.
"""

# Import modules
import requests
import urllib.parse as up


# Define the Barkeeper Class
class Barkeeper():

    def __init__(
        self,
        api,
        username,
        password
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        Initializes the session using user-credentials.
        """

        # Initialize session parameters
        self.api = api
        self.username = username
        self.password = password

        # Initialize session
        self.workday = requests.Session()
        self.workday.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.token = self.request_session_token()

    def __repr__(self):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        Returns the attributes of the Barkeeper Class as a <str>.
        """

        return "    api      : %s,\n    username : %s,\n    password : %s" % (
            self.api,
            self.username[:4] + '*' * (len(self.username)-4),
            self.password[:4] + '*' * (len(self.password)-4)
        )

    def request_session_token(
        self,
        operation='login'
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        Authenticates the session and returns a user-token.
        """

        # Request authentication token
        token = self.workday.post(
            up.urljoin(self.api, operation),
            json={
                'email': self.username,
                'password': self.password
            }
        ).json()['token']

        # Update session
        self.workday.headers.update(
            {'Authorization': 'Bearer %s' % (token)}
        )

        return token

    def clock_out(
        self,
        operation='logout'
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        Logs out the currently authenticated user.
        """

        # Request authentication token
        self.workday.post(
            up.urljoin(self.api, operation),
        )

    def create_cocktail(
        self,
        json,
        operation='cocktails'
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        <>
        """

        self.workday.post(
            up.urljoin(self.api, operation),
            json=json
        )

    def create_ingredient(
        self,
        json,
        operation='ingredients'
    ):
        """
        Variables
        ---------------------------------------------------------------------
        <>                      = <str>

        Description
        ---------------------------------------------------------------------
        <>
        """

        self.workday.post(
            up.urljoin(self.api, operation),
            json=json
        )
