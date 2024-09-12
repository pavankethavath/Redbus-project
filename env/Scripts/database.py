import mysql.connector
import pandas as pd

# Function to create MySQL connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Pavan@22',
        database='redbus_data'
    )

# Function to fetch data from the bus_routes table
def load_data():
    conn = create_connection()
    query = "SELECT * FROM bus_routes"  
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to categorize bus type based on seat type
def categorize_seat_type(bustype):
    if pd.isnull(bustype):
        return 'Others'
    bustype = bustype.lower()  
    if 'seater' in bustype or 'push back' in bustype:
        if 'sleeper' in bustype and 'seater' in bustype:
            return 'Seater / Sleeper'
        else:
            return 'Seater'
    elif 'sleeper' in bustype:
        if 'semi' in bustype:
            return 'Semi Sleeper'
        else:
            return 'Sleeper'
    else:
        return 'Others'

# Function to process and return the bus data with categorized seat types
def get_processed_data():
    df = load_data()
    df['seat_type_category'] = df['bustype'].apply(categorize_seat_type)
    return df
