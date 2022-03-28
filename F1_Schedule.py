"""
Brian Horner
CS 521 - Summer 1
Date: 6/22/2021
Final Project
This program takes a provided Formula 1 race schedule url and file.
It takes the Formula 1 race data with and writes to the file the race,
race location, race time, race time converted to EST, and time until
the race using the Race clas from the race_class module.
"""

# Imports
import datetime
import requests
import json
from bs4 import BeautifulSoup
import race_class


def race_info_output(data_list, file_name):
    """Function takes json data from the dictionaries in scrapped race data. It
    iterates over the data calling the Race class from race_class.py.
    It then writes the __repr__ method output to the file provided by the
    user."""
    for dictionary in data_list:
        # Assigning values from keys to temp storage
        temp_data_storage = (race_class.Race(dictionary['name'],
                                             dictionary['location']['address'],
                                             dictionary['endDate']))
        # Calling the Race class __repr__ method
        output_text = temp_data_storage.__repr__()
        # If not at end of data or no data errors
        if output_text is not None:
            # Writing data to file with line breaks in between
            with open(file_name, 'a') as output_file:
                output_file.write(output_text + "\n")
    print(f"Process done. Check out your file {file_name} with the Formula 1 "
          f"race data.")


def file_overwrite():
    """Prompts the user for inputs determining if the file provided s
    hould be overwritten or not. If yes, it will prompt the user to
    determine if a header should be added to the file. If not it does
    not overwrite the file and breaks out of the loop"""
    # Taking valid file name from user
    file_name = input("Please provide a text file name for the Formula 1 race "
                      "data"
                      " to be written to. (With correct file name syntax and "
                      ".txt extension): ")
    print(f"You provided the file name {file_name}.\n")
    loop_controller = 1
    while loop_controller < 2:
        # Getting input from user to determine if file is to be overwritten
        overwrite_file = input("Would you like to overwrite the previous "
                               "Formula 1 race data? (Yes or No): ")
        if overwrite_file == "Yes":
            #
            file_header = input("\nWould you like a descriptive header for "
                                "the Formula 1 Race Data? (Yes or No): ")
            if file_header == "Yes":
                try:
                    current_datetime = datetime.datetime.today(). \
                        strftime('%B %d, %Y - %I:%M:%S %p EST')
                    file = open(file_name, 'w')
                    file.write(f"Formula 1 Future Races as of "
                               f"{current_datetime}:\n\n")
                    file.close()
                    loop_controller += 1
                    print("\nThe option to have a descriptive header was "
                          "selected.")
                    print(f"Overwriting your file {file_name} with "
                          f"the new Formula 1 race data.\n")
                # Except catch for general file errors
                except OSError:
                    print("Error. File was not found, your file name was "
                          "incorrect or your disk is full. Please try again.")
                    break
            elif file_header == "No":
                try:
                    # Overwriting file using file write parameter
                    file = open(file_name, 'w')
                    file.write("")
                    file.close()
                    loop_controller += 1
                    print("The option to have no header was selected.")
                    print(f"Overwriting your file {file_name} with "
                          f"the new Formula 1 race data.\n")
                # Except catch for general file errors
                except OSError:
                    print("Error. File was not found, your file name was "
                          "incorrect or your disk is full. Please try again.")
                    break
        elif overwrite_file == "No":
            # We do not prompt for header as previous data still exists in file.
            print("We will append the new race data to the end of the file.\n")
            loop_controller += 1
        # Will prompt user for input until valid
        else:
            print("Error invalid input. Please try again.")
    return file_name


def main(url):
    """Takes a provided url as a argument and uses requests to connect. It
    uses beatufiul soup to grab the content of the website and find all data
    within script tag of type "application/ld+json. We then clean the data
    getting rid of the script tags, line breaks, duplicate }}
    and add the array brackets for conversion to json data with the json
    module. This is then provided to the race_info_output function."""
    # Printing descriptive output to instruct user on function of program
    print("This program returns up coming Formula 1 Race data from the "
          "provided current Formula 1 schedule link. Example: "
          "https://www.formula1.com/en/racing/2021.html\n")
    cleaned_data_string = ""
    # Using requests to connect to url
    r = requests.get(url)
    # Grabbing the data from the website
    soup = BeautifulSoup(r.content, 'html.parser',)
    # Finding all data with the 'script' tage of specific type
    all_scripts = soup.findAll('script', type="application/ld+json")
    # Going through data and cleaning for proper json format
    # This is memory intensive and not optimized for speed
    for number, script in enumerate(all_scripts):
        script = str(script).strip()
        script = script.split("</script>")
        script = str(script)[39:-6]
        script = script.replace("\\n", "")
        script = script.replace("\\", "")
        script = script.replace("}}", "}},")
        cleaned_data_string = cleaned_data_string + "" + script
    cleaned_data_string = "[" + cleaned_data_string
    cleaned_data_string = cleaned_data_string[:-1] + "]"
    # Loading clean race data into json module
    race_data = json.loads(cleaned_data_string)
    # Calling race data and the func file_overwrite
    race_info_output(race_data, file_overwrite())


# Calling main with url as argument
main("https://www.formula1.com/en/racing/2021.html")
