import argparse
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime 
   
print("QuickPod CLI Version 1.0.0.")
print("Copyright (C) 2025 Nathan McMinn. All Rights Reserved")
#Thank you for choosing QuickPod!
def unix_to_human_time(unix_time):
    if unix_time > 0:
        return datetime.utcfromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return 'N/A' 
def login():
    email = input("Enter your QuickPod Email:")
    password = input("Enter your QuickPod Password:")
    login_url = 'https://api.quickpod.io/api:2USncWkT/auth/login'
    credentials = {
        'email': email, 
        'password': password
    }
    response = requests.post(login_url, json=credentials)
    if response.status_code == 200:
        authToken = response.json().get('authToken')
        if authToken:
            print(f"Successfully logged in. AuthToken (First 4 digits): {authToken[:4]}")
            with open('.env', 'w') as f:
                f.write(f"authToken={authToken}")
            load_dotenv()
            print(authToken)
            print("Auth Token Stored successfully!")
            
        else:
            print("Error: AuthToken not found in the response.")
    else:
        print(f"Login failed. Status code: {response.status_code}")
        print(response.text)
def list_pods():
    if authToken:
        print(f"Using AuthToken (First Four Letters): {authToken[:4]}...")    
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        # Send GET request to list pods
        response = requests.get(pods_url, headers=headers)    
        if response.status_code == 200:
            print("Pod List:")
            try:
                mypods = response.json()
                if isinstance(mypods, list):
                    for pod in mypods:
                        last_seen_unix = pod.get('last_seen', 0)
                        last_billed_unix = pod.get('last_billed', 0)
                        ssh_private_key = pod.get('ssh_private_key', 'N/A')
                        last_seen = unix_to_human_time(last_seen_unix)
                        last_billed = unix_to_human_time(last_billed_unix)
                        print(f"Pod ID: {pod['id']}")
                        print(f"Created At: {pod['CreatedAt']}")
                        print(f"Command: {pod['Command']}")
                        print(f"Docker ID: {pod['docker_ID']}")
                        print(f"Image: {pod['Image']}")
                        print(f"Status: {pod['Status']}")
                        print(f"State: {pod['State']}")
                        print(f"Running For: {pod['RunningFor']}")
                        print(f"Public IP Address: {pod['public_ipaddr']}")
                        print(f"Pod Type: {pod['pod_type']}")
                        print(f"Last Seen: {last_seen}")
                        print(f"Last Billed: {last_billed}")
                        print(f"SSH Private Key: {pod['ssh_private_key']}")
                        print("-" * 40)  # Separator for readability
                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_machines():
    if authToken:
        print(f"Using AuthToken (First Four Letters): {authToken[:4]}...")
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mymachines'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(pods_url, headers=headers)
        if response.status_code == 200:
            try:
                mymachines = response.json()
                if isinstance(mymachines, list):
                    for machine in mymachines:
                        created_at_unix = machine.get('created_at', 0)
                        created_at = unix_to_human_time(created_at_unix)
                        print("=" * 40)
                        print("Machine Details:")
                        print(f"Machine ID: {machine['id']}")
                        print(f"Hostname: {machine['hostname']}")
                        print(f"Created At: {created_at}")
                        print(f"CPU Name: {machine['cpu_name']}")
                        print(f"CPU Cores: {machine['cpu_cores']}")
                        print(f"CPU RAM: {machine['cpu_ram']} GB")
                        print(f"Geolocation: {machine['geolocation']}")
                        print(f"Public IP: {machine['public_ipaddr']}")
                        print(f"Online: {'Yes' if machine['online'] else 'No'}")
                        print(f"Performance Score: {machine['perf_score']}")
                        print(f"Reliability: {machine['reliability']}")
                        print(f"Listed: {'Yes' if machine['listed'] else 'No'}")
                        print(f"Max Duration: {machine['max_duration']} Days")
                        print(f"Machine Type: {machine['machine_type']}")
                        print("=" * 40)
                        if '_machines' in machine and isinstance(machine['_machines'], list):
                            print("GPU Details:")
                            for gpu in machine['_machines']:
                                last_seen_unix = gpu.get('last_seen', 0)
                                last_seen = unix_to_human_time(last_seen_unix)
                                print(f"GPU Machine ID: {gpu['id']}")
                                print(f"GPU Name: {gpu['gpu_name']}")
                                print(f"GPU VRAM: {gpu['gpu_vram']} MB")
                                print(f"GPU Utilization: {gpu['utilization_gpu']}%")
                                print(f"GPU Clock Speed: {gpu['gpu_clock']}")
                                print(f"GPU Power Draw: {gpu['power_draw']} W")
                                print(f"Last Seen: {last_seen}")
                                print(f"Job Label: {gpu['job_label']}")
                                print(f"Online: {'Yes' if gpu['online'] else 'No'}")
                                print("-" * 40)
                        else:
                            print("No GPU machine data found in '_machines'.")
                else:
                    print("Error: Expected a list of machines, but received a different structure.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def print_auth_token():
    print(f"AuthToken: {authToken}")
def set_auth_token():
    newauthToken = input("Paste your authToken here:")
    with open('.env', 'w') as f:
        f.write(f"authToken={newauthToken}")
    load_dotenv()
    print("setting new auth token")
def delete_auth_token():
    dotenv_file = '.env'
    if os.path.exists(dotenv_file):
        try:
            os.remove(dotenv_file)  
            print("the Auth Token has been deleted.")
            exit()
        except Exception as e:
            print(f"An error occurred while deleting {dotenv_file}: {e}")
            exit()
    else:
        print(f"{dotenv_file} does not exist.")
        exit()

parser = argparse.ArgumentParser(description="Command-line utility for managing machines and jobs")

parser.add_argument(
    '--authtoken',
    type=str,
    help="Set a temporary auth token. This will not be stored and the existing stored authtoken will not be affected."
)
parser.add_argument(
    '--bypass-login',
    action="store_true",
    help="Send API calls without asking for authentication. This is simply a bypass, the API calls WILL NOT go through. "
)
subparsers = parser.add_subparsers(help="Available categories of commands")

auth_parser = subparsers.add_parser('auth', help="Authentication commands")
auth_subparsers = auth_parser.add_subparsers(help="Authentication subcommands")

auth_subparsers.add_parser('login', help="Log in and store the API key").set_defaults(func=login)
auth_subparsers.add_parser('delete-auth-token', help="Remove the Auth Token. You will need to authenticate again to access anything.").set_defaults(func=delete_auth_token)
auth_subparsers.add_parser('print-auth-token', help="Display the currently stored 403-character auth token and exit.").set_defaults(func=print_auth_token)
auth_subparsers.add_parser('set-auth-token', help="Enter your own 403-character authToken and exit.").set_defaults(func=set_auth_token)

clients_parser = subparsers.add_parser('clients', help="Client Commands")
clients_subparsers = clients_parser.add_subparsers(help="Client subcommands")

clients_subparsers.add_parser('listpods', help="List all pods with details.").set_defaults(func=list_pods)

hosts_parser = subparsers.add_parser('hosts', help="Host Commands")
hosts_subparsers = hosts_parser.add_subparsers(help="Host subcommands")

showmachines_parser = hosts_subparsers.add_parser('listmachines', help="")
showmachines_parser.set_defaults(func=list_machines)

args = parser.parse_args()
load_dotenv()
authToken = os.getenv("authToken")

if args.authtoken: #Login enforcement
    authToken = args.authtoken
    print(authToken)
elif authToken:
    pass
elif args.bypass_login:
    pass
else:
    print("You are not logged in!")
    login()
    load_dotenv()
    authToken = os.getenv("authToken")

if hasattr(args, 'func'):
    args.func()
else:
    parser.print_help()