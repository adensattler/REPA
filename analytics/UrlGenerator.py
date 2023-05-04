import urllib.parse

bounds = {"west":{"CO": -105.109837,
                  "CA": -118.668176},
          "east":{"CO": -104.599735,
                  "CA": -118.155487},
          "south":{"CO": 39.613671,
                   "CA": 33.704902},
          "north":{"CO": 40.094666,
                   "CA": 34.332796}
          }

def url_encoder(structure):
    return urllib.parse.quote(structure)

def url_generator(city, state, max_bedrooms=5, tow=False):

    structure = f'''{{"pagination":{{}},"usersSearchTerm":"{city}, {state}","mapBounds":{{"west":{bounds['west'][state]},"east":{bounds['east'][state]},"south":{bounds['south'][state]},"north":{bounds['north'][state]}}},"regionSelection":[],"isMapVisible":true,"filterState":{{"price":{{}},"mp":{{}},"beds":{{"max":{max_bedrooms}}},"built":{{}},"doz":{{}},"sort":{{"value":"globalrelevanceex"}},"ah":{{"value":true}},"con":{{"value":false}},"mf":{{"value":false}},"manu":{{"value":false}},"land":{{"value":false}},"tow":{{"value":false}},"apa":{{"value":false}},"apco":{{"value":false}}}},"isListVisible":true}}'''

    encoded_url = url_encoder(structure)
    return f"https://www.zillow.com/{city.lower()}-{state.lower()}/houses/?searchQueryState={encoded_url}"
