# Best-Crop-Recommendation-System

This project is an AI-powered crop recommendation system that suggests the most suitable crop(s) for a farmer based on soil, weather, and market conditions.

## Project Status

This is a functional baseline prototype that demonstrates the core features of the crop recommendation system. It includes:

*   A machine learning model trained on soil and weather parameters.
*   An interactive web application built with Streamlit.
*   Top-3 crop recommendations with confidence scores.
*   Basic fertilizer advice based on N, P, K levels.
*   Profitability estimates based on sample economic data.
*   A secure interface for adding an API key to fetch live weather data.

## Future Work

This project was envisioned as a comprehensive, best-in-class system. The current implementation is the first step. The following features from the original plan are part of the future roadmap:

*   **Advanced Data Integration:**
    *   Integrate historical weather data (10-20 years) for trend analysis.
    *   Incorporate remote sensing data (NDVI, EVI, soil moisture) from Sentinel or Landsat satellites.
    *   Use detailed agro-climatic zone data.
*   **Advanced Modeling:**
    *   Implement an LSTM/GRU model to capture time-series trends in weather.
    *   Build a hybrid CNN+MLP model to process satellite imagery alongside tabular data.
    *   Use multi-objective optimization for ranking crops based on profitability, sustainability, and yield.
*   **Enhanced Features:**
    *   Pest and disease forecasting.
    *   Personalized crop rotation schedules.
    *   A multilingual chatbot for wider accessibility.
*   **Production Deployment:**
    *   Containerize the application with Docker.
    *   Deploy to a cloud service like AWS, GCP, or Heroku for scalable access.