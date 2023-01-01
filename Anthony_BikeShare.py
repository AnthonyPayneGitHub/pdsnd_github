import time
import pandas as pd
import numpy as np
import string

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
cities = ['chicago','new york city','washington']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyzec
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*'*70)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('*'*70)
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\nWhich city would you like to analyze, Chicago, New York City or Washington ?:\n')).lower()
            if city not in cities:
                print('No Bikeshare data available for {}, please try again.'.format(city))      
            else:
                break    

        except Exception as e:
           
            print('{}, is not a valid entry.'.format(city))
            print('-'*40)
            main()
            
        
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\nWhich month would you like to analyze (all, january, february, ... , june) ?\n')).lower()
            if month not in months:
                print('No Bikeshare data available for {}, please try again, be sure to enter month between January and June or all.'.format(month))
            else:
                break

        except Exception as e:
             
             print('{}, is not a valid entry.'.format(month))
             print('-'*40)
             main()
             

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\nWhich day of the week would you like to analyze (all, monday, tuesday, ... sunday) ?:\n')).lower()
            if day not in days:
                print('No Bikeshare data available for {}, please try again, be sure to enter day of week between Sunday and Saturday or all.'.format(day))
            else:
                break
        
        except Exception as e:
            
            print('{}, is not a valid entry.'.format(day))
            print('-'*40)
            main()

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['daynumber'] = df['Start Time'].dt.day
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        month = months.index(month) 
        df = df[df['month'] == month] 


    # filter by Day if applicable
    if day != 'all':
        
        # use the index of the months list to get the corresponding int
        df['day_name'] = df['Start Time'].dt.day_name()
        df = df[df['day_name'] == day.title()] 
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('Most common month: ',popular_month)
    
    # find the most common Start hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most common hour: ', popular_hour)

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most common day of the week: ',popular_weekday)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """ Displays statistics on the most popular stations and trip. """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    df['station'] = df['Start Station']
    popular_station=df['station'].mode()[0]
    print('Most common Origin Station: ',popular_station)

    # TO DO: display most commonly used end station
    df['Dest station'] = df['End Station']
    popular_end_station=df['Dest station'].mode()[0]
    print('Most common Destination Station: ',popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'].str.cat(' to '+df['End Station'])
    popular_trip=df['trip'].mode()[0]
    print('\nMost popular Trip: ',popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total and mean travel time
    df['Duration']=df['Trip Duration']
    Total_time = df['Duration'].sum()
    Mean_Time = df['Duration'].mean()

    """ Convert Seconds to Minutes, Hours and Days in order to Display Travel Time to user """
    Minutes_Seconds = 60
    Hours_Seconds = 3600
    Hours_Days = 24
    Days_Seconds = np.multiply(Hours_Days,Hours_Seconds)
    
    """ Days """
    Trip_Days = int(np.divide(Total_time, Days_Seconds))
    Trip_Mean_Days = int(np.divide(Mean_Time,Days_Seconds))
    
    """ Hours """
    Total_time = Total_time % (Days_Seconds)
    Mean_Time = Mean_Time % (Days_Seconds)
    Trip_Hours = int(np.divide(Total_time,Hours_Seconds))
    Trip_Mean_Hours = int(np.divide(Mean_Time,Hours_Seconds))
 
    """ Minutes """
    Total_time %= Hours_Seconds
    Mean_Time %= Hours_Seconds
    Trip_Minutes = int(np.divide(Total_time,Minutes_Seconds))
    Trip_Mean_Minutes = int(np.divide(Mean_Time,Minutes_Seconds))

    """ Seconds """
    Total_time %= Minutes_Seconds
    Trip_Seconds = int(Total_time)
    Mean_Time %= Minutes_Seconds
    Trip_Mean_Seconds = int(Mean_Time)

    # TO DO: display mean travel time
    print('Total and Mean Travel Times in Seconds.')
    print("Total Travel Time: {} Seconds.".format(df['Duration'].sum()))
    print("Mean Travel Time: {} Seconds.".format(df['Duration'].mean()))

    """ Print Total and Mean Travel Times Converted to Days, Hours, and Seconds """
    print('\nTotal and Mean Travel Times converted to Days, Hours, Minutes, and Seconds.')
    print("Total Travel Time: ",Trip_Days,"days", Trip_Hours, "hours",Trip_Minutes, "minutes",Trip_Seconds, "seconds")
    print("Mean Travel Time: ",Trip_Mean_Days,"days", Trip_Mean_Hours, "hours",Trip_Mean_Minutes, "minutes",Trip_Mean_Seconds, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """ Displays statistics on bikeshare users. """

    print('\nCalculating Bikeshare User Stats...\n')
    start_time = time.time()

    try:
        # TO DO: Display counts of user types
        df['Users'] = df['User Type']
        print("User Type Distribution:")
        print(df['Users'].value_counts())

        # TO DO: Display counts of gender
        print("\nGender Distribution:")
        if "Gender" in df.columns:
            df['Gender Type'] = df['Gender'] 
            print(df['Gender Type'].value_counts())
        else:
            print('Bikeshare Gender data not available for this city.')

        # TO DO: Display earliest, most recent, and most common year of birth
        print("\nBirth Year Stats:")
        if "Birth Year" in df.columns:
            df['BirthYear'] = df['Birth Year']
            print("Earliest Birth Year:", int(df['BirthYear'].min()))
            print("Most recent Birth Year:", int(df['BirthYear'].max()))
            print("Most common Birth Year:", int(df['BirthYear'].mode()[0]))
        else:
            print("Bikeshare Birth data not available for this city.") 

    except(KeyError) as e:
        print('Data file error:',(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def Display_Trip_Detail(df):
    
    """ Display Bikeshare Trip detail data 5 rows at time, pending user request. """

    show_detail = input('Bikeshare Trip detail data can be presented 5 rows at a time.\nWould you like to see the first 5 rows of Trip detail data? Answer yes or no: ').lower()
    start_row = 0
    while show_detail == 'yes':
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        show_detail = input('Would you like to see the next 5 rows of Trip detail data? Answer yes or no: ').lower()


def main():
    
    """ Main function to return Bikeshare Stats."""

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        Display_Trip_Detail(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThank you, your Bikeshare analysis is complete!')
            break


if __name__ == "__main__":
	main()
