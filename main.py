import requests
import json

def generate_wehook(name, reg_No, email):
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    registration_payload = {
        "name": name,
        "regNo": reg_No,
        "email": email
    }


    headers = {
        "Content-Type" : "application/json"

    }
    try:
        response = requests.post(url, json=registration_payload, headers= headers)
        response.raise_for_status()
        webhook_data = response.json()


        return webhook_data
    except:
        print("Exception occured from url")
        return None


def submit_Solution(webhook_url, access_token):
    headers = {
        "Authorization" : access_token,
        "Content-Type" : "application/json"
    }
    final_query = """
        
SELECT 
    e1.EMP_ID,
    e1.FIRST_NAME,
    e1.LAST_NAME,
    d.DEPARTMENT_NAME,
    COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
    FROM EMPLOYEE e1
    JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
    LEFT JOIN EMPLOYEE e2 
        ON e1.DEPARTMENT = e2.DEPARTMENT 
        AND e2.DOB > e1.DOB
    GROUP BY 
        e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
    ORDER BY 
        e1.EMP_ID DESC;
    """.strip()

    payload = {
        " finalQuery ": final_query
    }

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()

        return results
    except:
        print("Error occured while submitting solution")
        return None


def main():
    name = 'Piyush Motwani'
    reg_No = "EN21IT301076"
    email = "en21it301076@medicaps.ac.in"


    webhook_data = generate_wehook(name=name, reg_No=reg_No, email=email)

    if not webhook_data:
        print("Failed to generate webhook")
        return
    
    webhook_url = webhook_data.get("webhook")
    access_token = webhook_data.get("accessToken")



    submissions = submit_Solution(webhook_url=webhook_url, access_token= access_token)

    if submissions:
        print(f"Response generated from server {submissions}")
    
    else:
        print("Failed to submit the solution")



if __name__ == "__main__":
    main()

