import requests
import pandas as pd

def fetch_clinical_trials(condition="cancer", max_studies=100, save_path=None):
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "filter.cond": condition,
        "pageSize": max_studies,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    trials = []
    for study in data.get('studies', []):
        identification = study.get('protocolSection', {}).get('identificationModule', {})
        conditions_module = study.get('protocolSection', {}).get('conditionsModule', {})
        eligibility_module = study.get('protocolSection', {}).get('eligibilityModule', {})
        location_module = study.get('protocolSection', {}).get('contactsLocationsModule', {})
        
        trial = {
            'nct_id': identification.get('nctId'),
            'title': identification.get('briefTitle'),
            'condition': "; ".join(conditions_module.get('conditions', [])),
            'eligibility': eligibility_module.get('eligibilityCriteria', ''),
            'location': "; ".join(
                [loc.get('city', '') for loc in location_module.get('locations', []) if 'city' in loc]
            )
        }
        trials.append(trial)
    
    df = pd.DataFrame(trials)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Saved to {save_path}")
    
    return df

# Example usage
if __name__ == "__main__":
    df = fetch_clinical_trials("lung cancer", 50, save_path="clinical_trials1.csv")
    print(df.head())
