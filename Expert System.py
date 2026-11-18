
# Create a dictionary containing the medical rules
rules = {
    "Possible Flu": {"fever", "cough", "body aches"},  # Symptoms associated with flu
    "Possible Common Cold": {"sneezing", "runny nose", "sore throat"},  # Symptoms associated with a cold
    "Possible Allergy": {"sneezing", "itchy eyes", "runny nose"}  # Symptoms associated with allergies
}

# Ask the user to enter their symptoms
user_input = input("Enter your symptoms separated by commas: ")

# Convert the input into lowercase words and separate them using commas
symptoms_list = user_input.lower().split(",")

# Create an empty set to store the patient's symptoms
patient_symptoms = set()

# Go through every symptom entered by the user
for symptom in symptoms_list:

    # Remove unnecessary spaces and add the symptom to the set
    patient_symptoms.add(symptom.strip())

# Create a variable to check if a diagnosis was found
found = False

# Check every diagnosis and its required symptoms
for diagnosis, required_symptoms in rules.items():

    # Check if all required symptoms exist in the patient's symptoms
    if required_symptoms.issubset(patient_symptoms):

        # Display the possible diagnosis
        print("Result:", diagnosis)

        # Change found to True because a rule matched
        found = True

# Check if no diagnosis was found
if found == False:

    # Display a message if none of the rules matched
    print("No matching diagnosis found.")

# Display a medical safety message
print("This is an educational system, not a real medical diagnosis.")
