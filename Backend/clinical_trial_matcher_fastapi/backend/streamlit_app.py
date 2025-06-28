import streamlit as st
import requests

st.set_page_config(page_title="AI Clinical Trial Matcher", layout="centered")
st.title("🔬 AI Clinical Trial Matcher")

# Input form
with st.form("patient_form"):
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    gender = st.selectbox("Gender", ["male", "female","other"])
    conditions = st.text_input("Medical Conditions (comma-separated)", "lung cancer")
    symptoms = st.text_input("Symptoms (comma-separated)", "cough, fatigue")
    location = st.text_input("Location", "Delhi")
    submit = st.form_submit_button("Find Matching Trials")

# On submit
if submit:
    with st.spinner("Matching trials..."):
        try:
            payload = {
                "age": age,
                "gender": gender,
                "conditions": [c.strip() for c in conditions.split(",")],
                "symptoms": [s.strip() for s in symptoms.split(",")],
                "location": location
            }
            response = requests.post("http://127.0.0.1:8000/match-trials", json=payload)
            matches = response.json()
            i = 0
            if not matches:
                st.warning("No matching trials found.")
            else:
                for match in matches:
                    i+=1
                    st.subheader(match['title'])
                    st.markdown(f"**NCT ID:** {match['nct_id']}")
                    st.markdown(f"**Similarity Score:** {match['similarity_score']:.2f}")
                    st.markdown(f"**Eligibility Status:** {match['eligibility_status']}")
                    if match['eligibility_status'] == "Needs Review":
                        st.warning("Eligibility needs review.")
                    else:
                        st.success("You are eligible for this trial!")
                    with st.form(f"email{i}"):
                        sub = st.form_submit_button("Apply for Trial")
                        if sub:
                            st.success("Your application has been submitted!")
                    if match['match_reasons']:
                        st.markdown("**Reason(s):**")
                        for reason in match['match_reasons']:
                            st.markdown(f"- {reason}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error: {e}")
