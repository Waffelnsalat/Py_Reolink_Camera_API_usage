import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

username = "Surviellance"
password = "--------" #TODO Repace the - Symbols with the wished password

def get_token(ip_address, password):
    url = f"https://{ip_address}/api.cgi?cmd=Login"
    payload = [{
        "cmd": "Login",
        "param": {
            "User": {
                "userName": "admin",
                "password": password,
                "Version": "0"
            }
        }
    }]
    try:
        # Send a POST request to the login endpoint with the provided IP address and password
        response = requests.post(url, json=payload, verify=False)
        json_response = response.json()
        json_response = json_response[0]
        if json_response.get("code") == 0:
            # If the login is successful, return the authentication token
            return json_response.get("value").get("Token").get("name")
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., connection errors)
        print(f"Failed to connect to {ip_address}: {str(e)}")
    return None

def get_users(ip_address, token):
    url = f"https://{ip_address}/api.cgi?cmd=GetUser&token={token}"
    payload = [{"cmd": "GetUser", "action": 1}]
    try:
        # Send a POST request to retrieve the list of users with the provided IP address and token
        response = requests.post(url, json=payload, verify=False)
        json_response = response.json()
        json_response = json_response[0]
        if json_response.get("code") == 0:
            # If the request is successful, return a list of user names
            return [user.get("userName") for user in json_response.get("value").get("User")]
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., connection errors)
        print(f"Failed to connect to {ip_address}: {str(e)}")
    return None

def add_user(ip_address, token, username, password):
    url = f"https://{ip_address}/api.cgi?cmd=AddUser&token={token}"
    payload = [{
        "cmd": "AddUser",
        "param": {
            "User": {
                "userName": username,
                "password": password,
                "level": "guest"
            }
        }
    }]
    try:
        # Send a POST request to add a new user with the provided IP address, token, username, and password
        response = requests.post(url, json=payload, verify=False)
        json_response = response.json()
        json_response = json_response[0]
        if json_response.get("code") == 0:
            # If the user is added successfully, print a success message and return True
            print(f"User {username} added successfully on {ip_address}.")
            return True
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., connection errors)
        print(f"Failed to connect to {ip_address}: {str(e)}")
    # If adding the user fails, print an error message and return False
    print(f"Failed to add user {username} on {ip_address}.")
    return False

def main():
    
    # Loop through the range of IP addresses (10.30.2.1 to 10.30.2.254)
    for i in range(1, 255):
        ip_address = f"10.30.2.{i}"
        admin_password = input(f"Enter admin password for {ip_address}: ")
        token = get_token(ip_address, admin_password)
        
        # Handle the case where login fails
        if token is None:
            continue_process = input(f"Failed to login on {ip_address}. Do you want to continue? (yes/no): ")
            if continue_process.lower() != 'yes':
                break
            else:
                continue
        
        users = get_users(ip_address, token)
        print(users)
        
        # Handle the case where getting the user list fails
        if users is None:
            continue_process = input(f"Failed to get user list on {ip_address}. Do you want to continue? (yes/no): ")
            if continue_process.lower() != 'yes':
                break
        
        # Code for adding a user if it doesn't exist

        if username not in users:
            add_user(ip_address, token, username, password)

    # Prompt to enter additional IP addresses manually
    additional_ips = input("Do you want to enter additional IP addresses manually? (yes/no): ")
    if additional_ips.lower() == 'yes':
        while True:
            ip_address = input("Enter the IP address: ")
            admin_password = input(f"Enter admin password for {ip_address}: ")
            token = get_token(ip_address, admin_password)
            
            # Handle the case where login fails
            if token is None:
                continue_process = input(f"Failed to login on {ip_address}. Do you want to continue? (yes/no): ")
                if continue_process.lower() != 'yes':
                    break
                else:
                    continue
            
            users = get_users(ip_address, token)
            
            # Handle the case where getting the user list fails
            if users is None:
                continue_process = input(f"Failed to get user list on {ip_address}. Do you want to continue? (yes/no): ")
                if continue_process.lower() != 'yes':
                    break
            
            # Code for adding a user if it doesn't exist
            if username not in users:
                add_user(ip_address, token, username, password)

main()
