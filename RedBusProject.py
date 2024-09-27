import streamlit as st
import pandas as pd
from database import get_processed_data  # Importing database functions

# Load Data from the database
df = get_processed_data()

seat_types = ['Select...', 'Seater', 'Sleeper', 'Seater / Sleeper', 'Semi Sleeper', 'Others']
price_ranges = [f"{i}-{i+500}" for i in range(0, 2501, 500)]

# Function to get consecutive 2-hour time windows
def get_available_time_ranges(route_data):
    # Extract the bus departure times
    available_times = route_data['departing_time'].apply(lambda t: f"{t.components.hours:02}:{t.components.minutes:02}")
    
    # Create 2-hour time ranges, starting from 00:00 to 23:59
    all_time_ranges = []
    for hour in range(0, 24, 2):  # Increment by 2 hours
        start_time = f"{hour:02}:00"
        end_time = f"{(hour + 2) % 24:02}:00"
        all_time_ranges.append(f"{start_time} - {end_time}")

    # Filter time ranges that contain at least one available bus
    available_time_ranges = set()
    for time in available_times:
        hour = int(time.split(':')[0])
        start_time = f"{(hour // 2) * 2:02}:00"  # Get the closest 2-hour range start time
        end_time = f"{(hour // 2) * 2 + 2:02}:00"  # Calculate the corresponding end time
        available_time_ranges.add(f"{start_time} - {end_time}")

    # Return only the 2-hour windows where buses are available, sorted
    return sorted(available_time_ranges)

# Sidebar Buttons
st.sidebar.title("Main Menu")
home_button = st.sidebar.button("🏠 Home")
filter_button = st.sidebar.button("🚌 Filter Buses")

if "page" not in st.session_state:
    st.session_state.page = "home"

if home_button:
    st.session_state.page = "home"

if filter_button:
    st.session_state.page = "filter"

# Home Screen 
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>Welcome to the Bus Filter Application!</h1>", unsafe_allow_html=True)

    # Display the bus image at the center
    st.markdown("<div style='text-align: center;'>"
                "<img src='https://illustoon.com/photo/dl/5904.png' width='300' alt='Bus Image'></div>", 
                unsafe_allow_html=True)

# Bus Filter Screen 
elif st.session_state.page == "filter":

    st.markdown("<div style='text-align: center;'>"
                "<img src='https://illustoon.com/photo/dl/5907.png' width='200' alt='Bus Icon'></div>", 
                unsafe_allow_html=True)

    st.markdown("<div style='text-align: center;'>Please select the filters and click the 'Apply Filters' button to see available buses.</div>", unsafe_allow_html=True)
    st.write("")

    row1_col1, row1_col2, row1_col3 = st.columns([2, 1, 1])  

    with row1_col1:
        route_name = st.selectbox('Select the Route', ['Select...'] + list(df['route_name'].unique()))

    with row1_col2:
        seat_type = st.selectbox('Select Seat Type', seat_types)

    with row1_col3: 
        ac_type = st.selectbox('Select AC Type', ['Select...', 'A/C', 'Non A/C'])

    # Initialize available_time_ranges as ['Select...'] by default
    available_time_ranges = ['Select...']

    # Update available_time_ranges if a route is selected
    if route_name != 'Select...':
        # Filter data by the selected route
        route_data = df[df['route_name'] == route_name]
        
        # Get available time windows for this route
        available_time_ranges = ['Select...'] + get_available_time_ranges(route_data)

    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])  

    with row2_col1:
        depart_time = st.selectbox('Starting time', available_time_ranges)

    with row2_col2:
        # Replacing dropdown for ratings with a slider (integer values only)
        star_rating = st.slider('Select Ratings', 1, 5, (1, 5))  # Slider for selecting rating range (min 1, max 5)

    with row2_col3: 
        bus_fare_range = st.selectbox('Bus Fare Range', ['Select...'] + price_ranges)

    # Submit button 
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)  # Spacer
    apply_filters = st.button("Apply Filters")

    if apply_filters:
        st.markdown("### Available Buses")

        # Apply filters to the data
        if route_name != 'Select...':
            df = df[df['route_name'] == route_name]

        if seat_type != 'Select...':
            df = df[df['seat_type_category'] == seat_type]

        # Filtering based on A/C or Non A/C type
        if ac_type == 'A/C':
            df = df[df['bustype'].str.contains(r'A/C|AC|A\.C\.', case=False, regex=True)]
            df = df[~df['bustype'].str.contains(r'Non|NON-|NON', case=False, regex=True)]
        elif ac_type == 'Non A/C':
            df = df[df['bustype'].str.contains('Non A/C|Non AC|NON A/C|NON-AC', case=False, regex=True)]

        # Filtering by the selected rating range from the slider (integer values)
        df = df[(df['star_rating'] >= star_rating[0]) & (df['star_rating'] <= star_rating[1])]

        # Filtering by the selected departure time 
        if depart_time != 'Select...':
            time_start, time_end = depart_time.split(' - ')
            df['departing_minutes'] = df['departing_time'].apply(lambda x: x.components.hours * 60 + x.components.minutes)
            time_start_minutes = int(time_start.split(':')[0]) * 60 + int(time_start.split(':')[1])
            time_end_minutes = int(time_end.split(':')[0]) * 60 + int(time_end.split(':')[1])
            df = df[(df['departing_minutes'] >= time_start_minutes) & (df['departing_minutes'] < time_end_minutes)]

        if bus_fare_range != 'Select...':
            price_min, price_max = map(int, bus_fare_range.split('-'))
            df = df[(df['price'] >= price_min) & (df['price'] <= price_max)]

        df = df.reset_index(drop=True)  
        df.index += 1 

        df['departing_time'] = df['departing_time'].apply(lambda x: f"{x.components.hours:02}:{x.components.minutes:02}")
        df['reaching_time'] = df['reaching_time'].apply(lambda x: f"{x.components.hours:02}:{x.components.minutes:02}")

        if 'departing_minutes' in df.columns:
            df = df.drop(columns=['departing_minutes'])

        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        # Remove duplicates
        df = df.drop_duplicates()

        # Display results
        if df.empty:
            st.warning("No buses available for the selected filters.")
        else:
            st.markdown(f"### Route: {route_name}")
            if 'route_link' in df.columns and route_name != 'Select...':
                route_link = df['route_link'].iloc[0]
                st.markdown(f"[Route Link]({route_link})")

            # Format the price column to show only two decimal places and remove highlighting
            df_display = df[['busname', 'bustype', 'departing_time', 'duration', 'reaching_time', 'star_rating', 'price', 'seats_available']]
            df_display['price'] = df_display['price'].map('{:,.2f}'.format)  # Format price with 2 decimals

            # Display bus information without any highlighting on the price column
            st.dataframe(df_display)
    else:
        st.info("Please select the filters and click the 'Apply Filters' button to see available buses.")
