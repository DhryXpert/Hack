import re

class EligibilityCriteria:
    def __init__(self):
        self.age_pattern = r'age[:\s]*(\d+)[^\d]*(\d+)?'
        self.gender_pattern = r'(male|female|both)'

    def parse_criteria(self, criteria_text):
        if not criteria_text:
            return {}
        parsed = {}
        age_match = re.search(self.age_pattern, criteria_text.lower())
        if age_match:
            min_age = int(age_match.group(1))
            max_age = int(age_match.group(2)) if age_match.group(2) else None
            parsed['age_range'] = (min_age, max_age)
        gender_match = re.search(self.gender_pattern, criteria_text.lower())
        if gender_match:
            parsed['gender'] = gender_match.group(1)
        return parsed

    def check_eligibility(self, patient_profile, trial_criteria):
        criteria = self.parse_criteria(trial_criteria)
        if 'age_range' in criteria:
            min_age, max_age = criteria['age_range']
            if patient_profile['age'] < min_age:
                return False
            if max_age and patient_profile['age'] > max_age:
                return False
        if 'gender' in criteria:
            required_gender = criteria['gender']
            if required_gender != 'both' and patient_profile['gender'] != required_gender:
                return False
        return True
