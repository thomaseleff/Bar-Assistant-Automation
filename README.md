# Bar Assistant Automation
Automating the [bar-assistant](https://github.com/karlomikus/bar-assistant) API requests for cocktail recipes and ingredients through Python.

## Components
Included in this repository,

- ```BarPy``` Python wrapper-library for the Bar Assistant API
- ```community``` Archive collection of cocktail recipes and ingredients web-scraped from notable US bars

## BarPy
Python wrapper-library for the Bar Assistant API.

### Getting Started
1. Clone the ```main``` branch of this repository to your local machine (see [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository), **Cloning a repository**).
2. Within the root directory, create a ```.env``` file with the following contents,

    ```Shell
    # Define bar-assistant application & authentication parameters
    BARPY_API='{bar_assistant_api_url_address}'
    BARPY_USERNAME='{bar_assistant_username}'
    BARPY_PASSWORD='{bar_assistant_password}'
    ```

    For example, ```.env``` would be configured as the following for the demo [API](https://bar.karlomikus.com/bar/docs) from bar-assistant,

    ```Shell
    # Define bar-assistant application & authentication parameters
    BARPY_API='https://bar.karlomikus.com/bar/api/'
    BARPY_USERNAME='admin@example.com'
    BARPY_PASSWORD='password'
    ```

3. Run ```main.py``` within the root directory to upload the example cocktail recipe and ingredient to your Bar Assistant DB.

    ```PowerShell
    python3 main.py
    ```

## Community
The community archive collection includes cocktail recipes and ingredients from notable US bars indexed by date. The following bar archive collections are available,

- [High West Saloon](community/high-west-saloon/) (Park City, UT)
- The Dead Rabbit (New York City, NY)
- The Violet Hour (Chicago, IL)
- Bar Leather Apron (Honolulu, HI)
- Jewel of the South (New Orleans, LA)