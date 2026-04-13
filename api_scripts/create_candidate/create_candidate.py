import requests
import json
import logging
import random
import string
import certifi

from config import API_BASE_URL, LOGIN_API_ENDPOINT, CREATE_CANDIDATE_API
from env.credentials import USERNAME, PASSWORD

logging.basicConfig(level=logging.INFO)


# -------------------------------
# Generate Random Data
# -------------------------------
def generate_random_name():
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"Nir_demo_{rand}"


def generate_random_email():
    rand = ''.join(random.choices(string.digits, k=6))
    return f"s1n1j1e1v1{rand}@gmail.com"


# -------------------------------
# Login API
# -------------------------------
def login_and_get_token(api_base_url, username, password):
    try:
        logging.info(f"Logging in with username: {username}")

        payload = {
            "LoginName": username,
            "Password": password,
            "TenantAlias": "agenticqa",
            "UserName": username
        }

        headers = {
            "content-type": "application/json"
        }

        login_url = f"{api_base_url}{LOGIN_API_ENDPOINT}"

        response = requests.post(
            login_url,
            headers=headers,
            data=json.dumps(payload),
            verify=certifi.where()
        )

        response.raise_for_status()

        login_response = response.json()
        token = login_response.get("Token")

        logging.info("Login successful.")
        return token

    except Exception as e:
        logging.error(f"Login failed: {e}")
        raise


# -------------------------------
# Create Candidate API
# -------------------------------
def create_candidate(api_base_url, token, name, email):
    url = f"{api_base_url}{CREATE_CANDIDATE_API}"

    headers = {
        "x-auth-token": token,
        "Content-Type": "application/json"
    }

    payload = {
        "AttachmentCollection": {"ResumeUrl": None, "PhotoUrl": None, "OtherAttachments": None},
        "PersonalDetails": {
            "Name": name,
            "PassportNo": "",
            "MaritalStatus": None,
            "DateOfBirth": "",
            "Address1": "",
            "PhoneOffice": None,
            "Gender": None,
            "Email1": email,
            "CurrencyType": None,
            "AadhaarNo": None
        },
        "EducationDetails": {"AddedItems": []},
        "PreferenceDetails": {},
        "SourceDetails": {},
        "ExperienceDetails": {"AddedItems": []},
        "SocialDetails": {},
        "CandidateMoreDetails": {},
        "CompensationDetails": {
            "CompanyId": None,
            "CompanyText": None,
            "TotalCTC": None,
            "FixedCTC": None,
            "VariablePercent": None,
            "VariablePay": None,
            "RetentionBonus": None,
            "RBPayoutScheme": None,
            "JoiningBonus": None,
            "JBPayoutScheme": None,
            "OtherBonus": None,
            "OtherBonusType": None,
            "OBPayoutScheme": None,
            "TotalESOPAllotted": None,
            "ESOPRate": None,
            "VestedSharesPercent": None,
            "NonVestedSharedPercent": None,
            "TotalVestingPeriod": None,
            "AdditionalAllotmentPerYear": None,
            "OtherDetails": None,
            "FileUrls": None
        },
        "SkillsDetails": {},
        "CustomDetails": {
            "Integer1": 11,
            "Integer2": 55,
            "Integer3": None,
            "Integer4": None,
            "Integer5": None,
            "Text1": "77",
            "Text2": "",
            "Text3": "",
            "Text4": "",
            "Text5": "",
            "DateCustomField1": "",
            "DateCustomField2": "",
            "TrueFalse1": False,
            "TrueFalse2": False
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    return response


# -------------------------------
# Main Execution
# -------------------------------
def main():
    token = login_and_get_token(API_BASE_URL, USERNAME, PASSWORD)

    if not token:
        logging.error("No token received. Exiting.")
        return

    for i in range(10):
        name = generate_random_name()
        email = generate_random_email()

        logging.info(f"Creating candidate {i+1}: {name}, {email}")

        response = create_candidate(API_BASE_URL, token, name, email)

        if response.status_code == 200:
            logging.info(f"✅ Candidate {i+1} created successfully")
        else:
            logging.error(f"❌ Failed for {name}: {response.text}")


if __name__ == "__main__":
    main()