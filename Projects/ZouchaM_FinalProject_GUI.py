# DSC 510
# Final Programming Assignment
# Author: Michael Zoucha
# 29 March 2021

# Change #: 1
# Change Made: Added GUI with Tkinter
# Date of Change: 04 April 2021
# Author: Michael Zoucha

# Change #: 2
# Change Made: Added forecast below current conditions
# Date of Change: 15 May 2021
# Author: Michael Zoucha

# Change #: 3
# Change Made: Final formatting changes and upgrades
# Date of Change: 28 May 2021
# Author: Michael Zoucha

# Change #: 4
# Change Made: Added 24 hour forecast and forecast labels
# Date of Change: 31 May 2021
# Author: Michael Zoucha

# Change #: 5
# Change Made: Changed city name verification to JSON/pandas from API to account for API flaw
# Date of Change: 02 June 2021
# Author: Michael Zoucha


import requests
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
from io import BytesIO
import pandas as pd


# Function to test connection to API
def test_connection():

    # Test URL uses 'dummy city' to test connection
    test_url = 'https://api.openweathermap.org/data/2.5/weather?q={},us&' \
               'appid=fe52c494615582cff13acb283ee60254&units=imperial'.format('Omaha')

    # Try connection before asking for input, set label message and if unsuccessful, quit program
    try:

        requests.get(test_url)

    # If connection error occurs
    except requests.ConnectionError:

        conn_result = "Connection Status: Disconnected"
        lbl_connection = tk.Label(master=window, text=conn_result, font=('Arial', 10), bg='light blue')
        lbl_connection.grid(row=19, column=0, sticky="wsw", columnspan=8)

        # Remove search button, popup window with error message, 'OK' quits the program
        btn_search.grid_remove()
        tk.messagebox.showerror(title='Error', message="Could not connect.\n Please try again later.")
        quit()

    # If no connection error occurs
    else:

        conn_result = "Connection Status: Connected"
        lbl_connection = tk.Label(master=window, text=conn_result, font=('Arial', 10), bg='light blue')
        lbl_connection.grid(row=19, column=0, sticky="wsw", columnspan=8)

        try:

            # Build data frame to search for city names
            url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
            df_ = pd.read_json(url)

        except pd.errors:

            conn_result = "Connection Status: Disconnected"
            lbl_connection = tk.Label(master=window, text=conn_result, font=('Arial', 10), bg='light blue')
            lbl_connection.grid(row=19, column=0, sticky="wsw", columnspan=8)

            # Remove search button, popup window with error message, 'OK' quits the program
            btn_search.grid_remove()
            tk.messagebox.showerror(title='Error', message="Error loading data.\n Please try again later.")
            quit()

        return df_


# Connect to API and get data
def get_weather_data(search_type, city, state_code, zip_code):

    # Use values passed by main() to determine search method and criteria
    if search_type == 'CITY':

        # If user only searched city name
        if state_code == '':

            # Search for multiple locations with the same name in the US
            location_query = location_df.loc[(location_df['name'] == city) & (location_df['country'] == 'US'), ['id', 'name', 'state', 'country', 'coord']]

            # If only one exists, set lat longs and city name
            if len(location_query) == 1:

                # Get values from pandas series of results
                longitude = location_query.coord.str['lon'].iloc[0]
                latitude = location_query.coord.str['lat'].iloc[0]
                city = str(location_query['name'].iloc[0]).strip()
                state_code = str(location_query['state'].iloc[0]).strip()
                city_name = (city + ', ' + state_code)

            # If there are none, search again
            elif len(location_query) == 0:

                error_message.set('Location not found. Please try again or search by zip code.')
                lbl_error_message.tkraise()
                search_type = 'ERROR'

                return search_type

            # If there are more than 1, ask for the state code
            else:

                error_message.set(str(len(location_query)) + '  "' + city.title() + '" locations found. ' +
                                  'Please use "' + city.title() + ', XX" format.')
                lbl_error_message.tkraise()
                search_type = 'ERROR'

                return search_type

        else:

            # Search for multiple locations with the same name and state in the US
            location_query = location_df.loc[(location_df['name'] == city) & (location_df['state'] == state_code) & (location_df['country'] == 'US'),
                                    ['id', 'name', 'state', 'country', 'coord']]

            # If only one exists, set lat longs and city name
            if len(location_query) == 1:

                # Get values from pandas series of results
                longitude = location_query.coord.str['lon'].iloc[0]
                latitude = location_query.coord.str['lat'].iloc[0]
                city = str(location_query['name'].iloc[0]).strip()
                state_code = str(location_query['state'].iloc[0]).strip()
                city_name = (city + ', ' + state_code)

            # If none exist, search again
            else:

                error_message.set('Location not found. Please try again or search by zip code.')
                lbl_error_message.tkraise()
                search_type = 'ERROR'

                return search_type

        # Catch connection error in case internet is interrupted
        try:

            # Using latitude and longitude, fill data from 'onecall' API
            url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&' \
                  'exclude=minutely,alerts&appid=fe52c494615582cff13acb283ee60254&units=imperial' \
                .format(latitude, longitude)
            response = requests.get(url)
            weather_data = response.json()
            print_current_weather(weather_data, city_name)
            print_weather_forecast(weather_data)

        except requests.ConnectionError:

            conn_result = "Connection Status: Disconnected"
            lbl_connection = tk.Label(master=window, text=conn_result, font=('Arial', 10), bg='light blue')
            lbl_connection.grid(row=19, column=0, sticky="wsw", columnspan=8)

            # Remove search button, popup window with error message, 'OK' quits the program
            btn_search.grid_remove()
            tk.messagebox.showerror(title='Error', message="Connection Error.\n Please try again later.")
            quit()

    # Use values passed by main() to determine search method and criteria
    elif search_type == 'ZIP':

        url = 'https://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&' \
              'appid=fe52c494615582cff13acb283ee60254'.format(zip_code)
        response = requests.get(url)
        lat_long_data = response.json()

        # Ensure the location is valid
        if lat_long_data['cod'] == '404':

            error_message.set('Location not found. Please enter a valid zip code.')
            lbl_error_message.tkraise()
            search_type = 'ERROR'

            return search_type

        # Get latitude and longitude for OneCallAPI
        latitude = lat_long_data['coord']['lat']
        longitude = lat_long_data['coord']['lon']
        city_name = lat_long_data['name']

        # Catch connection error in case internet is interrupted
        try:

            # Using latitude and longitude, fill data from 'onecall' API
            url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&' \
                  'exclude=minutely,alerts&appid=fe52c494615582cff13acb283ee60254&units=imperial' \
                .format(latitude, longitude)
            response = requests.get(url)
            weather_data = response.json()
            print_current_weather(weather_data, city_name)
            print_weather_forecast(weather_data)

        except requests.ConnectionError:

            conn_result = "Connection Status: Disconnected"
            lbl_connection = tk.Label(master=window, text=conn_result, font=('Arial', 10), bg='light blue')
            lbl_connection.grid(row=19, column=0, sticky="wsw", columnspan=8)

            # Remove search button, popup window with error message, 'OK' quits the program
            btn_search.grid_remove()
            tk.messagebox.showerror(title='Error', message="Connection Error.\n Please try again later.")
            quit()

    # return search type to catch errors
    return search_type


# Fill variables from API data and print
def print_current_weather(data, city_name):

    # Assign all used variables
    weather_description = data['current']['weather'][0]['description']
    sunrise_utc_time = datetime.utcfromtimestamp(data['current']['sunrise'])
    sunset_utc_time = datetime.utcfromtimestamp(data['current']['sunset'])
    added_time = timedelta(0, int(data['timezone_offset']))
    sunrise_time = (sunrise_utc_time + added_time)
    sunset_time = (sunset_utc_time + added_time)
    current_temp = int(round(data['current']['temp'], 0))
    feels_like_temp = int(round(data['current']['feels_like'], 0))
    wind_speed = int(round(data['current']['wind_speed'], 0))
    wind_degree = data['current']['wind_deg']
    wind_direction = get_wind_direction(wind_degree)
    pressure = data['current']['pressure']
    humidity = data['current']['humidity']
    icon_id = data['current']['weather'][0]['icon']
    icon_image = get_weather_icon(icon_id)

    # Initialize file for use in message widget
    current_weather_file = io.StringIO()

    # Print all necessary information to StringIO file to be used in message widget
    print('           Current Conditions : ' + str(weather_description).title(), file=current_weather_file)
    print('       Current Temperature : ' + str(current_temp) + u"\N{DEGREE SIGN}" + "F", file=current_weather_file)
    print('"'"Feels Like"'" Temperature : ' + str(feels_like_temp) + u"\N{DEGREE SIGN}" + "F", file=current_weather_file)
    print('    Wind Speed / Direction : ' + str(wind_direction), str(wind_speed) + ' mph', file=current_weather_file)
    print('                            Humidity : ' + str(humidity) + '%', file=current_weather_file)
    print('                            Pressure : ' + str(pressure) + ' hPA', file=current_weather_file)
    print('                              Sunrise : ' + sunrise_time.strftime('%-I:%M %p'), file=current_weather_file)
    print('                               Sunset : ' + sunset_time.strftime('%-I:%M %p'), file=current_weather_file)

    # Remove initial objects from window
    lbl_city_zip.grid_remove()
    lbl_error_message.grid_remove()
    frm_entry.grid_remove()
    ent_city_zip.grid_remove()
    btn_search.grid_remove()
    lbl_space.grid_remove()

    # Title including searched city name
    title_string = 'CURRENT WEATHER CONDITIONS FOR ' + str(city_name).upper()
    title_label = tk.Label(master=frm_info, text=title_string, bg='light blue', font=("Arial Bold", 14))
    title_label.grid(row=0, column=0, columnspan=8)

    # Get printout from current_weather_file and add text to message widget
    current_weather_string = current_weather_file.getvalue()
    current_weather = tk.Message(master=frm_info, text=current_weather_string, aspect=200, bg='light blue')
    current_weather.grid(row=1, column=0, columnspan=8)

    # Right icon
    current_icon = ImageTk.PhotoImage(icon_image)
    current_icon_label = tk.Label(master=frm_info, image=current_icon, bg='light blue')
    current_icon_label.image = current_icon
    current_icon_label.grid(row=1, column=6)

    # Left icon
    current_icon2 = ImageTk.PhotoImage(icon_image)
    current_icon_label2 = tk.Label(master=frm_info, image=current_icon2, bg='light blue')
    current_icon_label2.image = current_icon2
    current_icon_label2.grid(row=1, column=1)


# Function to fill and print future weather data
def print_weather_forecast(data):

    # Get count of days to iterate through for loop
    count = len(data['daily'])

    # Hourly label
    hourly_label = tk.Label(master=frm_info, text='24 HOUR FORECAST', font=("Arial Bold", 14), bg='light blue')
    hourly_label.grid(row=2, column=0, columnspan=12, sticky='n')

    # Daily label
    daily_label = tk.Label(master=frm_info, text='7 DAY FORECAST', font=("Arial Bold", 14), bg='light blue')
    daily_label.grid(row=8, column=0, columnspan=12, sticky='n')

    # For each day or 3-hour period, get and print forecast - (range(27)[4::3] = Start at index 4, grab every 3rd)
    for x, y in zip(range(count), range(27)[4::3]):

        # Hourly iteration

        # Assign all used variables
        weather_description = data['hourly'][y]['weather'][0]['description']
        high_temp = int(round(data['hourly'][y]['temp'], 0))
        utc_time = datetime.utcfromtimestamp(data['hourly'][y]['dt'])
        added_time = timedelta(0,int(data['timezone_offset']))
        date_time = utc_time + added_time
        forecast_datetime = date_time.strftime('%-I %p')

        precipitation_chance = "{:.0%}".format(data['hourly'][y]['pop'])
        wind_speed = int(round(data['hourly'][y]['wind_speed'], 0))
        wind_degree = data['hourly'][y]['wind_deg']
        wind_direction = get_wind_direction(wind_degree)
        icon_id = data['hourly'][y]['weather'][0]['icon']
        icon_image = get_weather_icon(icon_id)

        # Time header label
        time_label = tk.Label(master=frm_info, text=forecast_datetime, font=("Arial Bold", 13), bg='light blue')
        time_label.grid(row=3, column=x)

        # High temperature label - 24 hours
        forecast_weather_string_24 = str(high_temp) + u"\N{DEGREE SIGN}" + "F"
        forecast_weather_24 = tk.Label(master=frm_info, text=forecast_weather_string_24, bg='light blue')
        forecast_weather_24.grid(row=4, column=x)

        # Wind label - 24 hours
        wind_string_24 = str(wind_direction) + ' ' + str(wind_speed) + ' mph'
        wind_label_24 = tk.Label(master=frm_info, text=wind_string_24, bg='light blue')
        wind_label_24.grid(row=5, column=x)

        # Image label - 24 hours
        forecast_icon_24 = ImageTk.PhotoImage(icon_image)
        forecast_icon_label_24 = tk.Label(master=frm_info, image=forecast_icon_24, bg='light blue')
        forecast_icon_label_24.image = forecast_icon_24
        forecast_icon_label_24.grid(row=6, column=x)

        # Check for chance of rain or snow to print chance of precipitation, if none, print blanks to hold space - 24 hr
        if str(weather_description).find('rain') != -1 or str(weather_description).find('snow') != -1:

            precipitation_chance_label_24 = tk.Label(master=frm_info, text=precipitation_chance, bg='light blue')
            precipitation_chance_label_24.grid(row=7, column=x)

        else:

            precipitation_chance_label_24 = tk.Label(master=frm_info, text="", bg='light blue')
            precipitation_chance_label_24.grid(row=7, column=x)

        # Daily iteration

        # Assign all used variables
        weather_description = data['daily'][x]['weather'][0]['description']
        high_temp = int(round(data['daily'][x]['temp']['max'], 0))
        low_temp = int(round(data['daily'][x]['temp']['min'], 0))
        wind_speed = int(round(data['daily'][x]['wind_speed'], 0))
        wind_degree = data['daily'][x]['wind_deg']
        wind_direction = get_wind_direction(wind_degree)
        precipitation_chance = "{:.0%}".format(data['daily'][x]['pop'])
        icon_id = data['daily'][x]['weather'][0]['icon']
        icon_image = get_weather_icon(icon_id)

        # Get date string
        if x == 0:

            date_string = 'Today'

        else:

            date_string = date.fromtimestamp(data['daily'][x]['dt']).strftime('%A')

        # DoW header label
        date_label = tk.Label(master=frm_info, text=date_string, font=("Arial Bold", 13), bg='light blue')
        date_label.grid(row=10, column=x)

        # High temperature label
        forecast_weather_string = 'H: ' + str(high_temp) + u"\N{DEGREE SIGN}" + "F"
        forecast_weather = tk.Label(master=frm_info, text=forecast_weather_string, bg='light blue')
        forecast_weather.grid(row=11, column=x)

        # Low temperature label
        forecast_weather_string2 = "L: " + str(low_temp) + u"\N{DEGREE SIGN}" + "F"
        forecast_weather2 = tk.Label(master=frm_info, text=forecast_weather_string2, bg='light blue')
        forecast_weather2.grid(row=12, column=x)

        # Wind label
        wind_string = str(wind_direction) + ' ' + str(wind_speed) + ' mph'
        wind_label = tk.Label(master=frm_info, text=wind_string, bg='light blue')
        wind_label.grid(row=13, column=x)

        # Image label
        forecast_icon = ImageTk.PhotoImage(icon_image)
        forecast_icon_label = tk.Label(master=frm_info, image=forecast_icon, bg='light blue')
        forecast_icon_label.image = forecast_icon
        forecast_icon_label.grid(row=14, column=x)

        # Check for chance of rain or snow to print chance of precipitation, if none, print blanks to hold space
        if str(weather_description).find('rain') != -1 or str(weather_description).find('snow') != -1:

            precipitation_chance_label = tk.Label(master=frm_info, text=precipitation_chance, bg='light blue')
            precipitation_chance_label.grid(row=15, column=x)

        else:

            precipitation_chance_label = tk.Label(master=frm_info, text="", bg='light blue')
            precipitation_chance_label.grid(row=15, column=x)

        # Add spaces to keep column widths standard, unless last column
        lbl_spacer = tk.Label(master=frm_info, text='                          ', bg='light blue')
        lbl_spacer.grid(row=17, column=x)

    # Back button
    btn_search_again = tk.Button(
        master=frm_info,
        text="Back",
        command=lambda: get_weather_again_click(),
        width=19,
        bg='light grey',
        fg='black')
    btn_search_again.grid(row=19, column=2, columnspan=2, sticky='s')

    # Quit button
    btn_quit = tk.Button(
        master=frm_info,
        text="Quit",
        command=lambda: quit_click(),
        width=19,
        bg='light grey',
        fg='black')
    btn_quit.grid(row=19, column=4, columnspan=2, sticky='s')

    # After all information is built, update window
    frm_info.grid(row=0, column=0)
    window.update()


# Function to get and return the image associated with the weather conditions
def get_weather_icon(icon_id):

    icon_url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)
    icon_response = requests.get(icon_url, stream=True)
    icon_image = Image.open(BytesIO(icon_response.content))
    icon_image = icon_image.resize((75, 75))

    return icon_image


# Function to convert wind degrees into a direction
def get_wind_direction(wind_degree):

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    quadrant = int((wind_degree / 45) + 0.5)
    direction = directions[quadrant % 8]

    return direction


# Function to handle the clicking of 'get weather' button that calls the main function
def get_weather_click():

    # Clear error message, if any
    error_message.set(" ")
    lbl_error_message.tkraise()
    window.update()

    # Catch empty search
    if __name__ == '__main__' and ent_city_zip.get().strip() != '':
        main()


# Function to handle the clicking of 'back' button that calls the main function
def get_weather_again_click():

    # destroy all labels from forecast and current weather
    for widget in frm_info.winfo_children():
        widget.destroy()

    # remove form #2
    frm_info.grid_remove()

    # rebuild original form
    ent_city_zip.grid(row=2, column=1, sticky="w")
    lbl_city_zip.grid(row=2, column=0, sticky="w")
    lbl_title.grid(row=0, column=1, sticky='w')
    lbl_error_message.grid(row=0, column=0, columnspan=8)
    lbl_error_message.tkraise()
    lbl_space.grid(row=0, column=3)
    frm_entry.grid(row=0, column=0, padx=10)
    btn_search.grid(row=3, column=1)
    ent_city_zip.delete(0, 'end')

    # update window to render changes
    window.update()


# Function to handle the clicking of 'quit' button
def quit_click():

    window.destroy()


def main():

    # Get user entry
    entry = ent_city_zip.get().strip()

    # If entry is completely alpha, minus spaces, commas, and periods (for St., Mt., etc.)
    if entry.replace(',', '').replace(" ", "").replace('.', '').isalpha():

        # Initialize search_type and zip_code for passing to other functions if city search
        zip_code = '00000'
        search_type = 'CITY'

        # while True to catch input error
        while True:

            # if only city is searched
            if len(entry.split(',')) == 1:

                city = entry.title()
                state_code = ''

            # if city/state combination are attempted
            elif len(entry.split(',')) == 2:

                # If state code is two characters, assign variables
                if len(entry.split(',')[1].strip()) == 2:

                    city = entry.split(',')[0].strip().title()
                    state_code = entry.split(',')[1].strip().upper()

                else:

                    error_message.set("Please enter a two character state code.")
                    lbl_error_message.tkraise()
                    break

            # Multiple commas (i.e. Omaha, NE, USA)
            else:

                error_message.set('Enter a city name, city name/state code combination, or zip code to continue.')
                lbl_error_message.tkraise()
                break

            # use try for assertion error, return error from function if input error
            try:

                search_type = get_weather_data(search_type, city, state_code, zip_code)
                assert search_type != 'ERROR'
                break

            except AssertionError:

                break

    # if entry is only digits
    elif entry.isdigit():

        # Initialize search_type and city for passing to other functions if city search
        search_type = 'ZIP'
        city = ''
        state_code = ''

        # while True to catch input error
        while True:

            zip_code = entry

            # Ensure zip code is 5 digits
            if len(str(zip_code)) != 5:
                error_message.set('Please enter a valid 5 digit zip code.')
                lbl_error_message.tkraise()
                break

            # use try for assertion error, return error from function if input error
            try:

                search_type = get_weather_data(search_type, city, state_code, zip_code)
                assert search_type != 'ERROR'
                break

            except AssertionError:

                break

    # Catch any special characters or alpha/numeric combinations
    else:

        error_message.set('Please enter either a city or zip code to search.')
        lbl_error_message.tkraise()


# Set up the window
window = tk.Tk()
window.title("Weather Information")
window.resizable(width=True, height=True)
window.configure(bg='light blue')

# Initialize error_message string in case of errors
error_message = tk.StringVar()

# Create labels and entry text box
frm_entry = tk.Frame(master=window, bg='light blue')
frm_info = tk.Frame(master=window, bg='light blue')
ent_city_zip = tk.Entry(width=15)
lbl_title = tk.Label(text="", bg='light blue')
lbl_error_message = tk.Label(textvariable=error_message, font=('Arial', 10), bg='light blue', fg='red')
lbl_city_zip = tk.Label(text="City Name / Zip Code :", bg='light blue')
lbl_space = tk.Label(text='                     ', bg='light blue')
lbl_connection = tk.Label(bg='light blue')

# Check connection and add label
location_df = test_connection()

# PLace labels and text box in window
ent_city_zip.grid(row=2, column=1, sticky="w")
lbl_city_zip.grid(row=2, column=0, sticky="w")
lbl_title.grid(row=0, column=1, sticky='w')
lbl_error_message.grid(row=0, column=0, columnspan=10)
lbl_space.grid(row=3, column=3)
lbl_error_message.tkraise()

# Create the get weather button with function to call main()
btn_search = tk.Button(
    master=window,
    text="Get Weather",
    command=lambda: get_weather_click(),
    width=12,
    bg='light grey',
    fg='black',
)

# Set-up the layout using the .grid() geometry manager
frm_entry.grid(row=1, column=0, padx=10)
btn_search.grid(row=3, column=1)

# Run the application
window.mainloop()
