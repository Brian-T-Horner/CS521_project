"""
Brian Horner
CS 521 - Summer 1
Date: 6/22/2021
Final Project
This program establishes the Race class which takes the end race time,
location and time parameter. It has methods to return the race time,
race time in est, time until race and a print out with the race name,
race location, race time, race time in est, and time until race.
"""

# Imports
import datetime


class Race:
    """Race class for processing Formula 1 Race general data. It takes
    Name, Location, and race end time parameters. Time must be formatted as
    YYYY-MM-DDTHH:mm:SS as is customary with the Formula 1 website.
    This class is designed for web scrapping with the Formula 1 website."""
    def __init__(self, race_name, race_location, race_time):

        self.__race_name = race_name
        self.__race_location = race_location
        self.__race_time = race_time

    def actual_race_time(self):
        """This method calculates the time of the Formula 1 Race by
        subtracting two hours from the self.race_time attribute. The
        self.race_time is always set to two hours after the race starts."""
        # Keeping the race time format consistent with json data
        time_format = '%Y-%m-%dT%H:%M:%S'
        # Converting race_time to a datetime object
        race_time = datetime.datetime.strptime(self.__race_time, time_format)
        # Using datetime.delta to subtract two hours from race_time
        race_time = race_time - datetime.timedelta(hours=2)
        return race_time

    def race_local_time(self):
        """Method uses the return of actual_race_time function to
        convert the race time to local time (aka EST). It uses a
        dictionary containing how many hours ahead or behind the race
        location is from New York, USA."""
        time_date_conversion_table = {'Spielberg, Austria': 6,
                                      'Silverstone, Great Britain': 5,
                                      'Budapest, Hungary': 6,
                                      'Spa-Francorchamps, Belgium': 6,
                                      'Zandvoort, Netherlands': 6,
                                      'Monza, Italy': 6,
                                      'Sochi, Russia': 7,
                                      'Suzuka, Japan': 13,
                                      'Austin, United States': -1,
                                      'Mexico City, Mexico': -2,
                                      'São Paulo, Brazil': 2,
                                      'Melbourne, Australia': 16,
                                      'Jeddah, Saudi Arabia': 8,
                                      'Yas Island, Abu Dhabi': 9,
                                      'Istanbul, Turkey': 7
                                      }
        # Getting the race location from the self.race_location attribute
        try:
            time_delta_variable = time_date_conversion_table.get(
                self.__race_location)
        # Subtracting race time from the timedelta value from dictionary
            race_time_local = self.actual_race_time() - \
                datetime.timedelta(hours=time_delta_variable)
        # Could use a catch for if number is negative
            return race_time_local
        except TypeError:
            return"Error the race location was not found in the  " \
                  "time_data_conversion_table. Please consult developer to  " \
                  "update table.\n"

    def time_until_race(self):
        """Method uses the datetime module to determine how long until the
        Race."""
        time_format = '%H:%M:%S %p'
        # Getting time until the Race
        try:
            time_until_race = self.race_local_time() - \
            datetime.datetime.now()
            # Formatting rac_local_time return for this method
            race_time_display = datetime.datetime.strftime(self.race_local_time(), time_format)
            # Getting days and hours for return statement
            days = time_until_race.days
            hours = time_until_race.seconds / 3600
            return f"The Race is in {days} days and {hours:,.0f} hours at " \
                   f"{race_time_display}."
        except TypeError:
            return "Error the race location was not found in the  " \
                  "time_data_conversion_table. Please consult developer to  " \
                  "update table.\n"

    def __repr__(self):
        """Method provides the attributes and methods of the Race class in a
        clean printable manner."""
        time_format = '%B %d, %Y - %I:%M:%S %p'
        est_time_format = '%B %d, %Y - %I:%M:%S %p EST'
        # Uses .format as f'strings were to messy with this many variables
        try:
            return "Race Name: {0}\nRace Location: {1}\nRace Time: {2}\nRace " \
                   "Time in EST: {3}\nTime until Race: {4}" \
                   "\n".format(self.__race_name, self.__race_location,
                               datetime.datetime.strftime(self.actual_race_time(),
                                                          time_format),
                               datetime.datetime.strftime(self.race_local_time(),
                                                          est_time_format),
                               self.time_until_race())
        except TypeError:
            return "Error the race location was not found in the  " \
                  "time_data_conversion_table. Please consult developer to  " \
                  "update table.\n"


if __name__ == "__main__":
    """Unit Tests"""
    # Establishing variables for Class construction using individual variables
    test_race_name = "Boston"
    test_race_location = "Boston, MA"
    test_race_time = "2021-10-13T08:00:00"
    # Testing variable construction of Race Class
    race_class_test1 = Race(test_race_name, test_race_location, test_race_time)
    # Printing type
    print(type(race_class_test1))
    # Establishing dictionary for Class construction using dictionary
    race_class_test2 = {"name": "Silverstone",
                        "location": "Silverstone, Great Britain",
                        "time": "2021-11-13T08:00:00"}

    # Testing dictionary construction of Race Class
    race_class_test2 = Race(race_class_test2["name"],
                           race_class_test2["location"],
                           race_class_test2["time"])
    # Checking type of Race Class
    print(type(race_class_test2))

    # Testing actual_race_time Race method
    print(Race.actual_race_time(race_class_test1))
    print(Race.actual_race_time(race_class_test2))

    # Testing invalid input catch for race_local_time Race Method
    print(Race.race_local_time(race_class_test1))
    # Testing valid input for race_local_time Race Method
    print(Race.race_local_time(race_class_test2))

    # Testing invalid input catch for time_until_race Race Method
    print(Race.time_until_race(race_class_test1))
    # Testing valid input for time_until_race Race method
    print(Race.time_until_race(race_class_test2))

    # Testing invalid input catch for Race __repr__
    print(race_class_test1)
    # Testing valid input catch for Race __repr__
    print(race_class_test2)
