import time
import pandas as pd
import numpy as np


'''
Purpose:        Calculate various bikeshare data (proj #2:  Bikeshare)
By:             Quang Luong
Proj Due Date:  7/17/2018
Cohort:         June2018 Udacity Data Analyst Nano Degree

'''
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# used for time_stats calculation
months = ['january', 'february', 'march', 'april', 'may', 'june']
 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ["chicago", "new york", "washington"]
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
   

    print('Hello! Let\'s explore some US bikeshare data!')

    is_valid = False
     
# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
# As long as user input is incorrect, we will continue to ask...
    while not is_valid:
        city = input("Would you like to see data for Chicago, New York, or Washington?: ").lower().strip()
        is_valid = True
        if city not in cities:
            is_valid = False
      
    is_valid = False
    while not is_valid:
        #if is_valid:        
        answer_filter = input("Would you like to filter the data by month, day, or not at all? (Type 'na' for no time filter): ").lower().strip()
        if answer_filter == 'month':
            month = input("Please enter the month -- January, February, March, April, May, or June: " ).lower().strip() 
            is_valid = True
            day = 'all'
            if month not in months:
                is_valid = False
        elif answer_filter == 'day':
            day = input("Please enter the day of week -- Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday): ").lower().strip()
            is_valid = True
            month = 'all'
            if day not in days:
                is_valid = False
        elif answer_filter == 'na':
            month = 'all'
            day = 'all'
            is_valid = True
        else:
            is_valid = False
                         
        if not is_valid:
            print("one or more entry is invalid. Please try again.")

       
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# read data into dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

#filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        #filter by month to create new dataframe
        df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print("Popular times to travel (occurs most often in the start time)")
    
    start_time = time.time()
    
# TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = months[popular_month - 1].title()
    print("most common month: {}".format(popular_month))

# TO DO: display the most common day of week
    #popular_day = df['day_of_week'].mode()[0]
    print("most common day of week: {}".format(df['day_of_week'].mode()[0]))

# TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    
# popular_hour is a 24-hour, so convert to 12-hr clock
    if popular_hour > 12:
        hour = str(popular_hour - 12) + " pm"
    elif popular_hour == 12:
        hour = str(popular_hour) + " pm"
    else:
        hour = str(popular_hour) + " am"        
    print("most common hour of day: {}".format(hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print("Popular Stations and trip")
    start_time = time.time()

# TO DO: display most commonly used start station
    #common_start_station = df['Start Station'].mode()[0]
    print("most common start station: {}".format(df['Start Station'].mode()[0]))


# TO DO: display most commonly used end station
    #common_end_station = df['End Station'].mode()[0]
    print("most common end station: {}".format(df['End Station'].mode()[0]))

# TO DO: display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] +  ' to ' + df['End Station']
    print("most common trip from start to end: {}".format(combo_station.mode()[0]))
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    ASSUMPTIONS: MILLISECONDS ARE IGNORED """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# TO DO: display total travel time
    # get total seconds
    total_travel_time_sec = df['Trip Duration'].sum()
    
    # divide by 60 seconds per min to get minutes and seconds
    minutes, seconds = divmod(total_travel_time_sec, 60)
    
    # divide by 60 minutes per hour to get hour and minutes
    hour, minutes = divmod(minutes, 60)
    print("total travel time: {} hours, {} minutes, and {} seconds".format(hour, minutes, seconds))

# TO DO: display mean travel time
    mean_travel_time_sec = round(df['Trip Duration'].mean())
       
    # divide by 60 minutes per hour to get hour and minutes
    minutes, seconds = divmod(mean_travel_time_sec, 60)
    
    # divide by 60 minutes per hour to get hour and minutes
    hour, minutes = divmod(minutes, 60)
    print("average travel time: {} hour(s), {} minute(s), {} second(s)".format(hour, minutes, seconds))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

# TO DO: Display counts of user types
        print("counts of each user type:\n{}\n ".format(df['User Type'].value_counts()))
    
# TO DO: Display counts of gender
        print("counts of each gender:\n{}\n ".format(df['Gender'].value_counts()))
    except KeyError as e:
        print('counts of each gender:\nNo Gender for city chosen: {}\n'.format(city.title()))
    
    try:
# TO DO: Display earliest, most recent, and most common year of birth
        print('earliest, most recent, and most common year of birth:')
        print('earliest: {}'.format(int(df['Birth Year'].min())))
        print('most recent: {}'.format(int(df['Birth Year'].max())))
        print('most common: {}'.format(int(df['Birth Year'].mode()[0])))
    
    except KeyError as e:
        print('No Birth Year for city chosen: {}'.format(city))
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_raw_data(df):
    """
    Purpose:  ask user if they want to display individual trip data, and if so, how many
              records user wishes to see at a time
    Args:
         (dataframe) df  - data based on user selection
         
    Returns:  NONE
    """
    
    is_valid = False
       
    #keep asking until answer is correct:  y or n
    while not is_valid:
        try:
            answer = input("Would you like to see individual raw data? (enter 'y' or 'n') ").lower().strip()
            
            if answer == 'y':
                num_recs_display = input("How many records would you like to see at one time? ")
                num_recs_display = int(float(num_recs_display))
                display_raw_data(df, num_recs_display)
                is_valid = True
            elif answer == 'n':
                break
            else:
                is_valid = False
        except TypeError as e:
            print("{} is not a number\n".format(num_recs_display))
            is_valid = False
        except ValueError as e:
            print("{} is incorrect. Please enter a NUMBER. \n".format(num_recs_display))
            is_valid = False
    
def display_raw_data(df, num_recs_display):
    """
    Purpose:    Display the actual number of records 
    
    Args:
            (dataframe) df                  - data based on user selection
            (int)       num_recs_display    - number of records user wishes to see at a time
         
    Returns:  NONE
    """
    recs_to_display = num_recs_display
    lower_bound = 0
    uppr_bound = recs_to_display
    df_size = len(df.index)
    
    while (lower_bound < df_size):
        # chk if rows to be displayed is more than what we actually have
        if uppr_bound > df_size:
            uppr_bound = df_size  
            recs_to_display = df_size - lower_bound
            
        print("\nDisplaying {} rows of data: ".format(recs_to_display))
        print(df.iloc[lower_bound : uppr_bound])
        to_continue = input("would you like to see more records ('y' or 'n'): ")
        
        if to_continue.lower().strip() == 'y':
            lower_bound = uppr_bound 
            uppr_bound += recs_to_display 
        else:
            print("You do not wish to continue viewing...")
            break
    else:
        print("No more records to display")
    
    
def main():
    while True:
        city, month, day = get_filters()
        print("Calculating for {}, {}, and {} ...\n".format(city.title(), month.title(), day.title()))
        
        df = load_data(city, month, day)
            
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        get_raw_data(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


