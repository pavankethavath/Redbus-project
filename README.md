# RedBus Data Scraping and Dynamic Filtering Application

This project is a **Streamlit-based web application** designed to help users filter and display bus services from the **RedBus dataset**. The project fetches data from a **MySQL database**, which is populated by scraping data from the **RedBus website** using **Selenium**. The web application offers users a set of customizable filters to narrow down bus options based on their preferences, such as **route, seat type, A/C type, ratings, fare, and departure time**.

## Problem Statement

The "RedBus Data Scraping and Filtering Application" seeks to transform bus travel management by automating the extraction, analysis, and visualization of bus travel data. By utilizing **Selenium** for web scraping, this project efficiently collects data on bus routes, schedules, prices, and seat availability. By streamlining data collection and providing tools for decision-making, this solution aims to improve the overall user experience in the transportation industry and drive data-driven decisions.

## Business Use Cases

This solution can be applied to multiple business scenarios, including:

- **Travel Aggregators**: Display real-time bus schedules and seat availability to customers.
- **Market Analysis**: Analyze travel patterns and preferences for research and optimization.
- **Customer Service**: Offer customized travel options based on user data insights.
- **Competitor Analysis**: Compare pricing, services, and travel options with competitors to gain a market edge.
  
## Features

### 1. **Data Scraping Using Selenium**
- Data is scraped from the dynamic RedBus website using **Selenium** and stored in a **MySQL database**.
- The scraping script navigates through **12 RTCs**, iterating over all routes in all pages under each RTC Card.
- It collects crucial bus information such as **routes, route links, bus types, timings, fare, and seat availability**.
- The script ensures that sufficient time is provided to load all the data, handles pagination, and interacts with the "View Buses" buttons.

### 2. **MySQL Database Interaction**
- The project interacts with a **MySQL database** to fetch and manage bus route data.
- **Pandas** is used to manipulate the data, including categorizing seat types (e.g., Seater, Sleeper, Semi Sleeper) based on the bus descriptions.

### 3. **User Interface using Streamlit**
- The user interface is built using **Streamlit**, providing a clean and intuitive way for users to filter bus services.
- Users can filter buses based on various criteria, such as **route, seat type, A/C type, ratings, fare range**, and **departure time**.

  #### Home Page:
  - Displays a welcome message along with a bus image.
  - ![Home Screen](Images/Home_Screen.png)

  #### Bus Filter Page:
  - Users can apply filters like:
    - **Route Selection**: Choose the desired bus route.
    - **Seat Type**: Filter by seat types (Seater, Sleeper, Seater/Sleeper, Semi Sleeper, etc.).
    - **A/C Type**: Choose between A/C or Non-A/C buses.
    - **Departure Time**: Select buses based on time range (e.g., 22:00 - 23:00).
    - **Star Ratings**: Filter buses by user ratings (1 to 5).
    - **Fare Range**: Select buses based on ticket price (e.g., ₹500 - ₹1000).
    - 
  - ![Filters Screen](Images/Filters_Screen.png)

  #### Results Screen:
  - After applying filters, the results display a table with available buses, including information such as:
    - **Bus Name** - **Bus Type** - **Departure Time** - **Duration** - **Fare** - **Ratings** - **Seats Available**
  - ![Results Screen](Images/Results_Screen.png)

### 4. **Filter Logic**
- The filtering mechanism applies various transformations and constraints to the dataset:
  - **Seat Type Categorization**: Bus seat types (e.g., Seater, Sleeper) are categorized based on keywords.
  - **A/C and Non-A/C Detection**: Uses **regex patterns** to match buses based on whether they have A/C or are non-A/C.
  - **Time-Based Filtering**: Users can filter buses based on **departure time ranges**.
  - **Fare Range Filtering**: Filters buses according to the selected price range.

## Technologies Used
- **Python**: Core language for the application.
- **Streamlit**: For building the web interface.
- **MySQL**: For storing and managing bus data.
- **Selenium**: For web scraping dynamic bus data from the RedBus website.
- **Pandas**: For data manipulation and processing.
- **Regex**: For detecting A/C and Non-A/C buses.
  
---

## Database Schema

The scraped data is stored in a `bus_routes` table with the following schema:

| Column           | Data Type | Description                           |
|------------------|-----------|---------------------------------------|
| id               | INT       | Primary Key (Auto-increment)          |
| route_name       | TEXT      | Name of the bus route                 |
| route_link       | TEXT      | Link to route details                 |
| busname          | TEXT      | Name of the bus operator              |
| bustype          | TEXT      | Type of bus (Seater, Sleeper, etc.)    |
| departing_time   | TIME      | Departure time                        |
| duration         | TEXT      | Duration of the journey               |
| reaching_time    | TIME      | Arrival time                          |
| star_rating      | FLOAT     | User rating of the bus                |
| price            | DECIMAL   | Ticket price                          |
| seats_available  | INT       | Number of available seats             |

---
## Project Files

The project files are located in the `env/Scripts` directory, and they include:

1. **`selenium_redbus_data_scraping.ipynb`**:
   - Jupyter notebook containing the web scraping script, which collects bus data from the RedBus website and stores it in a MySQL database.

2. **`database.py`**:
   - Handles the MySQL database connections and fetches bus route data.
   - Processes and categorizes bus types using **Pandas** and returns the data for the app.

3. **`RedBusProject.py`**:
   - The main **Streamlit** application that defines the user interface.
   - Contains the logic to apply filters based on user selections and displays the filtered bus results.

4. **`redbus_database.sql`**:
   - SQL file for setting up the database structure, including tables like `bus_routes`.

## How to Run

### Prerequisites:
Ensure you have the following installed:
- **Python 3.x**
- **MySQL Server**
- **Selenium WebDriver**
- **Streamlit** (`pip install streamlit`)
- **Pandas** (`pip install pandas`)
- **MySQL Connector** (`pip install mysql-connector-python`)

### Steps:

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd redbus-project

## Set up MySQL Database:

1. **Create a MySQL Database**:
   - Use the provided `redbus_database.sql` file to set up the required database.
   - Ensure that the **database connection details** (username, password, host, etc.) in `database.py` match your MySQL setup.

2. **Run the Streamlit Application**:
   - To run the application, use the following command:
     ```bash
     streamlit run RedBusProject.py
     ```

## Scrape Data (if required):

- If you need to scrape new data from the RedBus website, use the `selenium_redbus_data_scraping.ipynb` notebook.
- The notebook will collect and populate new bus route data into the MySQL database.

## Future Enhancements:

1. **Advanced Filters**:
   - Add more detailed filtering options, such as:
     - Bus operator
     - Bus amenities (WiFi, charging ports)
     - Travel duration

2. **Live Data Integration**:
   - Integrate real-time bus data using the **RedBus API** to provide up-to-the-minute bus availability and pricing.

3. **Booking Links**:
   - Provide direct links that allow users to book buses through RedBus after filtering.

## Contributing:

- Contributions are welcome! Feel free to submit **pull requests** or open **issues** for any bugs, feature requests, or improvements.
- Let me know if you need any further changes or assistance!
