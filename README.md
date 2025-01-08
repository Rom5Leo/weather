
# **Weather App**

An interactive weather application built with **Streamlit** that provides weather data for user-specified locations. The app includes features like persistent user settings, interactive maps, weather icons, and more.

## **Features**

- **Retrieve Weather Information**:
  - Get the current temperature, humidity, and weather condition for any location.
  - Display local date and time for the queried location.
  
- **Favorite Locations**:
  - Add, view, and remove favorite locations.
  - Set a default location for quick access.

- **Interactive Map**:
  - View the queried location on an interactive map using **Folium**.

- **Weather Icons**:
  - Display icons that represent current weather conditions.

- **Persistent Settings**:
  - Store user preferences (default location, favorite locations, and temperature units) in `settings.json`.

## **Project Structure**

```
weather/
├── .devcontainer/        # Development environment configuration for containers
│   ├── devcontainer.json
├── weather/              # Core application logic
│   ├── __init__.py
│   ├── weather.py        # Functions for fetching and processing weather data
├── manage_settings.py    # Handles persistent settings using JSON
├── app.py                # Main Streamlit app
├── main.py               # CLI-based weather data viewer
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_weather.py   # Tests for weather functions
├── .streamlit/           # Streamlit configuration and secrets
│   ├── secrets.toml      # API keys for local testing
├── settings.json         # Persistent user settings
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Poetry configuration
├── poetry.lock           # Poetry dependency lock file
├── README.md             # Project documentation
├── .gitignore            # Files and directories to ignore in Git
```

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/weather.git
cd weather
```

### **2. Install Dependencies**
Using **pip**:
```bash
pip install -r requirements.txt
```
Or using **Poetry**:
```bash
poetry install
```

### **3. Add API Key**
1. Create a `.streamlit/secrets.toml` file.
2. Add your OpenWeatherMap API key:
   ```toml
   [OPENWEATHERMAP_API_KEY]
   OPENWEATHERMAP_API_KEY = "your_api_key_here"
   ```

### **4. Run the Application**
Start the Streamlit app:
```bash
streamlit run app.py
```

### **5. Run Tests**
Run unit tests using:
```bash
python -m unittest discover tests
```

---

## **Usage**

### **Weather Retrieval**
1. Enter a city name to retrieve weather data.
2. View temperature, humidity, and weather condition.
3. See a local map of the location and a weather icon.

### **Manage Locations**
- Add a favorite location:
  - Enter a city name in the **Add to Favorite Locations** field and click **Add**.
- Remove a favorite location:
  - Select a city from the dropdown and click **Remove**.
- Set a default location:
  - Enter a city name in the **Set Default Location** field and click **Set**.

---

## **Technologies Used**

- **Python**: Core language for the app.
- **Streamlit**: Framework for building the interactive web app.
- **Folium**: Library for rendering interactive maps.
- **Requests**: HTTP library for API calls.
- **Pytest/Unittest**: For testing application logic.
- **Poetry**: Dependency management.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Future Enhancements**

- Add historical weather comparisons.
- Allow users to switch between Celsius and Fahrenheit dynamically.
- Add alerts for extreme weather conditions.
