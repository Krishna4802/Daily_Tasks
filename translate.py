# translate words as parameter

import requests

def translate_text(p_translate_data, p_target_lang, p_secret_key):
    url = "https://translation.googleapis.com/language/translate/v2"
    
    params = {
        "q": p_translate_data,
        "target": p_target_lang,
        "key": p_secret_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}, message: {response.text}"}

p_translate_data = "株式会社理研"
p_target_lang = "en"
p_secret_key = "API_KEY"

result = translate_text(p_translate_data, p_target_lang, p_secret_key)
print(result)


#############################################################################################################################################################################################################################


# translate words from csv files

import pandas as pd
import requests
import time

def translate_text(p_translate_data, p_target_lang, p_secret_key):
    
    url = "https://translation.googleapis.com/language/translate/v2"
    
    params = {
        "q": p_translate_data,
        "target": p_target_lang,
        "key": p_secret_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}, message: {response.text}"}
    
def process_csv(input_csv_path, output_csv_path, target_language, api_key):
    df = pd.read_csv(input_csv_path)
    df['translated_name'] = ""
    df['detected_language'] = ""

    for index, row in df.iterrows():
        name = row['name']
        result = translate_text(name, target_language, api_key)
        
        if 'data' in result and 'translations' in result['data']:
            translation = result['data']['translations'][0]
            df.at[index, 'translated_name'] = translation.get('translatedText', '')
            df.at[index, 'detected_language'] = translation.get('detectedSourceLanguage', '')
        else:
            
            df.at[index, 'translated_name'] = 'Error'
            df.at[index, 'detected_language'] = 'Error'
        time.sleep(1)
    
    df.to_csv(output_csv_path, index=False)
    print(f"Processed data saved to {output_csv_path}")


input_csv_path = '<source_file_name>.csv'
output_csv_path = '<dest_file_name>.csv'
target_language = 'en'
api_key = 'API_KEY'

process_csv(input_csv_path, output_csv_path, target_language, api_key)
