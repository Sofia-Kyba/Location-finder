import folium
import ssl
import certifi
import geopy
import geopy.distance
import string

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)


def check(year_input, coordinates_input):
    """
    (str, str) -> bool
    Check whether user wrote right coordinates.
    """
    if type(coordinates_input) != str:
        return 'Error'
    if '.' not in year_input or '.' not in coordinates_input:
        return 'Error.'
    if len(year_input < 6):
        return 'Missing lat or long'
    return True


def read_file(file_name):
    """
    str -> list
    Read the file, cut unnecessary information,
    replace unnecessary information in lists and return list of lists.
    """
    with open(file_name, 'r', encoding="latin1") as file:
        locations = []
        for line in file:
            locations += [line.strip().split('\t')]
        cut_locations = locations[14:]
        result_lst = set()
        for element in range(len(cut_locations)):
            if '{' in cut_locations[element][0]:
                cut_locations[element][0] = cut_locations[element][0][:cut_locations[element][0].index('{')]
            if '(' in cut_locations[element][-1]:
                result_lst.add((cut_locations[element][0], cut_locations[element][-2]))
            else:
                result_lst.add((cut_locations[element][0], cut_locations[element][-1]))
        result = []
        for element in result_lst:
            result.append(list(element))
        return result


def define_needed_locations(needed_year):
    """
    (str, list) -> list
    Choose only that lists, which include the year
    that was written by user, and return new list.
    >>> define_needed_locations(2002, [['"$2 Bill" (2002) ', 'Los Angeles, California, USA'],
    ['"$2 Donuts" (2017)', 'Sydney, Australia']])
    [['"$2 Bill" (2002) ', 'Los Angeles, California, USA']]
    """
    lst = read_file('locations.list.txt')
    needed_locations = []
    for i in range(0, len(lst)):
        for j in range(0, len(lst[i])):
            if str(needed_year) in lst[i][j] and '(' not in lst[i][1]:
                needed_locations.append([lst[i][0], lst[i][1]])
    return needed_locations


def define_location_of_user(coordinates_input):
    """
    (str, str) -> tuple
    Define location of user by written coordinates and return it.
    >>> define_location_of_user('45.017545, 25.921232')
    Romania
    >>> define_location_of_user('50.017545, 5.921232')
    Luxembourg
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    loc = coordinates_input
    geolocator = Nominatim(user_agent="app_name",
                           timeout=10)
    location = geolocator.reverse(loc, language="en")
    if location.address is None:
        return "Write another coordinates"
    else:
        loc_list = location.address.split(',')
        needed_location = loc_list[-1][1:]
        if needed_location == 'United States of America':
            needed_location = "USA"
        elif needed_location == "United Kingdom":
            needed_location = 'UK'
        return needed_location


def country_locations(needed_year, coordinates_input):
    """
    (str, str) -> list
    Define the user's loсation by written coordinates and return list of lists
    with the films, that where filmed on that location.
    """
    lst = define_needed_locations(needed_year)
    needed_country = define_location_of_user(coordinates_input)

    new_lst = []
    for element in range(len(lst)):
        if needed_country in lst[element][1]:
            new_lst.append([lst[element][0], lst[element][1]])
    return new_lst


def define_coordinates(needed_year, coordinates_input):
    """
    (str, str) -> dict
    Define coordinates of locations in needed country and return dict
    with name of film as a keys and list of coordinates as an item
    """
    lst = country_locations(needed_year, coordinates_input)
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    for element in range(len(lst)):
        geolocator = Nominatim(user_agent="app_name",
                               timeout=10)
        location = geolocator.geocode(lst[element][1])
        try:
            lat_long = [location.latitude, location.longitude]
            lst[element][1] = lat_long
            lst[element] = tuple(lst[element])
        except:
            continue
    dictionary = dict(lst)
    return dictionary


def define_closest_films(needed_year, coordinates_input):
    """
    (str, str) -> list
    Define closest to the needed location films, sort them and choose ten of them.
    """
    locations = define_coordinates(needed_year, coordinates_input)
    coordinates = coordinates_input.split(',')
    lat = float(coordinates[0])
    long = float(coordinates[1])
    coords_1 = (lat, long)  # coordinates of user

    new_locations = []
    for element in locations:
        try:
            if type(locations[element]) == list:
                coords_2 = (locations[element][0], locations[element][1])  # coordinates of locations
                distance = geopy.distance.distance(coords_1, coords_2).km
                tup = (element, distance)
                if type(tup[1]) != str:
                    new_locations.append(tup)
        except:
            continue
    dict_locs = dict(new_locations)
    sorted_lst = sorted(dict_locs.items(), key=lambda x: x[1])
    result_lst = sorted_lst[:10]
    films = []
    for el in result_lst:
        el = list(el)
        films.append(el[0])

    all_information = []
    for film in films:
        for loc in locations:
            if film == loc:
                lat = locations[loc][0]
                long = locations[loc][1]
                all_information.append([film, lat, long])
    return all_information


def define_coordinates_of_cities(lst):
    """
    list -> list
    Define coordinates of cities and return list with them.
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    coordinates = []
    latitude = []
    longitude = []
    for element in range(len(lst)):
        geolocator = Nominatim(user_agent="app_name",
                               timeout=10)
        location = geolocator.geocode(lst[element])
        try:
            latitude.append(location.latitude)
            longitude.append(location.longitude)
        except:
            continue
    coordinates.append(latitude)
    coordinates.append(longitude)
    return coordinates


def generate_map(needed_year, coordinates_input):
    """
    (str, str) -> None
    Generate map, which include several layers with needed information.
    """
    location = coordinates_input.split(',')
    lat = float(location[0])
    long = float(location[1])
    map = folium.Map(titles='World Map', location=[lat, long], zoom_start=8)
    map.add_child(folium.Marker(location=(lat, long),
                                      popup="My location",
                                      fill_color='blue',
                                      color='brown',
                                      icon=folium.Icon()))

    all_films = []
    all_lat = []
    all_long = []
    needed_information = define_closest_films(needed_year, coordinates_input)
    for element in needed_information:
        all_films.append(element[0])
        all_lat.append(element[1])
        all_long.append(element[2])

    feat_movies = folium.FeatureGroup(name="Movies")
    for lt, ln, film in zip(all_lat, all_long, all_films):
        feat_movies.add_child(folium.Marker(location=[lt, ln],
                                            popup=film,
                                            icon=folium.Icon()))

    biggest_cities = ['Berlin', 'Madrid', 'Rome', 'Paris', 'Bucharest']
    coordinates = define_coordinates_of_cities(biggest_cities)
    lat_ = coordinates[0]
    long_ = coordinates[1]

    feat_cities = folium.FeatureGroup(name="Biggest cities of Europe")
    for lt_, ln_, hill in zip(lat_, long_, biggest_cities):
        feat_cities.add_child(folium.CircleMarker(location=[lt_, ln_],
                                            popup=hill,
                                            fill_color='yellow',
                                            color='red',
                                            icon=folium.Icon()))

    map.add_child(feat_movies)
    map.add_child(feat_cities)
    map.add_child(folium.LayerControl())
    map.save('Map_1.html')


if __name__ == '__main__':
    year = input('Please enter a year you would like to have a map for: ')
    coordinates = input('Please enter your location (format: lat, long): ')
    if check(year, coordinates):
        print("Map is generating...\nPlease wait...")
        generate_map(year, coordinates)
        print("Finished. Please have look on the map Map_1.html")
    else:
        print(check(year, coordinates))

