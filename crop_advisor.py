import os
from llama_cpp import Llama
class CropAdvisorLLM:
    def __init__(self):
        print("Initializing Mistral model for crop recommendations")
        self.llm = Llama(
            model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            n_ctx=2048,
            n_threads=os.cpu_count(),
            n_gpu_layers=0,
            verbose=False
        )
    

    def get_recommendations(self, location_data):
        prompt = f"""<s>[INST] You are an agricultural expert. I need specific crop recommendations for this specific location only and conditions.

            Current Conditions:
            Location: {location_data['region']}
            Temperature: {location_data['weather_analysis']['current']['temperature']['value']}°C
            Humidity: {location_data['weather_analysis']['current']['humidity']['value']}%
            Season: {location_data['season']}
            Soil: {location_data['soil_analysis']['basic_properties']['detailed_characteristics']['soil_composition']['texture']}

            Generate 3 specific crop recommendations based on these location conditions. List them in order of suitability.Give recommendations based on region.It should be very specific and famous in that region
            TYPE :[category] should be one among fruits,vegetables,cereals,pulses,flowers,leafy vegetables

          

            1. CROP: [name] | TYPE: [category] | SCORE: [1-100] | REASON: [Include regional significance if applicable]

            Your recommendations: [/INST]

            """


        try:
            response = self.llm(
                prompt,
                max_tokens=2048,
                temperature=0.1,  # Lower temperature for more focused output
                top_p=0.9,
                repeat_penalty=1.2,
                stop=["[INST]"]
            )

            generated_text = response['choices'][0]['text']
        

            recommendations = self.parse_recommendations("1." + generated_text)
            # end_time = time()
            # print(f"Generation time: {end_time - start_time:.2f} seconds")

            return recommendations

        except Exception as e:
            print(f"Error in generation: {str(e)}")
            return []
        
    def parse_recommendations(self, text):
            recommendations = []
            current_items = []

            # Split by newlines and process each line
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Check if line starts with a number and contains a pipe
                if (line.startswith(('1.', '2.', '3.')) or len(current_items) > 0) and '|' in line:
                    # Remove the number prefix if it exists
                    if line[0].isdigit():
                        line = line.split('.', 1)[1].strip()

                    # Split by pipes and extract components
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 4:
                        rec = {
                            'crop': parts[0],
                            'type': parts[1],
                            'score': parts[2],
                            'reason': parts[3]
                        }
                        recommendations.append(rec)

            return recommendations

    def print_recommendations(self,recommendations, region):
        print(f"\nRECOMMENDED CROPS FOR {region}")
        print("=" * 60)

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['crop'].upper()}")
                print(f"   Category: {rec['type']}")
                print(f"   Suitability: {rec['score']}")
                print(f"   Reason: {rec['reason']}")
        else:
            print("No recommendations generated. Retrying with different parameters...")
            return False
        return True

  
        