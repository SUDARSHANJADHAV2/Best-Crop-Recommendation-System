import streamlit as st
import pandas as pd
import joblib
import requests

# --- Initialize session state ---
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 26.0
if 'humidity' not in st.session_state:
    st.session_state['humidity'] = 57.0

# Load the trained model
model = joblib.load('models/baseline_random_forest.joblib')

# App title
st.title('Best Crop Recommendation System')

st.write("""
Enter the soil and weather conditions to get a crop recommendation. You can optionally fetch live weather data.
""")

# --- Weather API Integration ---
st.sidebar.header('Live Weather Data')
api_key = st.sidebar.text_input("Enter OpenWeatherMap API Key", type="password")
city = st.sidebar.text_input("Enter City Name", "Mumbai")

if st.sidebar.button("Fetch Weather"):
    if api_key:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data['cod'] == 200:
                st.session_state['temperature'] = data['main']['temp']
                st.session_state['humidity'] = data['main']['humidity']
                st.sidebar.success(f"Weather data for {city} fetched successfully!")
            else:
                st.sidebar.error(f"City not found or API key is invalid. (Error: {data.get('message', 'Unknown')})")
        except Exception as e:
            st.sidebar.error(f"Error fetching weather data: {e}")
    else:
        st.sidebar.warning("Please enter your API key to fetch weather data.")


# --- Input fields ---
st.header('Enter the following values:')

# Soil parameters
N = st.slider('Nitrogen (N)', 0, 140, 70)
P = st.slider('Phosphorus (P)', 5, 145, 75)
K = st.slider('Potassium (K)', 5, 205, 105)
ph = st.slider('pH', 3.5, 9.9, 6.7)
rainfall = st.slider('Rainfall (mm)', 20.0, 299.0, 160.0, help="Enter the average rainfall for the season.")

# Weather parameters (updated by API)
st.subheader("Weather Parameters")
temperature = st.slider('Temperature (°C)', 8.0, 44.0, st.session_state['temperature'])
humidity = st.slider('Humidity (%)', 14.0, 100.0, st.session_state['humidity'])

# Predict button
if st.button('Recommend Crop'):
    # Create a dataframe from the inputs
    input_data = pd.DataFrame({
        'N': [N],
        'P': [P],
        'K': [K],
        'temperature': [temperature],
        'humidity': [humidity],
        'ph': [ph],
        'rainfall': [rainfall]
    })

    # --- Top-3 Recommendations ---
    st.subheader('Top 3 Recommended Crops:')
    probabilities = model.predict_proba(input_data)
    top_3_indices = probabilities[0].argsort()[-3:][::-1]
    top_3_crops = model.classes_[top_3_indices]
    top_3_probs = probabilities[0][top_3_indices]

    for i in range(3):
        st.write(f"{i+1}. **{top_3_crops[i]}** (Confidence: {top_3_probs[i]*100:.2f}%)")

    # --- Fertilizer Advice ---
    st.subheader('Fertilizer Advice:')

    # N
    if N < 25:
        st.warning(f"**Nitrogen (N):** Your soil is low in Nitrogen ({N}). Consider adding a nitrogen-rich fertilizer like Urea.")
    elif N > 60:
        st.info(f"**Nitrogen (N):** Your soil has a good amount of Nitrogen ({N}).")
    else:
        st.success(f"**Nitrogen (N):** Your soil has an optimal level of Nitrogen ({N}).")

    # P
    if P < 30:
        st.warning(f"**Phosphorus (P):** Your soil is low in Phosphorus ({P}). Consider adding a phosphorus-rich fertilizer like Single Superphosphate (SSP).")
    elif P > 70:
        st.info(f"**Phosphorus (P):** Your soil has a good amount of Phosphorus ({P}).")
    else:
        st.success(f"**Phosphorus (P):** Your soil has an optimal level of Phosphorus ({P}).")

    # K
    if K < 25:
        st.warning(f"**Potassium (K):** Your soil is low in Potassium ({K}). Consider adding a potassium-rich fertilizer like Muriate of Potash (MOP).")
    elif K > 50:
        st.info(f"**Potassium (K):** Your soil has a good amount of Potassium ({K}).")
    else:
        st.success(f"**Potassium (K):** Your soil has an optimal level of Potassium ({K}).")

    # --- Profitability Analysis ---
    st.subheader('Profitability Analysis (Estimates per Hectare):')
    try:
        economics_df = pd.read_csv('data/crop_economics.csv')

        results = []
        for crop in top_3_crops:
            crop_data = economics_df[economics_df['crop'] == crop]
            if not crop_data.empty:
                yield_kg = crop_data['yield_kg_per_hectare'].values[0]
                price_inr = crop_data['price_inr_per_kg'].values[0]
                cost_inr = crop_data['cost_inr_per_hectare'].values[0]

                revenue = yield_kg * price_inr
                profit = revenue - cost_inr

                results.append({
                    "Crop": crop.capitalize(),
                    "Estimated Revenue (INR)": f"{revenue:,.2f}",
                    "Estimated Cost (INR)": f"{cost_inr:,.2f}",
                    "Estimated Profit (INR)": f"{profit:,.2f}"
                })

        if results:
            profit_df = pd.DataFrame(results)
            st.table(profit_df)
        else:
            st.info("Profitability data not available for the recommended crops.")

    except FileNotFoundError:
        st.error("Error: `crop_economics.csv` not found. Cannot perform profitability analysis.")
