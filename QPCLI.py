import argparse
import sys
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime 
import csv
import pandas as pd

#print("QuickPod CLI 1.3.1.")
#print("Copyright (C) 2025 QuickPod. All Rights Reserved")
#Thank you for choosing QuickPod!
fail_counter = 0 #Counter for repetitive API fails.
def unix_to_human_time(unix_time): #Only used in old commands; Any command can be modified from (var) --> unix_to_human_time(var) MUST BE A TIME or will fail.
    if unix_time > 0:
        return datetime.utcfromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return unix_time 
def auto_login(): #Auto login enforcement if an API call has failed.
    global fail_counter
    api_key = os.getenv("api_key")
    if api_key: #If API key exists:
        login_url = 'https://api.quickpod.org/update/auth/apikeylogin'
        credentials = {
            'api_key': api_key, 
        }
        try:
            response = requests.post(login_url, json=credentials) #Sends POST to the API.
        except Exception as e: # If it fails:
            if fail_counter > 2: #Gives it three attemps to succeed before quitting.
                print(f"API refused the call.{e}")
                print(f"Program has failed three times in a row.")
                print("ending.")
                login()
            else:
                retry_login(response)
        if response.status_code == 200: #If success:
            authToken = response.json().get('authToken') # Use the new authToken instead of the old one.
            if authToken:
                with open('.env', 'w') as f:
                    f.write(f"authToken={authToken}\n")  # Saves the new authToken for future command runs.
                with open('.env', 'a') as f:
                    f.write(f"api_key={api_key}\n") # Saves the correctly used api_key. The above command wipes the .env file so this must be rewritten.
                load_dotenv() #Saves / Loads the new variables
                os.environ['authToken'] = authToken
                os.environ['api_key'] = api_key
                script_path = sys.argv[0]
                arguments = sys.argv[1:]
                os.execv(sys.executable, [sys.executable] + [script_path] + arguments)
            else:
                print("No authtoken")
                login()
        elif response.status_code == 401: # 401 = AUTH ERROR.
            print("401. Bad login method.") #Bad login method.
            login()
        else:
            print(response.status_code) # Otherwise it prints the response code.
            retry_login(response)                 
    else:
        pass
    print("no api key")
    email = os.getenv("email")
    password = os.getenv("password")
    if email:
        login_url = 'https://api.quickpod.org/update/auth/login'
        credentials = {
            'email': email, 
            'password': password,
            }
        try:
            response = requests.post(login_url, json=credentials) # Sends POST request
        except Exception as e:
            fail_reason = response
            if fail_counter > 2: # If it fails 3 times:
                print(f"API refused the call.{e}") 
                print(f"Program has failed three times in a row.")
                print("ending.")
                login() # Send back to login
            else:
                fail_counter = fail_counter + 1
                exec(open(sys.argv[0]).read())
        if response.status_code == 200: # If success:
            authToken = response.json().get('authToken') # Gets authToken from the response.
            if authToken:
                with open('.env', 'w') as f:
                    f.write(f"authToken={authToken}\n")  # Writes the new authtoken
                with open('.env', 'a') as f:
                    f.write(f"email={email}\n") # Write successful email
                with open('.env', 'a') as f:
                    f.write(f"password={password}\n") # Write successful password
                load_dotenv()
                os.environ['authToken'] = authToken
                os.environ['email'] = email
                os.environ['password'] = password
                script_path = sys.argv[0]
                arguments = sys.argv[1:]
                os.execv(sys.executable, [sys.executable] + [script_path] + arguments)
            else:
                parser.print_help() # Otherwise prints help as a backup.
                exit()
        elif response.status_code == 401: # 401 = AUTH ERROR.
            print("401. Bad login method.") #Bad login method.
            login()
        else:
            #print(response.status_code) # Otherwise it prints the response code.
            retry_login()
    else:
        print("Authtoken expired. No method of login stored.") # If it doesn't exist then it forces login.
        login()
def retry_login(fail_reason):
    global fail_counter
    print("failed")
    print(fail_counter)
    fail_counter = fail_counter + 1
    if fail_counter > 2: # If it fails 3 times:
        print(f"Program has failed to login three times in a row.")
        print(fail_reason)
        print("login.")
        login()
    else:
        auto_login()
def login(): #Normal login or backup requires user input.
    login_method = input("Enter your QuickPod Email Or API Key Or Auth Token:") # Asks for login info
    if len(login_method) == 36: #If API Key:
        api_key = login_method #Stores APIKEY as the login Method.
        print("Logging in with API Key.")
        login_url = 'https://api.quickpod.org/update/auth/apikeylogin'
        credentials = {
            'api_key': api_key, 
        }
        response = requests.post(login_url, json=credentials) # Sends POST request
        if response.status_code == 200: # If success
            authToken = response.json().get('authToken') # Saves new authToken
            with open('.env', 'w') as f:
                f.write(f"authToken={authToken}\n")  # Saves authtoken in the .env
            with open('.env', 'a') as f:
                f.write(f"api_key={api_key}\n") # Saves api_key in the .env
            load_dotenv() # Saves/loads .env
            print("Auth Token Stored successfully!") # Success!
            os.environ['authToken'] = authToken
            os.environ['api_key'] = api_key
            script_path = sys.argv[0]
            arguments = sys.argv[1:]
            os.execv(sys.executable, [sys.executable] + [script_path] + arguments)
    elif len(login_method) > 300: # Will be removed in the next update. Saves a likely invalid key.
        print("WARNING: authTokens are refreshed every 24 hours. You will likely have issues with this!!!")
        newauthtoken = login_method
        print("Setting Auth Token...")
        print("Note that authtokens expire every 24 hours.")
        with open('.env', 'w') as f:
            f.write(f"authToken={newauthtoken}") # Saves authToken in the .env
        load_dotenv() # Saves / Loads .env
        os.environ['authToken'] = authToken
        script_path = sys.argv[0]
        arguments = sys.argv[1:]
        os.execv(sys.executable, [sys.executable] + [script_path] + arguments)
    else:
        print("Using Email / Password Authentication") # Email/passwd auth as a last resort.
        email = login_method
        password = input("Enter your QuickPod Password:") 
        login_url = 'https://api.quickpod.org/update/auth/login'
        credentials = {
            'email': email, 
            'password': password
        }
        response = requests.post(login_url, json=credentials) # Sends POST request.
        if response.status_code == 200: # If Success:
            authToken = response.json().get('authToken') # Gets authtoken from response.
            if authToken: # A check for if authToken is in the response.
                with open('.env', 'w') as f: 
                    f.write(f"authToken={authToken}\n")  #Writes authToken to .env for future commands.
                with open('.env', 'a') as f:
                    f.write(f"email={email}\n") # Writes successful email to .env for future commands.
                with open('.env', 'a') as f:
                    f.write(f"password={password}\n") # Writes successful password to .env for future commands.
                load_dotenv()
                print("Auth Token Stored successfully!")
                os.environ['authToken'] = authToken
                os.environ['email'] = email
                os.environ['password'] = password
                script_path = sys.argv[0]
                arguments = sys.argv[1:]
                os.execv(sys.executable, [sys.executable] + [script_path] + arguments)
            else:
                print("Error: AuthToken not found in the response.")
        else:
            print(f"Login failed. Status code: {response.status_code}") #If failed print response code.
            print(response.text)
            exit()
def search_all():
    if silent:
        pass
    else:
        print("Available Machines:") 
    search() # Runs the normal search (GPU) function.
    if silent:
        pass
    else:
        print("NOT Available Machines:")
    if args.csv:
        pods_url = 'https://api.quickpod.org/notrentable'
        params = {
            'num_gpus': args.num_gpus,
            'max_hourly_cost': args.max_hourly_cost,
            'disk_space': args.disk_space,
            'reliability': args.reliability,
            'duration': args.duration,
            'gpu_type': args.gpu_type,
            'location': args.location,
            'sort_by' : args.sortby,
        }

        response = requests.get(pods_url, params=params) # Send GET request using the required filters.
        if response.status_code == 200: # If success:
            try:
                offers = response.json() # Parse response.
                with open(f'{csv_name}.csv', mode='a', newline='', encoding='utf-8') as csvfile: # Make a CSV File.
                    writer = csv.writer(csvfile)
                    header = ([
                        'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                        'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                        'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                        'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                        'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                    ]) # Write the Header to the CSV File.
                    for offer in offers: # For every offer repeat:
                        machines = offer.get('_machines', []) #Gets the _machines section of the offers response.
                        for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                            globals()[key] = value 
                        row = [
                            offer.get('offer_name', 'N/A'),
                            offer.get('id', 'N/A'),
                            offer.get('machines_id', 'N/A'),
                            user_id,
                            verification,
                            geolocation,
                            geoinfo,
                            inet_down,
                            inet_up,
                            reliability,
                            max_duration,
                            offer.get('offer_type', 'N/A'),
                            cpu_name,
                            offer.get('memory', 'N/A'),
                            offer.get('cpus', 'N/A'),
                            cpu_frequency,
                            offer.get('hourly_cost', 'N/A'),
                            offer.get('tflops_per_dollar', 'N/A'),
                            offer.get('perf_per_dollar', 'N/A'),
                            offer.get('gpu_type', 'N/A'),
                            offer.get('num_gpus', 'N/A'),
                            offer.get('tflops', 'N/A'),
                            max_cuda,
                            offer.get('gpu_vram', 'N/A'),
                            offer.get('gpu_pcie', 'N/A'),
                            bw_dev_cpu,
                            offer.get('gpu_lanes', 'N/A'),
                            offer.get('max_disk_size', 'N/A'),
                            offer.get('ports_count', 'N/A'),
                            perf_score,
                            unix_to_human_time(offer.get('created_at')),
                            offer.get('occupied', 'N/A'),
                            unix_to_human_time(offer.get('last_updated')),
                            offer.get('onjob', 'N/A'),
                            ubuntu_version,
                            cpu_arch,
                            current_rentals_resident,
                            current_rentals_on_demand
                        ]
                        writer.writerow(row) # With some information fotten from the _machines section and some from the outside response creates a row in the CSV.
            except Exception as e:
                print(f"Error parsing JSON response: {e}") # Prints the error.
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error status code.
        if silent:
            pass
        else:
            print(f"Appended to {csv_name}.csv!") # Confirmation message. Must append to the CSV file instead of overriding.
    else:
        search_notrentable() # IF CSV is not selected continues with normal search_notrentable function.
def search(): # Offers Search function
    pods_url = 'https://api.quickpod.org/rentable'
    params = {
        'num_gpus': args.num_gpus,
        'max_hourly_cost': args.max_hourly_cost,
        'disk_space': args.disk_space,
        'reliability': args.reliability,
        'duration': args.duration,
        'gpu_type': args.gpu_type,
        'location': args.location,
        'sort_by' : args.sortby,
    }

    response = requests.get(pods_url, params=params) # Sends a GET request with the required filters.
    if response.status_code == 200: # If success:
        try:
            offers = response.json() # Parses JSON
            if args.csv:
                with open(f'{csv_name}.csv', mode='w', newline='', encoding='utf-8') as csvfile: # Creates a new CSV file.
                    writer = csv.writer(csvfile)
                    header = ([
                        'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                        'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                        'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                        'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                        'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                    ])
                    writer.writerow(header) # Writes the header.
                    for offer in offers: # For every offer:
                        machines = offer.get('_machines', []) #Gets the _machines section of the offers response
                        for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                            globals()[key] = value
                        row = [
                            offer.get('offer_name', 'N/A'),
                            offer.get('id', 'N/A'),
                            offer.get('machines_id', 'N/A'),
                            user_id,
                            verification,
                            geolocation,
                            geoinfo,
                            inet_down,
                            inet_up,
                            reliability,
                            max_duration,
                            offer.get('offer_type', 'N/A'),
                            cpu_name,
                            offer.get('memory', 'N/A'),
                            offer.get('cpus', 'N/A'),
                            cpu_frequency,
                            offer.get('hourly_cost', 'N/A'),
                            offer.get('tflops_per_dollar', 'N/A'),
                            offer.get('perf_per_dollar', 'N/A'),
                            offer.get('gpu_type', 'N/A'),
                            offer.get('num_gpus', 'N/A'),
                            offer.get('tflops', 'N/A'),
                            max_cuda,
                            offer.get('gpu_vram', 'N/A'),
                            offer.get('gpu_pcie', 'N/A'),
                            bw_dev_cpu,
                            offer.get('gpu_lanes', 'N/A'),
                            offer.get('max_disk_size', 'N/A'),
                            offer.get('ports_count', 'N/A'),
                            perf_score,
                            unix_to_human_time(offer.get('created_at')),
                            offer.get('occupied', 'N/A'),
                            unix_to_human_time(offer.get('last_updated')),
                            offer.get('onjob', 'N/A'),
                            ubuntu_version,
                            cpu_arch,
                            current_rentals_resident,
                            current_rentals_on_demand
                        ]
                        writer.writerow(row) # Writes one row if the CSV
                if silent:
                    pass
                else:
                    print(f"Saved to {csv_name}.csv!") # Confirmation message
            elif args.json:
                json_parser(offers) # Sends to the JSON Parser which will output the response.
            elif args.raw:
                print(offers) # Outputs the raw API string.
            elif args.list: # Old method, not reccomended. Use JSON instead.
                for offer in offers: # For every offer
                    machines = offer.get('_machines', []) # Gets the _machines section of the API response.
                    for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                        globals()[key] = value
                    print("--------Machine Overview--------") # Prints each line individually.
                    print(f"Offer Name: {offer.get('offer_name', 'N/A')}")
                    print(f"Offer ID: {offer.get('id', 'N/A')}")
                    print(f"Machine ID: {offer.get('machines_id', 'N/A')}")
                    print(f"Host: {user_id}")
                    print(f"Verified: {verification}")
                    print(f"Location: {geolocation}")
                    print(f"Location Details: {geoinfo}")
                    print(f"Internet Download Speed: {inet_down}")
                    print(f"Internet Upload Speed: {inet_up}")
                    print(f"Reliability: {reliability}")
                    print(f"Max Duration: {max_duration}")
                    print(f"Offer Type: {offer.get('offer_type', 'N/A')}")
                    print(f"CPU Name: {cpu_name}")
                    print(f"Memory: {offer.get('memory', 'N/A')} GB")
                    print(f"CPUs: {offer.get('cpus', 'N/A')}")
                    print(f"CPU Frequency: {cpu_frequency}")
                    print(f"Hourly Cost: ${offer.get('hourly_cost', 'N/A')}")
                    print(f"TFLops per Dollar: {offer.get('tflops_per_dollar', 'N/A')}")
                    print(f"Perf per Dollar: {offer.get('perf_per_dollar', 'N/A')}")

                    print("--------Machine Details--------")
                    print(f"GPU Type: {offer.get('gpu_type', 'N/A')}")
                    print(f"Num GPUs: {offer.get('num_gpus', 'N/A')}")
                    print(f"TFLops: {offer.get('tflops', 'N/A')}")
                    print(f"Max CUDA Version: {max_cuda}")
                    print(f"GPU VRAM: {offer.get('gpu_vram', 'N/A')} MB")
                    print(f"GPU PCIe Version: {offer.get('gpu_pcie', 'N/A')}")
                    print(f"PCIE Speed: {bw_dev_cpu}")
                    print(f"GPU PCIe Lanes: {offer.get('gpu_lanes', 'N/A')}")
                    print(f"Max Disk Size: {offer.get('max_disk_size', 'N/A')} GB")
                    print(f"Ports Count: {offer.get('ports_count', 'N/A')}")
                    print(f"Perf Score: {perf_score}")

                    print("--------Advanced--------")
                    created_at_human = unix_to_human_time(offer.get('created_at'))
                    last_updated_human = unix_to_human_time(offer.get('last_updated'))
                    print(f"Created At: {created_at_human}")
                    print(f"Occupied: {offer.get('occupied', 'N/A')}")
                    print(f"Last Updated: {last_updated_human}")
                    print(f"On Job: {offer.get('onjob', 'N/A')}")
                    print(f"Ubuntu Version: {ubuntu_version}")
                    print(f"CPU Architecture: {cpu_arch}")
                    print(f"Current Rentals Stored: {current_rentals_resident}")
                    print(f"Current Rentals Running: {current_rentals_on_demand}")
            else:
                if not offers: # If offers does not exist:
                    print("No Available Machines!")
                else: # Default option, in shell table format.
                    pd.set_option('display.width', 1000)
                    pd.set_option('display.max_columns', None)
                    pd.set_option('display.max_rows', None)
                    list = pd.DataFrame(offers) # Creates a list.
                    print(list[['id', 'offer_name', 'machines_id', 'hourly_cost', 'cpus', 'memory', 'max_disk_size', 'num_gpus', 'gpu_vram', 'gpu_pcie', 'gpu_lanes', 'tflops', 'onjob', 'occupied']].to_string(index=False)) # Prints the list with only certain rows.

        except Exception as e: # If it fails:
            print(f"Error parsing JSON response: {e}") # State the error.
    elif response.status_code == 401:
        auto_login()
    else:
        print(f"Failed to fetch pods. Status code: {response.status_code}") # Print the response failure code.
def search_cpu():
    pods_url = 'https://api.quickpod.org/rentable_cpu'
    params = {
        'num_gpus': args.num_cpus,
        'max_hourly_cost': args.max_hourly_cost,
        'disk_space': args.disk_space,
        'reliability': args.reliability,
        'duration': args.duration,
        'gpu_type': args.cpu_type,
        'location': args.location,
        'sort_by' : args.sortby,
    } 

    response = requests.get(pods_url, params=params) # Sends a GET request to the API
    if response.status_code == 200: # If Success:
        try:
            offers = response.json() # Parses offers
            if args.json:
                json_parser(offers)
            elif args.raw:
                print(offers)
            else:
                for offer in offers: # For every offer:
                    machines = offer.get('_machines', []) # gets _machines section of API response.
                    for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                        globals()[key] = value
                    print("--------Machine Overview--------")
                    print(f"Offer Name: {offer.get('offer_name', 'N/A')}")
                    print(f"Offer ID: {offer.get('id', 'N/A')}")
                    print(f"Machine ID: {offer.get('machines_id', 'N/A')}")
                    print(f"Host: {user_id}")
                    print(f"Verified: {verification}")
                    print(f"Location: {geolocation}")
                    print(f"Location Details: {geoinfo}")
                    print(f"Internet Download Speed: {inet_down}")
                    print(f"Internet Upload Speed: {inet_up}")
                    print(f"Reliability: {reliability}")
                    print(f"Max Duration: {max_duration}")
                    print(f"Offer Type: {offer.get('offer_type', 'N/A')}")
                    print(f"CPU Name: {cpu_name}")
                    print(f"Memory: {offer.get('memory', 'N/A')} GB")
                    print(f"CPUs: {offer.get('cpus', 'N/A')}")
                    print(f"CPU Frequency: {cpu_frequency}")
                    print(f"Hourly Cost: ${offer.get('hourly_cost', 'N/A')}")
                    print(f"TFLops per Dollar: {offer.get('tflops_per_dollar', 'N/A')}")
                    print(f"Perf per Dollar: {offer.get('perf_per_dollar', 'N/A')}")

                    print("--------Machine Details--------")
                    print(f"GPU Type: {offer.get('gpu_type', 'N/A')}")
                    print(f"Num GPUs: {offer.get('num_gpus', 'N/A')}")
                    print(f"TFLops: {offer.get('tflops', 'N/A')}")
                    print(f"Max CUDA Version: {max_cuda}")
                    print(f"GPU VRAM: {offer.get('gpu_vram', 'N/A')} MB")
                    print(f"GPU PCIe Version: {offer.get('gpu_pcie', 'N/A')}")
                    print(f"PCIE Speed: {bw_dev_cpu}")
                    print(f"GPU PCIe Lanes: {offer.get('gpu_lanes', 'N/A')}")
                    print(f"Max Disk Size: {offer.get('max_disk_size', 'N/A')} GB")
                    print(f"Ports Count: {offer.get('ports_count', 'N/A')}")
                    print(f"Perf Score: {perf_score}")

                    print("--------Advanced--------")
                    created_at_human = unix_to_human_time(offer.get('created_at'))
                    last_updated_human = unix_to_human_time(offer.get('last_updated'))
                    print(f"Created At: {created_at_human}")
                    print(f"Occupied: {offer.get('occupied', 'N/A')}")
                    print(f"Last Updated: {last_updated_human}")
                    print(f"On Job: {offer.get('onjob', 'N/A')}")
                    print(f"Ubuntu Version: {ubuntu_version}")
                    print(f"CPU Architecture: {cpu_arch}")
                    print(f"Current Rentals Stored: {current_rentals_resident}")
                    print(f"Current Rentals Running: {current_rentals_on_demand}")
        except Exception as e: # If it fails:
            print(f"Error parsing JSON response: {e}") # Prints the error.
    elif response.status_code == 401:
            auto_login()
    else:
        print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error status code.
def search_notrentable():
    pods_url = 'https://api.quickpod.org/notrentable'
    params = {
        'num_gpus': args.num_gpus,
        'max_hourly_cost': args.max_hourly_cost,
        'disk_space': args.disk_space,
        'reliability': args.reliability,
        'duration': args.duration,
        'gpu_type': args.gpu_type,
        'location': args.location,
        'sort_by' : args.sortby,
    }

    response = requests.get(pods_url, params=params) # Sends a GET request with the required filters.
    print(response)
    if response.status_code == 200: # If success:
        try:
            offers = response.json() # Parses JSON
            print(offers)
            if args.csv:
                with open(f'{csv_name}.csv', mode='w', newline='', encoding='utf-8') as csvfile: # Creates a new CSV file.
                    writer = csv.writer(csvfile)
                    header = ([
                        'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                        'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                        'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                        'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                        'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                    ])
                    writer.writerow(header) # Writes the header.
                    for offer in offers: # For every offer:
                        machines = offer.get('_machines', []) #Gets the _machines section of the offers response
                        for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                            globals()[key] = value
                        row = [
                            offer.get('offer_name', 'N/A'),
                            offer.get('id', 'N/A'),
                            offer.get('machines_id', 'N/A'),
                            user_id,
                            verification,
                            geolocation,
                            geoinfo,
                            inet_down,
                            inet_up,
                            reliability,
                            max_duration,
                            offer.get('offer_type', 'N/A'),
                            cpu_name,
                            offer.get('memory', 'N/A'),
                            offer.get('cpus', 'N/A'),
                            cpu_frequency,
                            offer.get('hourly_cost', 'N/A'),
                            offer.get('tflops_per_dollar', 'N/A'),
                            offer.get('perf_per_dollar', 'N/A'),
                            offer.get('gpu_type', 'N/A'),
                            offer.get('num_gpus', 'N/A'),
                            offer.get('tflops', 'N/A'),
                            max_cuda,
                            offer.get('gpu_vram', 'N/A'),
                            offer.get('gpu_pcie', 'N/A'),
                            bw_dev_cpu,
                            offer.get('gpu_lanes', 'N/A'),
                            offer.get('max_disk_size', 'N/A'),
                            offer.get('ports_count', 'N/A'),
                            perf_score,
                            unix_to_human_time(offer.get('created_at')),
                            offer.get('occupied', 'N/A'),
                            unix_to_human_time(offer.get('last_updated')),
                            offer.get('onjob', 'N/A'),
                            ubuntu_version,
                            cpu_arch,
                            current_rentals_resident,
                            current_rentals_on_demand
                        ]
                        writer.writerow(row) # Writes one row if the CSV
                if silent:
                    pass
                else:
                    print(f"Saved to {csv_name}.csv!") # Confirmation message
            elif args.json:
                json_parser(offers) # Sends to the JSON Parser which will output the response.
            elif args.raw:
                print(offers) # Outputs the raw API string.
            elif args.list: # Old method, not reccomended. Use JSON instead.
                for offer in offers: # For every offer
                    machines = offer.get('_machines', []) # Gets the _machines section of the API response.
                    for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                        globals()[key] = value
                    print("--------Machine Overview--------") # Prints each line individually.
                    print(f"Offer Name: {offer.get('offer_name', 'N/A')}")
                    print(f"Offer ID: {offer.get('id', 'N/A')}")
                    print(f"Machine ID: {offer.get('machines_id', 'N/A')}")
                    print(f"Host: {user_id}")
                    print(f"Verified: {verification}")
                    print(f"Location: {geolocation}")
                    print(f"Location Details: {geoinfo}")
                    print(f"Internet Download Speed: {inet_down}")
                    print(f"Internet Upload Speed: {inet_up}")
                    print(f"Reliability: {reliability}")
                    print(f"Max Duration: {max_duration}")
                    print(f"Offer Type: {offer.get('offer_type', 'N/A')}")
                    print(f"CPU Name: {cpu_name}")
                    print(f"Memory: {offer.get('memory', 'N/A')} GB")
                    print(f"CPUs: {offer.get('cpus', 'N/A')}")
                    print(f"CPU Frequency: {cpu_frequency}")
                    print(f"Hourly Cost: ${offer.get('hourly_cost', 'N/A')}")
                    print(f"TFLops per Dollar: {offer.get('tflops_per_dollar', 'N/A')}")
                    print(f"Perf per Dollar: {offer.get('perf_per_dollar', 'N/A')}")

                    print("--------Machine Details--------")
                    print(f"GPU Type: {offer.get('gpu_type', 'N/A')}")
                    print(f"Num GPUs: {offer.get('num_gpus', 'N/A')}")
                    print(f"TFLops: {offer.get('tflops', 'N/A')}")
                    print(f"Max CUDA Version: {max_cuda}")
                    print(f"GPU VRAM: {offer.get('gpu_vram', 'N/A')} MB")
                    print(f"GPU PCIe Version: {offer.get('gpu_pcie', 'N/A')}")
                    print(f"PCIE Speed: {bw_dev_cpu}")
                    print(f"GPU PCIe Lanes: {offer.get('gpu_lanes', 'N/A')}")
                    print(f"Max Disk Size: {offer.get('max_disk_size', 'N/A')} GB")
                    print(f"Ports Count: {offer.get('ports_count', 'N/A')}")
                    print(f"Perf Score: {perf_score}")

                    print("--------Advanced--------")
                    created_at_human = unix_to_human_time(offer.get('created_at'))
                    last_updated_human = unix_to_human_time(offer.get('last_updated'))
                    print(f"Created At: {created_at_human}")
                    print(f"Occupied: {offer.get('occupied', 'N/A')}")
                    print(f"Last Updated: {last_updated_human}")
                    print(f"On Job: {offer.get('onjob', 'N/A')}")
                    print(f"Ubuntu Version: {ubuntu_version}")
                    print(f"CPU Architecture: {cpu_arch}")
                    print(f"Current Rentals Stored: {current_rentals_resident}")
                    print(f"Current Rentals Running: {current_rentals_on_demand}")
            else:
                if not offers: # If offers does not exist:
                    print("No Available Machines!")
                else: # Default option, in shell table format.
                    pd.set_option('display.width', 1000)
                    pd.set_option('display.max_columns', None)
                    pd.set_option('display.max_rows', None)
                    list = pd.DataFrame(offers) # Creates a list.
                    print(list[['id', 'offer_name', 'machines_id', 'hourly_cost', 'cpus', 'memory', 'max_disk_size', 'num_gpus', 'gpu_vram', 'gpu_pcie', 'gpu_lanes', 'tflops', 'onjob', 'occupied']].to_string(index=False)) # Prints the list with only certain rows.

        except Exception as e: # If it fails:
            print(f"Error parsing JSON response: {e}") # State the error.
    elif response.status_code == 401:
            auto_login()
    else:
        print(f"Failed to fetch pods. Status code: {response.status_code}") # Print the response failure code.
def search_notrentable_cpu():
    pods_url = 'https://api.quickpod.org/notrentable_cpu'
    params = {
        'num_gpus': args.num_cpus,
        'max_hourly_cost': args.max_hourly_cost,
        'disk_space': args.disk_space,
        'reliability': args.reliability,
        'duration': args.duration,
        'gpu_type': args.cpu_type,
        'location': args.location,
        'sort_by' : args.sortby,
    } 

    response = requests.get(pods_url, params=params) # Sends a GET request to the API
    if response.status_code == 200: # If Success:
        try:
            offers = response.json() # Parses offers
            if args.json:
                json_parser(offers)
            elif args.raw:
                print(offers)
            else:
                for offer in offers: # For every offer:
                    machines = offer.get('_machines', []) # gets _machines section of API response.
                    for key, value in machines.items(): # Assigns the corresponding variables to the json response.
                        globals()[key] = value
                    print("--------Machine Overview--------")
                    print(f"Offer Name: {offer.get('offer_name', 'N/A')}")
                    print(f"Offer ID: {offer.get('id', 'N/A')}")
                    print(f"Machine ID: {offer.get('machines_id', 'N/A')}")
                    print(f"Host: {user_id}")
                    print(f"Verified: {verification}")
                    print(f"Location: {geolocation}")
                    print(f"Location Details: {geoinfo}")
                    print(f"Internet Download Speed: {inet_down}")
                    print(f"Internet Upload Speed: {inet_up}")
                    print(f"Reliability: {reliability}")
                    print(f"Max Duration: {max_duration}")
                    print(f"Offer Type: {offer.get('offer_type', 'N/A')}")
                    print(f"CPU Name: {cpu_name}")
                    print(f"Memory: {offer.get('memory', 'N/A')} GB")
                    print(f"CPUs: {offer.get('cpus', 'N/A')}")
                    print(f"CPU Frequency: {cpu_frequency}")
                    print(f"Hourly Cost: ${offer.get('hourly_cost', 'N/A')}")
                    print(f"TFLops per Dollar: {offer.get('tflops_per_dollar', 'N/A')}")
                    print(f"Perf per Dollar: {offer.get('perf_per_dollar', 'N/A')}")

                    print("--------Machine Details--------")
                    print(f"GPU Type: {offer.get('gpu_type', 'N/A')}")
                    print(f"Num GPUs: {offer.get('num_gpus', 'N/A')}")
                    print(f"TFLops: {offer.get('tflops', 'N/A')}")
                    print(f"Max CUDA Version: {max_cuda}")
                    print(f"GPU VRAM: {offer.get('gpu_vram', 'N/A')} MB")
                    print(f"GPU PCIe Version: {offer.get('gpu_pcie', 'N/A')}")
                    print(f"PCIE Speed: {bw_dev_cpu}")
                    print(f"GPU PCIe Lanes: {offer.get('gpu_lanes', 'N/A')}")
                    print(f"Max Disk Size: {offer.get('max_disk_size', 'N/A')} GB")
                    print(f"Ports Count: {offer.get('ports_count', 'N/A')}")
                    print(f"Perf Score: {perf_score}")

                    print("--------Advanced--------")
                    created_at_human = unix_to_human_time(offer.get('created_at'))
                    last_updated_human = unix_to_human_time(offer.get('last_updated'))
                    print(f"Created At: {created_at_human}")
                    print(f"Occupied: {offer.get('occupied', 'N/A')}")
                    print(f"Last Updated: {last_updated_human}")
                    print(f"On Job: {offer.get('onjob', 'N/A')}")
                    print(f"Ubuntu Version: {ubuntu_version}")
                    print(f"CPU Architecture: {cpu_arch}")
                    print(f"Current Rentals Stored: {current_rentals_resident}")
                    print(f"Current Rentals Running: {current_rentals_on_demand}")
        except Exception as e: # If it fails:
            print(f"Error parsing JSON response: {e}") # Prints the error.
    elif response.status_code == 401:
            auto_login()
    else:
        print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error status code.
def search_all_cpu():
    search_cpu() # runs the search_cpu function.
    search_notrentable_cpu() # runs the search_notrentable_cpu function
def json_parser(json_data): # JSON Parser
    print(json.dumps(json_data, indent=4)) # prints the response in JSON format after parsing.
    exit()
def list_ssh(): # A function for listing SSH logins of all pods.
    if authToken:
        pods_url = 'https://api.quickpod.org/mypods' 
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   # send a GET response to mypods.
        if response.status_code == 200: # If success:
            data_gpu = response.json()
            print("  ID                            SSH Command                                              Status") # Sketchy way to print a header row :)
            for pod in data_gpu: # For every pod run:
                podid = pod.get('id', 0)
                ip = pod.get('public_ipaddr', 0)
                sshport = pod.get('open_port_start', 0)
                usrname = pod.get('Names', 'N/A')
                status = pod.get('Status', 0)
                print(f'{podid}     ssh -p {sshport} {usrname}@{ip}     {status}') #Assemble the SSH command and print it.
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"failed{response.status_code}") # Print the response failure code.
            exit()
        pods_url = 'https://api.quickpod.org/mypods_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)    # Send GET response to mypods_cpu
        if response.status_code == 200: # If success:
            data_cpu = response.json()
            for pod in data_cpu: # For every pod run:
                podid = pod.get('id', 0)
                ip = pod.get('public_ipaddr', 0)
                sshport = pod.get('open_port_start', 0)
                usrname = pod.get('Names', 'N/A')
                status = pod.get('Status', 0)
                print(f'{podid}     ssh -p {sshport} {usrname}@{ip}     {status}') # Assemble the CPU pods ssh and print it
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"failed{response.status_code}") # Print failure code 
            exit()
def list_pods(): # A function for listing all pods a client is currently running.
    if authToken:
        pods_url = 'https://api.quickpod.org/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   # Send GET request to mypods.
        if response.status_code == 200: # If success:
            if silent:
                pass
            else:
                print("GPU Pod List:")
            try:
                mypods = response.json() # parse response
                if isinstance(mypods, list):
                    if args.json:
                        json_parser(mypods) # Send to json_parser
                    elif args.raw:
                        print(mypods) # Print out raw API response
                    elif args.list:
                        for pod in mypods: # For every pod run:
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
                            #print(f"SSH Private Key: {pod['ssh_private_key']}")
                            print("-" * 40)  # Separator for readability
                    else:
                        if not mypods:
                            print("No GPU Pods!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mypods_list = pd.DataFrame(mypods) # Create list
                            print(mypods_list[['id', 'Names', 'CreatedAt', 'pod_type', 'Status', 'Image', 'RunningFor', 'last_billed', 'last_billed_state']].to_string(index=False)) # Print List

                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}") # Prints the error
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}") # prints the error code
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_pods_cpu():
    if authToken:
        pods_url = 'https://api.quickpod.org/mypods_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)    # Send GET request to mypods_cpu
        if response.status_code == 200:  # If success:
            if silent:
                pass
            else:
                print("CPU Pod List:")
            try:
                mypods = response.json() # Parse response
                if isinstance(mypods, list):
                    if args.raw:
                        print(mypods) # Prints raw API output
                    elif args.json:
                        json_parser(mypods) # Sends data to json_parser
                    elif args.list:
                        for pod in mypods: # For every pod:
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
                            #print(f"SSH Private Key: {pod['ssh_private_key']}")
                            print("-" * 40)
                    else:
                        if not mypods:
                            print("No CPU Pods!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mypods_list = pd.DataFrame(mypods) # Creates the row.
                            print(mypods_list[['id', 'Names', 'CreatedAt', 'pod_type', 'Status', 'Image', 'RunningFor', 'last_billed', 'last_billed_state']].to_string(index=False)) # Prints row with only specific columns

                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e: # If error:
                print(f"Error parsing JSON response: {e}") # Print the error response.
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}") # Print the error status code.
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_all_pods(): # Lists all Pods
    list_pods() #runs list_pods
    list_pods_cpu() # rins list_pods_cpu
def public_templates(): # Searches all public templates and gives details for each.2
    pods_url = 'https://api.quickpod.org/public_templates'
    response = requests.get(pods_url)     # Sends GET request to public_templates
    message = response.json() # Parses the response
    if response.status_code == 200: # If Success:
        if args.json:
            json_parser(message) # Sends the data to the json_parser.
        elif args.raw:
            print(message) # Prints raw API response.
        elif args.list:
            list = pd.DataFrame(message) # Creates the list.
            print(list.to_string(index=False)) # prints the list.
        else:
            pd.set_option('display.width', 1000)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            list = pd.DataFrame(message) # Create the list.
            print(list[['id', 'created_at', 'user_id', 'image_path', 'template_uuid', 'launch_mode', 'disk_space', 'is_public', 'template_type',]].to_string(index=False)) # Prints with specific columns only.

    else:
        print(f"Failed to get templates. Status code: {response.status_code}") # Prints the error code
        print(message)
def my_templates():
    if authToken:
        pods_url = 'https://api.quickpod.org/templates'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }
        response = requests.get(pods_url, headers = headers) # Sends a GET request to /templates   
        message = response.json() # parses the response
        if response.status_code == 200: # If success:
            if args.json:
                json_parser(message) # Sends data to json_parser
            elif args.raw:
                print(message) # Prints raw API response.
            elif args.list:
                list = pd.DataFrame(message) # Makes list
                print(list.to_string(index=False)) # Prints list
            else:
                pd.set_option('display.width', 1000)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_rows', None)
                list = pd.DataFrame(message) # Makes List
                print(list[['id', 'created_at', 'user_id', 'image_path', 'template_uuid', 'launch_mode', 'disk_space', 'is_public', 'template_type',]].to_string(index=False)) # Prints list with specific columns only.
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to get templates. Status code: {response.status_code}") # Prints failure code.
            print(message)
    else:
        print("not logged in.")
def create_job():
    if authToken:
        pods_url = 'https://api.quickpod.org/update/createjob'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        if args.name: # If a pod name is specified:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'altname': f'{args.name}',
                'template_uuid': f'{args.template}',
            }
        else: # If a pod name is NOT specified.
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'template_uuid': f'{args.template}',

            }
        response = requests.post(pods_url, headers=headers, json=params)    # Send POST request to createjob
        message = response.json()  # parse the response.
        if response.status_code == 200: # If success.
            print(message)
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to create pod. Status code: {response.status_code}") # Prints failure status code.
            print(message)
def create_pod():
    if authToken:
        pods_url = 'https://api.quickpod.org/update/createpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        if args.name: # If a pod name is specified:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'altname': f'{args.name}',
                'template_uuid': f'{args.template}',
            }
        else: # If a pod name is NOT specified.
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'template_uuid': f'{args.template}',

            }
        response = requests.post(pods_url, headers=headers, json=params)    # Send POST request to createjob
        message = response.json()  # parse the response.
        if response.status_code == 200: # If success.
            print(message)
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to create pod. Status code: {response.status_code}") # Prints failure status code.
            print(message)
def start_pod():
    if authToken:
        pods_url = 'https://api.quickpod.org/update/startpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)   # Sends GET request to startpod 
        message = response.json() # Parses Response
        if response.status_code == 200: # If Success:
            if args.raw:
                print(response.status_code) # Prints raw API response.
            if args.json:
                json_parser(message) # Sends response to json_parser.
            else:
                print("success!")
                print(message)
        elif response.status_code == 401:
            auto_login()
        else: # If it fails:
            if args.raw:
                print(response.status_code) # Print raw API response.
            if args.json:
                json_parser(message) # Send response to json_parsrr.
            else:
                print(f"Failed to start pod. Status code: {response.status_code}")
                print(message)
def stop_pod():
    if authToken:
        pods_url = 'https://api.quickpod.org/update/stoppod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    # Sends GET request to stoppod
        message = response.json() # Parses response.
        if response.status_code == 200: # If Success
            print("success!")
            print(message)
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to stop pod. Status code: {response.status_code}") # Print error code.
            print(message)
def restart_pod():
    if authToken:
        pods_url = 'https://api.quickpod.org/update/restartpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params) # Send GET request to restartpod    
        message = response.json() # Parse response
        if response.status_code == 200: # If Sucess:
            if args.raw:
                print(response.status_code) # Prints raw API output
            if args.json:
                json_parser(message) # Sends response to json_parser
            else:
                print("success!")
                print(message)
        elif response.status_code == 401:
            auto_login()
        else: # If it fails:
            if args.raw:
                print(response.status_code) # Prints raw API output
            if args.json:
                json_parser(message) # Sends response to json_parser
            else:
                print(f"Failed to restart pod. Status code: {response.status_code}")
                print(message)
def restart_all_pods():
    if authToken:
        pods_url = 'https://api.quickpod.org/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)  # Sends GET request to mypods. Finds all current pods.
        mypods = response.json() # parses response
        if response.status_code == 200: # If Success:
            for pod in mypods: # For every pod run:
                uuid = pod.get('Names', 'N/A')
                ID = pod.get('id', 'N/A')
                pods_url = 'https://api.quickpod.org/update/restartpod'
                headers = {
                    'Authorization': f'Bearer {authToken}',
                    'Content-Type': 'application/json'
                }   
                params = {
                    'pod_uuid': f'{uuid}'
                }
                response = requests.get(pods_url, headers=headers, params=params)    # Sends a GET request to restart the pod.
                message = response.json() # Parses response. 
                if response.status_code == 200: # If Success run:
                    if args.raw:
                        print(response.status_code) # Print raw API output.
                    if args.json:
                        json_parser(message) # Send response to json_parser.
                    else:
                        print(f"restarting pod {ID}") # Human Response.
                else: # If failure:
                    if args.raw:
                        print(response.status_code) # Print status code.
                    if args.json:
                        json_parser(message) # Send response to json_parser
                    else:
                        print(f"Failed to restart pod. Status code: {response.status_code}") # Print failure status code.
                        print(message)
        elif response.status_code == 401:
            auto_login()
def destroy_pod(): # Destroys a Pod
    if authToken:
        pods_url = 'https://api.quickpod.org/update/destroypod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    # Send GET request to destorypod
        message = response.json()
        if response.status_code == 200: # If success:
            if args.raw:
                print(response.status_code) # Prints status code.
            if args.json:
                json_parser(message) # Sends response to json_parser
            else:
                print("success!")
                print(message)
        elif response.status_code == 401:
            auto_login()
        else:
            if args.raw:
                print(response.status_code) # Prints status code
            if args.json:
                json_parser(message) # Sends response to json_parser
            else:
                print(f"Failed to destroy pod. Status code: {response.status_code}")
                print(message)
def list_host_machine():
    if unlist == True:
        listvsunlist = False
    else:
        listvsunlist = True
    confirmed_machine_id = 0
    gpu_list = []
    gpu_count = 0
    find_id = int(args.ID)
    machine_found = False
    if authToken:
        pods_url = 'https://api.quickpod.org/mymachines'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(pods_url, headers=headers) # Sends GET request to mymachines_cpu
        if response.status_code == 200: # If success:
            try:
                mymachines_gpu = response.json() # Parses machine response
                for machine in mymachines_gpu:
                    machine_id = machine["id"]
                    if machine_id == find_id:
                        machine_found = True
                        confirmed_machine_id = machine_id
                        if args.manual:
                            current_storage_price = machine["listed_storage_cost"]
                            current_max_duration = machine["max_duration"]
                            current_min_gpus = machine["min_gpu"]
                            current_listed = machine["listed"]
                            print("Welcome to the QuickPod CLI Machine Lister!")
                            print(f"You are editing machine # {machine_id}")
                            print("Here's some info about it:")
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            machineslist = pd.DataFrame(mymachines_gpu) # Creates List
                            filtered_machineslist = machineslist[machineslist['id'] == machine_id]
                            print(filtered_machineslist[['id', 'hostname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False)) # Prints list with only certain columns
                            while True:
                                list_storage_price = input(f"We'll start with the storage cost. Currently it's at ${current_storage_price}/hr. (Press enter to keep it at that.)")
                                if not list_storage_price:
                                    list_storage_price = current_storage_price
                                    break
                                try:
                                    list_storage_price = float(list_storage_price)
                                    break 
                                except ValueError:
                                    print("Invalid input! Please enter a valid float.")
                            while True:
                                list_max_duration = input(f"Next up is Max Duration. Currently it's at {current_max_duration} Days. (Press enter to keep it at that.)")
                                if not list_max_duration:
                                    list_max_duration = current_max_duration
                                    break
                                try:
                                    list_max_duration = int(list_max_duration)
                                    break 
                                except ValueError:
                                    print("Invalid input! Please enter a valid int.")
                            while True:
                                list_min_gpus = input(f"Finally we have min GPUs. Currently it's at {current_min_gpus}. (Press enter to keep it at that.)")
                                if not list_min_gpus:
                                    list_min_gpus = current_min_gpus
                                    break
                                try:
                                    list_min_gpus = int(list_min_gpus)
                                    break 
                                except ValueError:
                                    print("Invalid input! Please enter a valid int.")
                            listorno = input(f"Would you like to list your machine? Currently Listed = {current_listed} [Y/N]")
                            if listorno == "n":
                                listvsunlist = False
                            else:
                                listvsunlist = True
                        elif silent:
                            if args.storage_cost == 0:
                                list_storage_price = machine["listed_storage_cost"]
                            else:
                                list_storage_price = args.storage_cost
                            if args.max_duration == 0:
                                list_max_duration = machine["max_duration"]
                            else:
                                list_max_duration = args.max_duration
                            if args.min_gpus == 0:
                                list_min_gpus = machine["min_gpu"]
                            else:
                                list_min_gpus = args.min_gpus
                        else:
                            print(f"Machine ID: {machine_id}")
                            if args.storage_cost == 0:
                                list_storage_price = machine["listed_storage_cost"]
                                print(f"Keeping Storage price at ${list_storage_price}/hr.")
                            else:
                                list_storage_price = args.storage_cost
                                print(f"Setting Storage price to ${list_storage_price}/hr.")
                            if args.max_duration == 0:
                                list_max_duration = machine["max_duration"]
                                print(f"Keeping Max Duration at {list_max_duration} Days.")
                            else:
                                list_max_duration = args.max_duration
                                print(f"Setting Max Duration to {list_max_duration} Days.")
                            if args.min_gpus == 0:
                                list_min_gpus = machine["min_gpu"]
                                print(f"Keeping Min GPUs at {list_min_gpus}.")
                            else:
                                list_min_gpus = args.min_gpus
                                print(f"Setting Min GPUs to {list_min_gpus}.")
                        if '_machines' in machine and isinstance(machine['_machines'], list): # If a section called _machines exists run:
                            for gpu in machine['_machines']: # For every entry in _machines
                                gpu_id = gpu["id"]
                                gpu_cost = gpu["listed_gpu_cost"]
                                gpu_index = gpu["gpu_machine_index"]
                                gpu_name = gpu["gpu_name"]
                                gpu_vram = gpu["gpu_vram"]
                                gpu_pcie = gpu["gpu_pcie"]
                                gpu_lanes = gpu["gpu_lanes"]
                                gpu_tflops = gpu["tflops"]
                                if args.manual:
                                    print("=-"*50)
                                    print(f"Found GPU {gpu_index}. Here's some info:")
                                    print(f"GPU Name: {gpu_name}")
                                    print(f"GPU VRAM: {gpu_vram}")
                                    print(f"GPU PCIE {gpu_pcie}x{gpu_lanes}")
                                    print(f"GPU TeraFlops: {gpu_tflops}")
                                    while True:
                                        new_gpu_cost = input(f"GPU {gpu_index} is currently at ${gpu_cost}/hr (Press enter to keep it at that or enter a new price.)")
                                        if not new_gpu_cost:
                                            list_gpu_cost = gpu_cost
                                            break
                                        try:
                                            list_gpu_cost = float(new_gpu_cost)
                                            break 
                                        except ValueError:
                                            print("Invalid input! Please enter a valid float.")
                                elif args.cost == 0:
                                    list_gpu_cost = gpu_cost
                                    if silent:
                                        pass
                                    else:
                                        print(f"Keeping GPU {gpu_index} at ${list_gpu_cost}/hr")
                                else:
                                    list_gpu_cost = args.cost
                                    if silent:
                                        pass
                                    else:
                                        print(f"Setting GPU {gpu_index} to ${list_gpu_cost}/hr")
                                gpu_list.append({
                                    "id": gpu_id,
                                    "listed_gpu_cost": str(list_gpu_cost)
                                })
                            json_stage = {
                                "listed_storage_cost": str(list_storage_price),
                                "listed": listvsunlist,
                                "max_duration": str(list_max_duration),
                                "gpus_listing": gpu_list,
                                "listed_inet_down_cost": "0.25",
                                "min_gpu": str(list_min_gpus)
                            }
                            if silent:
                                pass
                            else:
                                print("Sending Request...")
                            response = requests.put(
                            url=f"https://api.quickpod.org/update/listmachines/{confirmed_machine_id}",
                            json=json_stage,
                            headers = {
                                'Authorization': f'Bearer {authToken}',
                            }
                            )
                            if response.status_code == 200:
                                pass
                            else:
                                print(f"failed{response.status_code}")
                        else:
                            print("API Error getting machine info")
                    else:
                        continue
            except Exception as e:
                print(f"Error parsing JSON response: {e}") # Prints the error
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error code
    else:
        print("Error: AuthToken not found. Please log in first.")
    if machine_found == False:
        confirmed_machine_id = 0
        gpu_list = []
        gpu_count = 0
        find_id = int(args.ID)
        machine_found = False
        if authToken:
            pods_url = 'https://api.quickpod.org/mymachines_cpu'
            headers = {
                'Authorization': f'Bearer {authToken}',
                'Content-Type': 'application/json'
            }  
            response = requests.get(pods_url, headers=headers) # Sends GET request to mymachines_cpu
            if response.status_code == 200: # If success:
                try:
                    mymachines_gpu = response.json() # Parses machine response
                    for machine in mymachines_gpu:
                        machine_id = machine["id"]
                        if machine_id == find_id:
                            machine_found = True
                            confirmed_machine_id = machine_id
                            if args.manual:
                                current_storage_price = machine["listed_storage_cost"]
                                current_max_duration = machine["max_duration"]
                                current_listed = machine["listed"]
                                print("Welcome to the QuickPod CLI Machine Lister!")
                                print(f"You are editing machine # {machine_id}")
                                print("Here's some info about it:")
                                pd.set_option('display.width', 1000)
                                pd.set_option('display.max_columns', None)
                                pd.set_option('display.max_rows', None)
                                machineslist = pd.DataFrame(mymachines_gpu) # Creates List
                                filtered_machineslist = machineslist[machineslist['id'] == machine_id]
                                print(filtered_machineslist[['id', 'hostname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False)) # Prints list with only certain columns
                                while True:
                                    list_storage_price = input(f"We'll start with the storage cost. Currently it's at ${current_storage_price}/hr. (Press enter to keep it at that.)")
                                    if not list_storage_price:
                                        list_storage_price = current_storage_price
                                        break
                                    try:
                                        list_storage_price = float(list_storage_price)
                                        break 
                                    except ValueError:
                                        print("Invalid input! Please enter a valid float.")
                                while True:
                                    list_max_duration = input(f"Next up is Max Duration. Currently it's at {current_max_duration} Days. (Press enter to keep it at that.)")
                                    if not list_max_duration:
                                        list_max_duration = current_max_duration
                                        break
                                    try:
                                        list_max_duration = int(list_max_duration)
                                        break 
                                    except ValueError:
                                        print("Invalid input! Please enter a valid int.")
                                listorno = input(f"Would you like to list your machine? Currently Listed = {current_listed} [Y/N]")
                                if listorno == "n":
                                    listvsunlist = False
                                else:
                                    listvsunlist = True
                            if silent:
                                if args.storage_cost == 0:
                                    list_storage_price = machine["listed_storage_cost"]
                                else:
                                    list_storage_price = args.storage_cost
                                if args.max_duration == 0:
                                    list_max_duration = machine["max_duration"]
                                else:
                                    list_max_duration = args.max_duration
                            else:
                                print(f"Machine ID: {machine_id}")
                                if args.storage_cost == 0:
                                    list_storage_price = machine["listed_storage_cost"]
                                    print(f"Keeping Storage price at ${list_storage_price}/hr.")
                                else:
                                    list_storage_price = args.storage_cost
                                    print(f"Setting Storage price to ${list_storage_price}/hr.")
                                if args.max_duration == 0:
                                    list_max_duration = machine["max_duration"]
                                    print(f"Keeping Max Duration at {list_max_duration} Days.")
                                else:
                                    list_max_duration = args.max_duration
                                    print(f"Setting Max Duration to {list_max_duration} Days.")
                            if '_machines' in machine and isinstance(machine['_machines'], list): # If a section called _machines exists run:
                                for gpu in machine['_machines']: # For every entry in _machines
                                    gpu_id = gpu["id"]
                                    cpu_cost = gpu["listed_gpu_cost"]
                                if args.manual:
                                    while True:
                                        new_cpu_cost = input(f"Machine {machine_id} is currently at ${cpu_cost}/core/hr (Press enter to keep it at that or enter a new price.)")
                                        if not new_cpu_cost:
                                            list_cpu_cost = cpu_cost
                                            break
                                        try:
                                            list_gpu_cost = float(new_cpu_cost)
                                            break 
                                        except ValueError:
                                            print("Invalid input! Please enter a valid float.")
                                if args.cost == 0:
                                    list_cpu_cost = cpu_cost
                                    if silent:
                                        pass
                                    else:
                                        print(f"Keeping Machine {machine_id} at ${list_cpu_cost}/hr")
                                else:
                                    list_gpu_cost = args.cost
                                    if silent:
                                        pass
                                    else:
                                        print(f"Setting Machine {machine_id} to ${list_cpu_cost}/hr")
                                json_stage = {
                                    "listed_storage_cost": str(list_storage_price),
                                    "listed": listvsunlist,
                                    "max_duration": str(list_max_duration),
                                    "listed_cpu_cost": str(list_cpu_cost)
                                }
                                if silent:
                                    pass
                                else:
                                    print("Sending Request...")
                                response = requests.put(
                                url=f"https://api.quickpod.org/update/listmachines_cpu/{confirmed_machine_id}",
                                json=json_stage,
                                headers = {
                                    'Authorization': f'Bearer {authToken}',
                                }
                                )
                                if response.status_code == 200:
                                    pass
                                else:
                                    print(f"failed{response.status_code}")
                            else:
                                print("API Error getting machine info")
                        else:
                            continue
                except Exception as e:
                    print(f"Error parsing JSON response: {e}") # Prints the error
            elif response.status_code == 401:
                auto_login()
            else:
                print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error code
        else:
            print("Error: AuthToken not found. Please log in first.")
    else:
        pass
    if machine_found == True:
        pass
    else:
        print("No machine by the specified ID found.")



def unlist_host_machine():
    global unlist
    unlist = True
    list_host_machine()

def change_privileged_mode():
    machines_url = 'https://api.quickpod.org/update/machine_allow_privileged_access'
    headers = {
        'Authorization': f'Bearer {authToken}',
        'Content-Type': 'application/json'
    }  
    request = {
    "allow_priveleged": args.truefalse,
    "machine_id": args.ID
    }
    response = requests.post(machines_url, headers=headers, json=request) # sends GET request to mymachines
    if response.status_code == 200: # If success
        print("Success!")
    elif response.status_code == 401:
        auto_login()
    else:
        print(f"Failed to change privileged mode. Status code: {response.status_code}")


def get_machines(): # lists all machines HOSTS ONLY
    if authToken:
        machines_url = 'https://api.quickpod.org/mymachines'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(machines_url, headers=headers) # sends GET request to mymachines
        if response.status_code == 200: # If success
            try:
                mymachines = response.json() # Parses response
                if isinstance(mymachines, list):
                    if args.raw:
                        print(mymachines) # Prints raw API output.
                    elif args.json:
                        json_parser(mymachines) # Sends response to json_parser
                    elif args.list:
                        for machine in mymachines: # For every machine run:
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
                            if '_machines' in machine and isinstance(machine['_machines'], list): # If a section called _machines exists run:
                                print("GPU Details:")
                                for gpu in machine['_machines']: # For every entry in _machines
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
                        if not mymachines: # If mymachines does not exist
                            print("No GPU Machines to List!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            machineslist = pd.DataFrame(mymachines) # Creates List
                            print(machineslist[['id', 'hostname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False)) # Prints list with only certain columns
            except Exception as e:
                print(f"Error parsing JSON response: {e}") # Displays error
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch machines. Status code: {response.status_code}") # Prints error status code.
    else:
        print("Error: AuthToken not found. Please log in first.")
def get_cpu_machines():# List CPU machines HOSTS ONLY
    if authToken:
        pods_url =  'https://api.quickpod.org/mymachines_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(pods_url, headers=headers) # Sends GET request to mymachines_cpu
        if response.status_code == 200: # If success:
            try:
                mymachines = response.json() # Parses machine response
                if isinstance(mymachines, list):
                    if args.raw:
                        print(mymachines) # Prints raw API output
                    elif args.json:
                        json_parser(mymachines) # Sends response to json_parser
                    elif args.list:
                        for machine in mymachines: # For every machine run:
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
                    else:
                        if not mymachines:
                            print("No CPU Machines to List!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mymachineslist = pd.DataFrame(mymachines) # Creates list
                            print(mymachineslist[['id', 'hostname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False)) # Prints list with only certain columns
                else:
                    print("Error: Expected a list of machines, but received a different structure.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}") # Prints the error
        elif response.status_code == 401:
            auto_login()
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}") # Prints the error code
    else:
        print("Error: AuthToken not found. Please log in first.")
def get_all_machines(): # Runs both functions.
    get_machines()
    get_cpu_machines()
def get_machine_contracts():
    pods_url = 'https://api.quickpod.org/mymachine_contracts'
    headers = {
        'Authorization': f'Bearer {authToken}',
        'Content-Type': 'application/json'
    } 
    try:
        response = requests.get(pods_url, headers=headers)
        message = response.json()
    except Exception as e:
        print(f"Error from the API {e}") # Prints the error
    
    if response.status_code == 200:
        print     
        contracts_sorted = sorted(message, key=lambda machine: machine['id'])
        if args.raw:
            print(contracts_sorted)
        elif args.json:
            for contracts in contracts_sorted:
                print(json.dumps(contracts, indent=4)) # prints the response in JSON format after parsing.
        else:
            hourly_cost = 0
            all_total_cost = 0
            num_pods = 0
            print("="*50)
            print("CPU Machines:")
            for contracts in contracts_sorted: 
                if contracts['machine_type'] == "GPU":
                    continue  
                print("-"*50)
                print(f"Machine ID: {contracts['id']} | Hostname: {contracts['hostname']}")
                if '_pods_of_machines' in contracts and isinstance(contracts['_pods_of_machines'], list): # If a section called _pods_of_machines exists run:
                    for pod in contracts['_pods_of_machines']: # For every entry in _machines
                        if pod['hourly_cost'] == 0:
                            continue
                        id_pod = pod['offers_id']
                        total_cost = pod['pod_cost']
                        gpu_cost = pod['hourly_cost']
                        storage_cost = pod['storage_cost']
                        if pod['State'] == "running":
                            hourly_cost = hourly_cost + gpu_cost
                            total_costph = gpu_cost + storage_cost
                        else:
                            total_costph = storage_cost
                        hourly_cost = hourly_cost + storage_cost
                        all_total_cost = all_total_cost + total_cost
                        num_pods = num_pods + 1
                        print(f"{id_pod} | ${(round(total_cost, 2))} | ${(round(total_costph, 4))}/hr")
            print("="*50)
            print("GPU Machines:")
            for contracts in contracts_sorted: 
                if contracts['machine_type'] == "CPU":
                    continue  
                print("-"*50)
                print(f"Machine ID: {contracts['id']} | Hostname: {contracts['hostname']}")
                if '_pods_of_machines' in contracts and isinstance(contracts['_pods_of_machines'], list): # If a section called _pods_of_machines exists run:
                    for pod in contracts['_pods_of_machines']: # For every entry in _machines
                        if pod['hourly_cost'] == 0:
                            continue
                        id_pod = pod['offers_id']
                        total_cost = pod['pod_cost']
                        gpu_cost = pod['hourly_cost']
                        storage_cost = pod['storage_cost']
                        if pod['State'] == "running":
                            hourly_cost = hourly_cost + gpu_cost
                            total_costph = gpu_cost + storage_cost
                        else:
                            total_costph = storage_cost                        
                        hourly_cost = hourly_cost + storage_cost
                        all_total_cost = all_total_cost + total_cost
                        num_pods = num_pods + 1
                        print(f"{id_pod} | ${(round(total_cost, 2))} | ${(round(total_costph, 4))}/hr")
            print("="*50)
            lines = [
                "                Total Numbers:",
                "----------------------------------------------",
                f"${hourly_cost}/hr Total",
                f"Your Contracts are worth a total of ${(round(all_total_cost, 2))} ",
                f"You have {num_pods} Contracts Running or Stored.",
                "For more data please run with --json or --raw."
            ]
            max_width = max(len(line) for line in lines)
            print("+" + "-" * (max_width + 2) + "+")
            for line in lines:
                print(f"| {line.ljust(max_width)} |")
            print("+" + "-" * (max_width + 2) + "+")
    elif response.status_code == 401:
        auto_login()
    else:
        print(f"\u26A0error{response.status_code}")    


def list_balance():
    url = "api.quickpod.org/update/auth/me"
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        print(tabulate([
            [data.get("balance", "N/A"), data.get("currency", "USD"), data.get("lastTransaction", "N/A")]
        ], headers=["Balance", "Currency", "Last Transaction"]))
    except Exception as e:
        print("Error fetching balance:", e)

def list_earnings():
    url = "api.quickpod.org/update/auth/me"
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        print(tabulate([
            [data.get("totalEarned", "N/A"), data.get("pendingPayout", "N/A"), data.get("lastPayoutDate", "N/A")]
        ], headers=["Total Earned", "Pending Payout", "Last Payout Date"]))
    except Exception as e:
        print("Error fetching earnings:", e)

def auto_create():
    pods_url = 'https://api.quickpod.org/rentable'
    
    # Initialize parameters dictionary with default values if not provided
    params = {
    'num_gpus': 0,
    'max_hourly_cost': 20,
    'disk_space': 0,
    'reliability': 0,
    'duration': 0,
    'gpu_type': "All GPUs",
    'location': args.location,
    'sort_by' : "",
}
    
    # Add filters to the parameters only if they are specified by the user
    
    # Send GET request with filters
    response = requests.get(pods_url, params=params)
    if response.status_code != 200:
        print(f"Error in searching pods {response.status_code}")
        return []
    #Parse the JSON response and filter based on additional arguments
    offers = response.json()
    # Filter offers
#Parse offers if it's a JSON string
    if isinstance(offers, str):
        try:
            offers = json.loads(offers)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse offers as JSON: {e}")
    if not isinstance(offers, list):
        raise ValueError("Offers must be a list of dictionaries")

    # Filter offers
    filtered_offers = []
    offer_count = 0
    for offer in offers:
        if args.verified and not offer.get('_machines', {}).get('verification', False):
            continue
        if args.privileged and not offer.get('_machines', {}).get('allow_privileged_access', False):
            continue
        if args.rel is not None and args.rel > 0 and offer.get('_machines', {}).get('reliability', 0) < args.rel:
            continue
        #if args.cuda is not None and args.cuda > 0 and offer.get('_machines', {}).get('reliability', 0) < args.cuda:
            #continue
        if args.min_days is not None and args.min_days > 0 and offer.get('_machines', {}).get('max_duration', 0) < args.min_days:
            continue
        if args.inet is not None and args.inet > 0 and offer.get('_machines', {}).get('inet_up', 0) < args.inet:
            continue
        if args.cost is not None and args.cost > 0 and (not offer.get('hourly_cost', float('inf')) or offer['hourly_cost'] > args.cost):
            continue
        if args.storage_cost is not None and args.storage_cost > 0 and (not offer.get('listed_storage_cost', float('inf')) or offer['hourly_cost'] > args.storage_cost):
            continue
        if args.gpus is not None and args.gpus > 0 and (not offer.get('num_gpus', 0) or offer['num_gpus'] < args.gpus):
            continue
        if args.cpus is not None and args.cpus > 0 and (not offer.get('cpus', 0) or offer['cpus'] < args.cpus):
            continue
        if args.mem is not None and args.mem > 0 and (not offer.get('memory', 0) or offer['memory'] < args.mem):
            continue
        filtered_offers.append(offer)
        offer_count = offer_count + 1
    offers = filtered_offers
    # Sort offers
    sort_key = args.sortby
    if sort_key == 'reliability':
        offers.sort(key=lambda x: x.get('reliability', 0), reverse=args.reverse)
    elif sort_key == 'price':
        offers.sort(key=lambda x: x.get('max_hourly_cost', float('inf')), reverse=args.reverse)
    elif sort_key == 'tflops-per-dollar':
        offers.sort(key=lambda x: x.get('tflops_per_dollar', 0), reverse=args.reverse)
    elif sort_key == 'vram-per-dollar':
        offers.sort(key=lambda x: x['gpu_vram'] / x['max_hourly_cost'] if x.get('max_hourly_cost', 0) > 0 else 0, reverse=args.reverse)
    elif sort_key == 'cpus':
        offers.sort(key=lambda x: x.get('cpus', 0), reverse=args.reverse)
    elif sort_key == 'memory':
        offers.sort(key=lambda x: x.get('memory', 0), reverse=args.reverse)
    else:
        raise ValueError(f"Invalid sortby value: {sort_key}")
    pods_failed = 0
    pods_created = 0
    pods_url = 'https://api.quickpod.org/update/createpod'
    headers = {
        'Authorization': f'Bearer {authToken}',
        'Content-Type': 'application/json'
    } 
    for offer in offers:  
        if pods_created == args.n:
            break
        params = {
            #"coupon_code": "",
            #"docker_options": "",
            #"pod_uuid": "",
            "offers_id": offer['id'],
            "disk_size": f"{args.disk}",
            "template_uuid": f"{args.template}",
            "altname": f'{str(args.name) + "-" + str(pods_created)}',
        }
        print(params)
        response = requests.post(pods_url, headers=headers, json=params)    # Send POST request to createjob
        if response.status_code == 200: # If success.
            pods_created = pods_created + 1
            print("Success!")
        elif response.status_code == 401:
            auto_login()
        elif response.status_code == 406:
            pods_failed = pods_failed + 1
            print(f"Duplicate or Invalid ID... Trying the next on the list.")
        else:
            print(f"Failed to create pod. Status code: {response.status_code}") # Prints failure status code.
            print(message)
    print(f"{pods_created} pods created out of {offer_count} offers meeting criteria. {pods_failed} were overlapping or invalid ID's.")

def bulk_create_pods(offers):
    print("proceeding..")
    pod_ids = []
    for offer in offers:
        response = requests.post('https://api.quickpod.org/createpod', json={
            'offer': offer,
            'template_id': args.template,
            'image_id': args.name,
            'disk_size': args.disk
        })
        if response.status_code == 200:
            print("Pod created successfully with ID:", response.json().get('pod_id'))
            pod_ids.append(response.json().get('pod_id'))
        else:
            print("Failed to create pod:", response.json().get('message', 'Unknown error'))

def get_host_available_jobs():
    exit()
def print_auth_token(): # Prints the currently stored authtoken
    if args.raw or args.json or args.silent: # if any of the silencing variables are existant run:
        print(authToken)
    else: # Otherwise run:
        print(f"AuthToken: {authToken}")
def delete_auth_token(): # Delete the currently stored authtoken
    dotenv_file = '.env' # Defining dotenv file
    if os.path.exists(dotenv_file):
        try:
            os.remove(dotenv_file)  # Removes the dotenv file
            if silent:
                exit()
            else:
                print("the Auth Token and any other login methods have been deleted.")
                exit()
        except Exception as e: # If there is an error print it.
            print(f"An error occurred while deleting {dotenv_file}: {e}")
            exit()
    else:
        print(f"{dotenv_file} does not exist.") # If the file doesn't exist.
        exit()

parser = argparse.ArgumentParser(description="Command-line utility for managing machines and jobs") # Basic help script.


parser.add_argument(
    '--silent', "-s",
    action="store_true",
    help="Output no text other than the requested response and errors."
)
parser.add_argument(
    '--authtoken',
    type=str,
    help="Set a temporary auth token. This will not be stored and the existing stored authtoken will not be affected."
)
parser.add_argument(
    '--bypass-login',
    action="store_true",
    help="Mostly used as a debug feature. Send API calls without asking for authentication. This is simply a bypass, the API calls WILL NOT go through. "
)
parser.add_argument(
    '--csv',
    type=str,
    help="Outputs the data to a CSV File. Only compatible with Search currently. You must specify a csv file to save it to without .csv. Ex. --csv my_csv_file"
)
parser.add_argument(
    '--json',
    action="store_true",
    help="Output in JSON Format. Unless there is an error, the response to the command will automatically be silenced so the command can be directly be piped into a json parser."
)
parser.add_argument(
    '--raw',
    action="store_true",
    help="Outputs in raw unfiltered API format. Harder to parse than --json, but still a good tool to act as a method of calling the API or for debug."
)
parser.add_argument(
    '--list',
    action="store_true",
    help="Outputs in a semi-readable long list format. Better for filters. Does not have all the data."
)
subparsers = parser.add_subparsers(help="Available categories of commands")

auth_parser = subparsers.add_parser('auth', help="Authentication commands")
auth_subparsers = auth_parser.add_subparsers(help="Authentication subcommands")

auth_subparsers.add_parser('login', help="Log in and store the Auth Token").set_defaults(func=login)
auth_subparsers.add_parser('delete', help="Remove the Auth Token. You will need to authenticate again to access anything. If it asks for login, then the file does not exist.").set_defaults(func=delete_auth_token)
auth_subparsers.add_parser('print', help="Display the currently stored 403-character auth token and exit.").set_defaults(func=print_auth_token)

client_parser = subparsers.add_parser('client', help="Client Commands")
client_subparsers = client_parser.add_subparsers(help="Client subcommands")

client_subparsers.add_parser('list-balance', help="Check client account balance").set_defaults(func=list_balance)
client_subparsers.add_parser('list-ssh-logins', help="Show all current SSH logins available.").set_defaults(func=list_ssh)
client_subparsers.add_parser('list-pods', help="List all GPU pods with details.").set_defaults(func=list_pods)
client_subparsers.add_parser('list-cpu-pods', help="List all CPU pods with details.").set_defaults(func=list_pods_cpu)
client_subparsers.add_parser('list-all-pods', help="List all pods with details.").set_defaults(func=list_all_pods)

search_parser = client_subparsers.add_parser('search', help="List available GPU offers")
search_parser.set_defaults(func=search)
search_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_parser.set_defaults(func=search)

search_occupied_parser = client_subparsers.add_parser('search-occupied', help="List NOT Available GPU offers")
search_occupied_parser.set_defaults(func=search_notrentable)
search_occupied_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_occupied_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_occupied_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_occupied_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_occupied_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_occupied_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_occupied_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_occupied_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_occupied_parser.set_defaults(func=search_notrentable)

search_all_parser = client_subparsers.add_parser('search-all-gpu', help="List all GPU offers, Available or Not.")
search_all_parser.set_defaults(func=search_cpu)
search_all_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_all_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_all_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_all_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_all_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_all_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_all_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_all_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_all_parser.set_defaults(func=search_all)

search_cpu_parser = client_subparsers.add_parser('search-cpu', help="List available CPU offers")
search_cpu_parser.set_defaults(func=search_cpu)
search_cpu_parser.add_argument('--num-cpus', type=int, help='Number of CPUs to filter the pods', default=0) 
search_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_cpu_parser.add_argument('--cpu-type', type=str, help='Type of CPU to filter the pods', default='All CPUs')  
search_cpu_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_cpu_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_cpu_parser.set_defaults(func=search_cpu)

search_occupied_cpu_parser = client_subparsers.add_parser('search-occupied-cpu', help="List NOT Available CPU offers")
search_occupied_cpu_parser.set_defaults(func=search_notrentable_cpu)
search_occupied_cpu_parser.add_argument('--num-cpus', type=int, help='Number of CPUs to filter the pods', default=0) 
search_occupied_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_occupied_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_occupied_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_occupied_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_occupied_cpu_parser.add_argument('--cpu-type', type=str, help='Type of CPU to filter the pods', default='All CPUs')  
search_occupied_cpu_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_occupied_cpu_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_occupied_cpu_parser.set_defaults(func=search_notrentable_cpu)

search_all_cpu_parser = client_subparsers.add_parser('search-all-cpu', help="List All CPU offers")
search_all_cpu_parser.set_defaults(func=search_all_cpu)
search_all_cpu_parser.add_argument('--num-cpus', type=int, help='Number of CPUs to filter the pods', default=0) 
search_all_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_all_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_all_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_all_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_all_cpu_parser.add_argument('--cpu-type', type=str, help='Type of CPU to filter the pods', default='All CPUs')  
search_all_cpu_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_all_cpu_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_all_cpu_parser.set_defaults(func=search_all_cpu)

client_subparsers.add_parser('public-templates', help="Show all Public Templates").set_defaults(func=public_templates)
client_subparsers.add_parser('my-templates', help="Show My Templates").set_defaults(func=my_templates)

create_subparser = client_subparsers.add_parser('create', help="Create a pod with a Template")
create_subparser.set_defaults(func=create_pod)
create_subparser.add_argument('--offer', help="Offer ID of the Pod", type=str)
create_subparser.add_argument('--template', help="UUID of the Template to use.", type=str)
create_subparser.add_argument('--disk', help="Disk Space in GB to allocate.", type=int)
create_subparser.add_argument('--name', help="Name of the Pod", type=str)

start_subparser = client_subparsers.add_parser('start', help="Start an existing Stopped Pod.")
start_subparser.set_defaults(func=start_pod)
start_subparser.add_argument('uuid', help="UUID for the pod", type=str)

stop_subparser = client_subparsers.add_parser('stop', help="Stop a Running Pod.")
stop_subparser.set_defaults(func=stop_pod)
stop_subparser.add_argument('uuid', help="UUID for the pod", type=str)

restart_subparser = client_subparsers.add_parser('restart', help="Restart a Pod")
restart_subparser.set_defaults(func=restart_pod)
restart_subparser.add_argument('uuid', help="UUID for the pod", type=str)

restart_all_subparser = client_subparsers.add_parser('restart-all', help="Restart all Pods")
restart_all_subparser.set_defaults(func=restart_all_pods)

destroy_subparser = client_subparsers.add_parser('destroy', help="Destroy a Pod. ALL DATA WILL BE LOST THIS ACTION IS IRREVERSABLE")
destroy_subparser.set_defaults(func=destroy_pod)
destroy_subparser.add_argument('uuid', help="UUID for the pod", type=str)


auto_create_parser = client_subparsers.add_parser("auto-create", help="Automatically create N pods using current filters and sorts")
auto_create_parser.set_defaults(func=auto_create)
#essentials
auto_create_parser.add_argument("n", type=int, help="Number of pods to create")
auto_create_parser.add_argument('--privileged', '-p', action="store_true", help='Only use privileged offers') 
auto_create_parser.add_argument('--verified', '-v', action="store_true", help='Only show use offers that have been verified to work by QuickPod') 
auto_create_parser.add_argument("-r", '--reverse', action="store_true", help="reverse list")
auto_create_parser.add_argument("-y", '--yes', action="store_true", help="Don't display the first offers for verification.")

#API Filters
auto_create_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
auto_create_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
#Manual filters (>)
auto_create_parser.add_argument('--gpus', '--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
auto_create_parser.add_argument('--rel', '--minimum-reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
auto_create_parser.add_argument('--min-days', '--duration', type=int, help='Minimum duration to filter the pods (in days)', default=0)  
auto_create_parser.add_argument('--cpus', '--min-cpus', type=int, help='Number of GPUs to filter the pods', default=0) 
auto_create_parser.add_argument('--mem', '--min-memory', type=int, help='Maximum hourly cost to filter the pods', default=0)   
auto_create_parser.add_argument('--cuda','--min-cuda', type=float, help='Minimum reliability level to filter the pods', default=0)
auto_create_parser.add_argument('--inet', '--min-inet-up-speed', type=int, help='Minimum duration to filter the pods (in hours)', default=0)  
#Manual filters (<)
auto_create_parser.add_argument('--cost', '--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)   
auto_create_parser.add_argument('--storage-cost', '--max-disk-cost', type=float, help='Maximum hourly disk cost to filter the pods', default=20) 
#sort (Price least to greatest, reliability, tflops, cpus, and memory greatest to least)
auto_create_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'tflops-per-dollar', 'vram-per-dollar' 'cpus', 'memory'], help='Sort by field', default='price') 
#creation
auto_create_parser.add_argument("--template", required=True, help="Template ID to use for pod creation")
auto_create_parser.add_argument("--name", required=True, help="Optional image ID")
auto_create_parser.add_argument("--disk", required=True, type=str, help="Disk size in GB")


host_parser = subparsers.add_parser('host', help="Host Commands")
host_subparsers = host_parser.add_subparsers(help="Host subcommands")
host_subparsers.add_parser('list-earnings', help="Check host earnings balance").set_defaults(func=list_earnings)
host_subparsers.add_parser('print-machines', help="Show a list of all active GPU machines under this host account.").set_defaults(func=get_machines)
host_subparsers.add_parser('print-cpu-machines', help="Show a list of all active CPU machines under this host account.").set_defaults(func=get_cpu_machines)
host_subparsers.add_parser('print-all-machines', help="Show a list of all active machines under this host account.").set_defaults(func=get_all_machines)
create_subparser = host_subparsers.add_parser('create-job', help="[HOSTS] Create a Job with a Template")
create_subparser.set_defaults(func=create_job)
create_subparser.add_argument('--offer', help="Offer ID of the Pod", type=str)
create_subparser.add_argument('--template', help="UUID of the Template to use.", type=str)
create_subparser.add_argument('--disk', help="Disk Space in GB to allocate.", type=int)
create_subparser.add_argument('--name', help="Name of the Pod", type=str)
list_subparser = host_subparsers.add_parser('list-machine', help="Lists a machine for rental. Any fields left blank will be kept as what they already are.")
list_subparser.set_defaults(func=list_host_machine)
list_subparser.add_argument('ID', help="Required Argument. Machine Number goes Here. If you don't know it or want to set pricing for ALL of your machines, input ALL.", type=str)
list_subparser.add_argument('--manual', help="Manually go through each GPU on specified Machine. Can edit GPU pricing individually Will ignore all arguments except for ID.", action="store_true")
list_subparser.add_argument('--storage-cost', help="Cost of storage per Terabyte per Hour.", type=float, default=0)
list_subparser.add_argument('--max-duration', help="Maximum number of days the renter can run for.", type=int, default=0)
list_subparser.add_argument('--cost', help="Cost to set ALL GPUs to. To set a manual price for each GPU, use --manual", type=float, default=0)
list_subparser.add_argument('--min-gpus', help="Minimum number of GPUs that can be rented in a pod. Ignored if updating a CPU machine.", type=int, default=0)
unlist_subparser = host_subparsers.add_parser('unlist-machine', help="Unlsts a machine. Can still update pricing. Any fields left blank will be kept as what they already are.")
unlist_subparser.set_defaults(func=unlist_host_machine)
unlist_subparser.add_argument('ID', help="Required Argument. Machine Number goes Here. If you don't know it or want to set pricing for ALL of your machines, input ALL.", type=str)
unlist_subparser.add_argument('--manual', help="Manually go through each GPU on specified Machine. Can edit GPU pricing individually Will ignore all arguments except for ID.", action="store_true")
unlist_subparser.add_argument('--storage-cost', help="Cost of storage per Terabyte per Hour.", type=float, default=0)
unlist_subparser.add_argument('--max-duration', help="Maximum number of days the renter can run for.", type=int, default=0)
unlist_subparser.add_argument('--cost', help="Cost to set ALL GPUs to. To set a manual price for each GPU, use --manual", type=float, default=0)
unlist_subparser.add_argument('--min-gpus', help="Minimum number of GPUs that can be rented in a pod. Ignored if updating a CPU machine.", type=int, default=0)
host_subparsers.add_parser('print-contracts', help="Show a list of all active GPU machines under this host account.").set_defaults(func=get_machine_contracts)
privileged_subparser = host_subparsers.add_parser('set-privileged', help="Sets the Privileged Mode of a Machine.")
privileged_subparser.set_defaults(func=change_privileged_mode)
privileged_subparser.add_argument('ID', help="Required Argument. Machine Number goes Here.", type=int)
privileged_subparser.add_argument('truefalse', help="Required Argument. Choose whether or not to make a machine privileged", type=bool, choices=[True, False])
args = parser.parse_args() 
unlist = False
if args.json or args.silent or args.raw: # If any silencing argument:
    silent = 1
else:
    silent = 0
if silent:
    pass
else:
    print("QuickPod CLI Beta 1.3.1.") # version
    print("Copyright (C) 2025 QuickPod. All Rights Reserved") # Copyright
load_dotenv() # Load in the variables stored in the dotenv
authToken = os.getenv("authToken") # Gets the authtoken from dotenv

if args.authtoken: # If using a custom authtoken:
    authToken = args.authtoken
    if silent:
        pass
    else:
        print(f"Using Custom Auth Token: {authToken[:4]}")
elif authToken:
    pass
elif args.bypass_login: # If bypass login is selected
    pass
else:
    print("You are not logged in!") #This should not be silenced because login is required
    login() # Runs the login function
    load_dotenv() # Loads the dotenv in case it's changed.
    authToken = os.getenv("authToken") # sets authToken
if args.csv: # Not useful right now. Protects against empty filenames for CSV's.
    csv_name = args.csv 
    if csv_name == "": #Failsafe against empty filename
        csv_name = latest
    else:
        pass


if hasattr(args, 'func'): # If a function is specified:
    args.func() # Run that function
else:
    parser.print_help() # Otherwise print the help.