import streamlit as st
import pandas as pd
import re
from typing import Dict, Union
from llama_cpp import Llama
import time
from state_manager import StateManager

class YieldAdvisorLLM:
    def __init__(self):
        self.static_yields = {
            "rice": 2873,
            "wheat": 3615,
            "jowar": 1175,
            "bajra": 1449,
            "maize": 3321,
            "tur": 831,
            "gram": 1224,
            "groundnut": 2179,
            "rapeseed and mustard": 1443,
            "sugarcane": 79000,
            "cotton": 436,
            "jute": 2795,
            "mesta": 2056,
            "potato": 24000,
            "tea": 2042,
            "coffee": 780,
            "rubber": 973
        }
        
        # Convert hectare values to per acre
        self.static_yields = {crop: yield_value/2.47105 for crop, yield_value in self.static_yields.items()}
        self.initialize_llm()

    def initialize_llm(self):
        """Initialize LLM if not already initialized"""
        if 'llm' not in st.session_state:
            try:
                st.session_state.llm = Llama(
                    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                    n_ctx=2048,
                    n_threads=4,
                    n_gpu_layers=0,
                    verbose=False
                )
            except Exception as e:
                st.error(f"Error initializing LLM: {str(e)}")
                st.session_state.llm = None

    def parse_response(self, response):
        """Parse LLM response to extract yield and price values"""
        try:
            lines = response.strip().split('\n')
            yield_value = None
            price_value = None
            
            for line in lines:
                if line.startswith('Yield:'):
                    yield_value = float(line.replace('Yield:', '').strip())
                elif line.startswith('Price:'):
                    price_value = float(line.replace('Price:', '').strip())
            
            return yield_value, price_value
        except Exception as e:
            st.warning(f"Error parsing response: {str(e)}")
            return None, None

    def get_price_from_llm(self, crop: str) -> float:
        """Get crop price using LLM"""
        if st.session_state.llm is None:
            self.initialize_llm()
            if st.session_state.llm is None:
                return None

        price_prompt = f"""<s>[INST] You are an agricultural market specialist. Provide the current market price per kg for {crop} in India based on recent trends. Return ONLY the numeric price value in rupees per kg.

        For reference, some typical crop prices:
        Rice: 20-25 Rs/kg
        Wheat: 25-30 Rs/kg
        Cotton: 60-70 Rs/kg
        Potato: 15-20 Rs/kg

        Respond EXACTLY in this format (just the number):
        Price: XXX[/INST]"""

        try:
            price_response = st.session_state.llm(
                price_prompt,
                max_tokens=20,
                temperature=0.9,
                top_p=0.1,
                repeat_penalty=1.2,
                stop=["[INST]", "</s>"]
            )
            
            price_text = price_response['choices'][0]['text'].strip()
            price_match = re.search(r'Price:\s*(\d+(?:\.\d+)?)', price_text)
            
            return float(price_match.group(1)) if price_match else None
        except Exception as e:
            st.warning(f"Error getting price: {str(e)}")
            return None

    def get_recommendations(self, crop: str) -> tuple:
        """Get yield and price recommendations using LLM prompt"""
        if st.session_state.llm is None:
            self.initialize_llm()
            if st.session_state.llm is None:
                return None, None

        combined_prompt = f"""<s>[INST] You are an agricultural specialist. For the crop {crop} in India:
                        1. Provide its yield per acre (in kg/acre)
                        2. Provide its current market price (in Rs/kg)

                        For reference:
                        Typical yields (2023-24):
                        - Rice: 1162 kg/acre
                        - Wheat: 1463 kg/acre
                        - Cotton: 176 kg/acre
                        - Potato: 9713 kg/acre

                        Typical prices:
                        - Rice: 20-25 Rs/kg
                        - Wheat: 25-30 Rs/kg
                        - Cotton: 60-70 Rs/kg
                        - Potato: 15-20 Rs/kg

                        Respond EXACTLY in this format (just the numbers):
                        Yield: XXX
                        Price: XXX[/INST]"""

        try:
            # Add small delay between LLM calls to prevent resource conflicts
            time.sleep(0.1)
            
            response = st.session_state.llm(
                combined_prompt,
                max_tokens=20,
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.2,
                stop=["[INST]", "</s>"]
            )
            
            response_text = response['choices'][0]['text'].strip()
            return self.parse_response(response_text)
        except Exception as e:
            st.warning(f"Error getting recommendations: {str(e)}")
            return None, None

    def get_yield_prediction(self, crop: str, acres: float) -> Dict[str, Union[str, float]]:
        """Get yield prediction and calculate total income"""
        if not crop:
            return None
            
        crop = crop.lower().strip()
        
        try:
            # First check static data for yield
            if crop in self.static_yields:
                yield_per_acre = self.static_yields[crop]
                price_per_kg = self.get_price_from_llm(crop)
                
                if price_per_kg is None:
                    return {
                        "crop": crop,
                        "acres": acres,
                        "error": "Could not determine price"
                    }
            else:
                # Get both yield and price from LLM for unknown crops
                yield_per_acre, price_per_kg = self.get_recommendations(crop)
                
                if yield_per_acre is None or price_per_kg is None:
                    return {
                        "crop": crop,
                        "acres": acres,
                        "error": "Could not determine yield or price"
                    }

            # Calculate totals
            expected_yield = acres * yield_per_acre
            total_income = expected_yield * price_per_kg
            
            return {
                "crop": crop,
                "acres": acres,
                "yield_per_acre": yield_per_acre,
                "expected_yield": expected_yield,
                "price_per_kg": price_per_kg,
                "total_income": total_income,
                "unit": "kg"
            }

        except Exception as e:
            return {
                "crop": crop,
                "acres": acres,
                "error": str(e)
            }

def render_yield_advisor_tab():
    """Function to render the Yield Advisor tab content"""

    StateManager.initialize_state()
    if 'yield_advisor' not in st.session_state:
        st.session_state.yield_advisor = YieldAdvisorLLM()
    
    if 'num_crops' not in st.session_state:
        st.session_state.num_crops = 1
    
    # Add/Remove crop buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("➕ Add Crop"):
            st.session_state.num_crops = min(5, st.session_state.num_crops + 1)  # Limit to 5 crops
            
    with col2:
        if st.button("➖ Remove Crop") and st.session_state.num_crops > 1:
            st.session_state.num_crops -= 1
    
    # Create inputs for each crop
    predictions = []
    
    with st.form(key='crop_form'):
        for i in range(st.session_state.num_crops):
            col1, col2 = st.columns([2, 1])
            with col1:
                crop = st.text_input(
                    f"Crop Name {i+1}",
                    key=f"crop_{i}",
                    placeholder="e.g., rice, wheat, potato"
                ).strip().lower()
            with col2:
                acres = st.number_input(
                    f"Acres {i+1}",
                    min_value=0.1,
                    max_value=1000.0,
                    value=1.0,
                    step=0.1,
                    key=f"acres_{i}"
                )
            
            if crop:
                with st.spinner(f"Calculating predictions for {crop}..."):
                    prediction = st.session_state.yield_advisor.get_yield_prediction(crop, acres)
                    if prediction:
                        predictions.append(prediction)
        
        submit_button = st.form_submit_button(label="Calculate Yield")
    
    if submit_button:
        if not predictions:
            st.error("Please enter at least one crop name")
        else:
            display_predictions(predictions)
            if predictions and all('total_income' in pred for pred in predictions):
                st.session_state.total_income_value = sum(pred['total_income'] for pred in predictions)

def display_predictions(predictions):
    """Display the predictions in a formatted table with totals"""
    st.subheader("Yield Predictions")
    
    try:
        df = pd.DataFrame(predictions)
        if 'error' in df.columns:
            st.warning("Some predictions could not be calculated")
            df = df[['crop', 'acres', 'error']].fillna('-')
        else:
            # Format numeric columns
            df['yield_per_acre'] = df['yield_per_acre'].apply(lambda x: f"{x:,.2f} kg/acre")
            df['expected_yield'] = df['expected_yield'].apply(lambda x: f"{x:,.2f} kg")
            df['price_per_kg'] = df['price_per_kg'].apply(lambda x: f"₹{x:,.2f}")
            df['total_income'] = df['total_income'].apply(lambda x: f"₹{x:,.2f}")
            
            # Calculate totals
            total_area = sum(pred['acres'] for pred in predictions)
            total_yield = sum(pred['expected_yield'] for pred in predictions)
            total_income = sum(pred['total_income'] for pred in predictions)
            
            # Rename and format columns
            df.columns = ['Crop', 'Acres', 'Yield per Acre', 'Expected Yield', 'Price per kg', 'Total Income', 'Unit']
            df = df.drop('Unit', axis=1)
            
            # Display results
            st.dataframe(df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Area", f"{total_area:,.2f} acres")
            with col2:
                st.metric("Total Expected Yield", f"{total_yield:,.2f} kg")
            with col3:
                st.metric("Total Income", f"₹{total_income:,.2f}")
            
            # Add download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Predictions",
                data=csv,
                file_name="yield_predictions.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error displaying predictions: {str(e)}")

# def main():
#     st.set_page_config(
#         page_title="Advanced Soil and Weather Analysis System",
#         page_icon="🌾",
#         layout="wide"
#     )
    
#     st.title("Advanced Soil and Weather Analysis System")
#     tabs = st.tabs([
#         "Location & Weather",
#         "Soil Analysis",
#         "Environmental Risks",
#         "Forecast",
#         "Crop Advisor",
#         "Yield Advisor",
#         "Profit Dashboard"
#     ])
    
#     with tabs[5]:
#         st.title("Yield Advisor")
#         st.write("Predict crop yields based on official Indian agricultural data")
#         render_yield_advisor_tab()

# if __name__ == "__main__":
#     main()