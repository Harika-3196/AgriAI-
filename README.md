# 🌾 Agri AI

## Overview

Agri AI is an advanced Gen AI application designed to empower new farmers with comprehensive agricultural insights. By combining location intelligence, environmental analysis, crop recommendations, yield predictions, and financial management, it provides a complete farming assistant in one user-friendly platform.

### video demo - https://drive.google.com/file/d/1vo-4yXwpKrgR4Jy_aiy_LhX0PRx94PK_/view?usp=sharing
### screenshots of application- https://drive.google.com/drive/folders/1sWXyHqeXpJaiyfvZmVyyjv9ffTV3jD9u?usp=sharing
## 🌟 Key Features

### 1. Smart Location Detection

* **Automatic Detection**: Uses system IP for location (via `http://ip-api.com/json`)
* **Manual Input**: Supports multiple formats:
  * Pincode
  * State
  * City
  * District

### 2. Environmental Intelligence

#### Regional Information
* Detailed geographical coordinates
* Comprehensive regional analysis

#### Weather Monitoring (OpenWeather API)
* **Temperature Analysis**
  * Real-time values
  * Classification (cold/hot/moderate)
* **Humidity Tracking**
  * Current levels
  * Classification (very humid/moderate/less)
* **Solar Radiation Monitoring**
  * Intensity measurements
  * Classification (High/low/moderate)
* **Wind Conditions**
  * Speed measurements
  * Dust storm probability

### 3. Soil Analysis (Ambee Data API)
* Physical Properties
* Chemical Properties
* Water Characteristics
* Fertility Indicators

### 4. Risk Assessment
* Climate type classification
* Environmental risk factors:
  * Landslide probability
  * Storm warnings
  * Other regional risks

### 5. Weather Forecasting
* 5-day detailed weather predictions
* Powered by OpenWeather API

### 6. 🤖 AI Crop Advisor

#### Model Architecture
* Based on **Mistral 7B Instruct Model**
* Converted to GGUF format for optimized performance
* Lightweight deployment using **llama.cpp**

#### Input Parameters
* Geographical location data
* Soil characteristics:
  * pH levels
  * Nutrient content
  * Water retention
* Local weather patterns
* Seasonal variations

#### Capabilities
* **Crop Recommendations**
  * Season-specific suggestions
  * Multiple crop options ranked by suitability
  * Intercropping possibilities
* **Growing Guidelines**
  * Optimal planting times
  * Spacing requirements
  * Irrigation schedules
* **Risk Assessment**
  * Disease susceptibility
  * Pest management suggestions
  * Weather-related precautions

#### Model Optimization
* GGUF format benefits:
  * Reduced memory footprint
  * Faster inference times
  * Efficient CPU usage
* Custom prompt templates for agriculture

### 7. 📊 Yield & Income Calculator

#### Yield Calculation Engine
* **Area-Based Calculations**
  * Supports multiple unit conversions (acres, hectares)
  * Accounts for:
    * Walking paths (15% area reduction)
    * Border spacing
    * Plant density optimization
    * Row spacing requirements

#### Crop-Specific Parameters
* **Yield Factors**
  * Historical yield data integration
  * Regional productivity patterns
  * Soil quality impact assessment
  * Weather influence coefficients

#### Market Integration
* **Price Analysis**
  * Real-time market rates
  * Historical price trends
  * Seasonal price variations
  * Local market differentials

#### Financial Projections
* **Expenses and Profit  Calculations with cool Visualizations based on category of spends**
  

### 8. Financial Dashboard
* Expense tracking
* Budget estimation
* Profit calculation
* Complete financial overview
* Download the report
  <p float="left">
  <img src="/Users/h0s060n/Desktop/Screenshot 2024-11-03 at 10.05.48 PM.png" width="400" />
  <img src="/Users/h0s060n/Desktop/Screenshot 2024-11-03 at 10.05.56 PM" width="400" /> 
</p>

## 📋 Requirements

### Model Setup

1. Download the GGUF-formatted Mistral model:
```
https://drive.google.com/file/d/1XOt8-Y9EWtsOIEH5bjVc3Y7V7EWbMafe/view?usp=drive_link
```
# Place it in your working directory

### Dependencies

Install required packages:
```bash
pip3 install -r requirements.txt
```

Key dependencies include:
* **transformers**
* **torch**
* **llama-cpp**

## 🔑 API Requirements
added testing keys in the repo for easy testing

You'll need API keys for:
* OpenWeather API
* Ambee Data API

## 💡 Getting Started

1. Clone the repository
2. Install dependencies
3. Download the Mistral model
4. Set up your API keys
5. Run the application
   
## crop advisor application
```streamlit run final.py ```

## yield prediction and dashboard 
```streamlit run yield_app.py```


