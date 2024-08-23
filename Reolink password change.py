import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
import string

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def change_password(ip_address, old_password, new_password):
    # Construct the API URL for logging in
    url = f"https://{ip_address}/api.cgi?cmd=Login"
    
    # Create the payload containing the command and parameters for the login request
    payload = [{
        "cmd": "Login",
        "param": {
            "User": {
                "userName": "admin",
                "password": old_password,
                "Version": "0"
            }
        }
    }]
    
    try:
        # Send the login request and disable SSL certificate verification
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx response codes
        json_response = response.json()
        json_response = json_response[0]  # Extract the first item from the response list
        if json_response.get("code") != 0:
            raise Exception(f"API Error: {json_response.get('code')}")
        token = json_response.get("value").get("Token").get("name")  # Extract the authentication token
        
        # Construct the API URL for changing the user's password
        url = f"https://{ip_address}/api.cgi?cmd=ModifyUser&token={token}"
        # Create the payload containing the command and parameters for changing the password
        payload = [{
            "cmd": "ModifyUser",
            "action": 0,
            "param": {
                "User": {
                    "userName": "admin",
                    "newPassword": new_password,
                    "oldPassword": old_password
                }
            }
        }]
        # Send the password change request and disable SSL certificate verification
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx response codes
        json_response = response.json()
        json_response = json_response[0]  # Extract the first item from the response list
        if json_response.get("code") != 0:
            raise Exception(f"API Error: {json_response.get('code')}")
        print(f"Password for {ip_address} changed successfully.")
        return True  # Return True to indicate successful password change
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except ValueError:
        print("Invalid JSON response. Actual response:", response.text)
    except Exception as e:
        print(e)
        return False  # Return False to indicate failed password change


def main():
    # Display the warning and get confirmation
    print("WARNING: Whoever executes this script is responsible for:")
    print("1. All the changes which get made.")
    print("2. Registering the passwords on Devolution in the correct spot.")
    print("3. Ensuring that the password file does not get shared and does get deleted after the passwords are registered.")
    confirm = input("Please write 'confirm' to continue, or any other key to quit: ")
    
    # If the user does not confirm, stop the script
    if confirm.lower() != 'confirm':
        print("You did not confirm. The script will now exit.")
        return
    # Loop through the range of IP addresses
    for i in range(1, 255):
        ip_address = f"10.30.2.{i}"
        old_password = input(f"Enter old password for {ip_address}: ")
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))  # Change 10 to the desired password length
        success = change_password(ip_address, old_password, new_password)
        if success:
            with open("password_changes.txt", "a") as file:  # Open the file in append mode
                file.write(f"{ip_address}: {new_password}\n")  # Write the IP address and new password to the file
        else:
            continue_process = input("An error occurred. Do you want to continue? (yes/no): ")
            if continue_process.lower() != 'yes':
                break
    
    # Prompt to enter additional IP addresses manually
    additional_ips = input("Do you want to enter additional IP addresses manually? (yes/no): ")
    if additional_ips.lower() == 'yes':
        while True:
            ip_address = input("Enter the IP address: ")
            old_password = input(f"Enter old password for {ip_address}: ")
            new_password = input("Enter the new password: ")
            success = change_password(ip_address, old_password, new_password)
            if success:
                with open("password_changes.txt", "a") as file:  # Open the file in append mode
                    file.write(f"{ip_address}: {new_password}\n")  # Write the IP address and new password to the file
            continue_process = input("Do you want to enter more IP addresses? (yes/no): ")
            if continue_process.lower() != 'yes':
                break
    


main()
