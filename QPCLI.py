import argparse
import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime 
import csv
import pandas as pd

#print("QuickPod CLI Version 1.1.0.")
#print("Copyright (C) 2025 QuickPod. All Rights Reserved")
#Thank you for choosing QuickPod!
def unix_to_human_time(unix_time):
    if unix_time > 0:
        return datetime.utcfromtimestamp(unix_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return 'N/A' 
def login():
    login_method = input("Enter your QuickPod Email Or API Key Or Auth Token:")
    if len(login_method) == 36:
        api_key = login_method
        print("Logging in with API Key.")
        login_url = 'https://api.quickpod.io/api:2USncWkT/auth/apikeylogin'
        credentials = {
            'api_key': api_key, 
        }
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            authToken = response.json().get('authToken')
            if authToken:
                print(f"Successfully logged in. AuthToken (First 4 digits): {authToken[:4]}")
            with open('.env', 'w') as f:
                f.write(f"authToken={authToken}")
            load_dotenv()
            print("Auth Token Stored successfully!")
            exit()
    elif len(login_method) > 300:
        newauthtoken = login_method
        print("Setting Auth Token...")
        with open('.env', 'w') as f:
            f.write(f"authToken={newauthtoken}")
        load_dotenv()
        exit()
    else:
        print("Using Email / Password Authentication")
        email = login_method
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
                print("Auth Token Stored successfully!")
            else:
                print("Error: AuthToken not found in the response.")
        else:
            print(f"Login failed. Status code: {response.status_code}")
            print(response.text)
            exit()
def search_all():
    if silent:
        pass
    else:
        print("Available Machines:")
    search()
    if silent:
        pass
    else:
        print("NOT Available Machines:")
    if args.csv:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/notrentable'
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

        response = requests.get(pods_url, params=params)
        if response.status_code == 200:
            try:
                offers = response.json()
                with open(f'{csv_name}.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    header = ([
                        'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                        'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                        'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                        'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                        'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                    ])
                    for offer in offers:
                        machines = offer.get('_machines', [])
                        for key, value in machines.items():
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
                        writer.writerow(row)
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
        if silent:
            pass
        else:
            print(f"Appended to {csv_name}.csv!")
    else:
        search_notrentable()
def search():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/rentable'
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

        response = requests.get(pods_url, params=params)
        if response.status_code == 200:
            try:
                offers = response.json()
                #print(offers)
                if args.csv:
                    with open(f'{csv_name}.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        header = ([
                            'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                            'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                            'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                            'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                            'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                        ])
                        writer.writerow(header)
                        for offer in offers:
                            machines = offer.get('_machines', [])
                            for key, value in machines.items():
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
                            writer.writerow(row)
                    if silent:
                        pass
                    else:
                        print(f"Saved to {csv_name}.csv!")
                elif args.json:
                    json_parser(offers)
                elif args.raw:
                    print(offers)
                elif args.list:
                    for offer in offers:
                        machines = offer.get('_machines', [])
                        for key, value in machines.items():
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
                else:
                    if not offers:
                        print("No Available Machines!")
                    else:
                        pd.set_option('display.width', 1000)
                        pd.set_option('display.max_columns', None)
                        pd.set_option('display.max_rows', None)
                        list = pd.DataFrame(offers)
                        print(list[['id', 'offer_name', 'machines_id', 'hourly_cost', 'cpus', 'memory', 'max_disk_size', 'num_gpus', 'gpu_vram', 'gpu_pcie', 'gpu_lanes', 'tflops', 'onjob', 'occupied']].to_string(index=False))

            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def search_cpu():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/rentable_cpu'
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

        response = requests.get(pods_url, params=params)
        print(response.status_code)
        if response.status_code == 200:
            try:
                offers = response.json()
                print(response)
                print(offers)
                for offer in offers:
                    machines = offer.get('_machines', [])
                    for key, value in machines.items():
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
                    
                if isinstance(offers, list):
                    print("ok")
                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def search_notrentable():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/notrentable'
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

        response = requests.get(pods_url, params=params)
        if response.status_code == 200:
            try:
                offers = response.json()
                if args.csv:
                    with open(f'{csv_name}.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        header = ([
                            'Offer Name', 'Offer ID', 'Machine ID', 'Host', 'Verified', 'Location', 'Location Details', 'Internet Download Speed',
                            'Internet Upload Speed', 'Reliability', 'Max Duration', 'Offer Type', 'CPU Name', 'Memory', 'CPUs', 'CPU Frequency', 
                            'Hourly Cost', 'TFLops per Dollar', 'Perf per Dollar', 'GPU Type', 'Num GPUs', 'TFLops', 'Max CUDA Version', 'GPU VRAM',
                            'GPU PCIe Version', 'PCIE Speed', 'GPU PCIe Lanes', 'Max Disk Size', 'Ports Count', 'Perf Score', 'Created At', 
                            'Occupied', 'Last Updated', 'On Job', 'Ubuntu Version', 'CPU Architecture', 'Current Rentals Stored', 'Current Rentals Running'
                        ])
                        writer.writerow(header)
                        for offer in offers:
                            machines = offer.get('_machines', [])
                            for key, value in machines.items():
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
                            writer.writerow(row)
                        if silent:
                            pass
                        else:
                            print(f"Saved to {csv_name}.csv!")
                elif args.json:
                    json_parser(offers)
                elif args.raw:
                    print(offers)
                elif args.list:
                    if silent:
                        pass
                    else:
                        print("Defaulting to Old Method")
                    for offer in offers:
                        machines = offer.get('_machines', [])
                        for key, value in machines.items():
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

                else:
                    if not offers:
                        print("No machines to list")
                    else:
                        pd.set_option('display.width', 1000)
                        pd.set_option('display.max_columns', None)
                        pd.set_option('display.max_rows', None)
                        list = pd.DataFrame(offers)
                        print(list[['id', 'offer_name', 'machines_id', 'hourly_cost', 'cpus', 'memory', 'max_disk_size', 'num_gpus', 'gpu_vram', 'gpu_pcie', 'gpu_lanes', 'tflops', 'onjob', 'occupied']].to_string(index=False))

            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def search_notrentable_cpu():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/rentable'
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

        response = requests.get(pods_url, params=params)
        if response.status_code == 200:
            try:
                offers = response.json()
                for offer in offers:
                    machines = offer.get('_machines', [])
                    for key, value in machines.items():
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
                    
                if isinstance(offers, list):
                    print("ok")
                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def search_all_cpu():
    search_cpu()
    search_notrentable_cpu
def json_parser(json_data):
    print(json.dumps(json_data, indent=4))
def list_ssh():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   
        if response.status_code == 200:
            data_gpu = response.json()
            print("ID                            SSH Command                                              Status")
            for pod in data_gpu:
                podid = pod.get('id', 0)
                ip = pod.get('public_ipaddr', 0)
                sshport = pod.get('open_port_start', 0)
                usrname = pod.get('Names', 'N/A')
                status = pod.get('Status', 0)
                print(f'{podid}     ssh -p {sshport} {usrname}@{ip}     {status}')
        else:
            print(f"failed{response.status_code}")
            exit()
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   
        if response.status_code == 200:
            data_cpu = response.json()
            for pod in data_cpu:
                podid = pod.get('id', 0)
                ip = pod.get('public_ipaddr', 0)
                sshport = pod.get('open_port_start', 0)
                usrname = pod.get('Names', 'N/A')
                status = pod.get('Status', 0)
                print(f'{podid}     ssh -p {sshport} {usrname}@{ip}     {status}')

        else:
            print(f"failed{response.status_code}")
            exit()


def list_pods():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   
        if response.status_code == 200:
            if silent:
                pass
            else:
                print("GPU Pod List:")
            try:
                mypods = response.json()
                if isinstance(mypods, list):
                    if args.json:
                        json_parser(mypods)
                    elif args.raw:
                        print(mypods)
                    elif args.list:
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
                            #print(f"SSH Private Key: {pod['ssh_private_key']}")
                            print("-" * 40)  # Separator for readability
                    else:
                        if not mypods:
                            print("No GPU Pods!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mypods_list = pd.DataFrame(mypods)
                            print(mypods_list[['id', 'Names', 'CreatedAt', 'pod_type', 'Status', 'Image', 'RunningFor', 'last_billed', 'last_billed_state']].to_string(index=False))

                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_pods_cpu():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)    
        if response.status_code == 200:
            if silent:
                pass
            else:
                print("CPU Pod List:")
            try:
                mypods = response.json()
                if isinstance(mypods, list):
                    if args.raw:
                        print(mypods)
                    elif args.json:
                        json_parser(mypods)
                    elif args.list:
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
                            #print(f"SSH Private Key: {pod['ssh_private_key']}")
                            print("-" * 40)  # Separator for readability`
                    else:
                        if not mypods:
                            print("No CPU Pods!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mypods_list = pd.DataFrame(mypods)
                            print(mypods_list[['id', 'Names', 'CreatedAt', 'pod_type', 'Status', 'Image', 'RunningFor', 'last_billed', 'last_billed_state']].to_string(index=False))

                else:
                    print("The response is not a list of pods. Please check the API response.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_all_pods():
    list_pods()
    list_pods_cpu()

def public_templates():
    pods_url = 'https://api.quickpod.io/api:2USncWkT/public_templates'
    response = requests.get(pods_url)    
    message = response.json()
    if response.status_code == 200:
        if args.json:
            json_parser(message)
        elif args.raw:
            print(message)
        elif args.list:
            list = pd.DataFrame(message)
            print(list.to_string(index=False))
        else:
            pd.set_option('display.width', 1000)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            list = pd.DataFrame(message)
            print(list[['id', 'created_at', 'user_id', 'image_path', 'template_uuid', 'launch_mode', 'disk_space', 'is_public', 'template_type',]].to_string(index=False))

    else:
        print(f"Failed to get templatesStatus code: {response.status_code}")
        print(message)
def my_templates():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:2USncWkT/templates'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }
        response = requests.get(pods_url, headers = headers)    
        message = response.json()
        if response.status_code == 200:
            if args.json:
                json_parser(message)
            elif args.raw:
                print(message)
            elif args.list:
                list = pd.DataFrame(message)
                print(list.to_string(index=False))
            else:
                pd.set_option('display.width', 1000)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_rows', None)
                list = pd.DataFrame(message)
                print(list[['id', 'created_at', 'user_id', 'image_path', 'template_uuid', 'launch_mode', 'disk_space', 'is_public', 'template_type',]].to_string(index=False))

        else:
            print(f"Failed to get templates. Status code: {response.status_code}")
            print(message)
    else:
        print("not logged in.")
def create_job():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/createjob'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        if args.name:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'altname': f'{args.name}',
                'template_uuid': f'{args.template}',
            }
        else:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'template_uuid': f'{args.template}',

            }
        response = requests.post(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            print(message)
        else:
            print(f"Failed to create pod. Status code: {response.status_code}")
            print(message)
def create_pod():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/createpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        if args.name:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'altname': f'{args.name}',
                'template_uuid': f'{args.template}',
            }
        else:
            params = {
                'offers_id': f'{args.offer}',
                'disk_size': f'{args.disk}',
                'template_uuid': f'{args.template}',

            }
        response = requests.post(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            if args.json:
                json_parser(message)
            else:
                print(message)

        else:
            print(f"Failed to create pod. Status code: {response.status_code}")
            print(message)
def start_pod():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/startpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print("success!")
                print(message)
        else:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print(f"Failed to start pod. Status code: {response.status_code}")
                print(message)

def stop_pod():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/stoppod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            print("success!")
            print(message)
        else:
            print(f"Failed to stop pod. Status code: {response.status_code}")
            print(message)
def restart_pod():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/restartpod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print("success!")
                print(message)
        else:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print(f"Failed to restart pod. Status code: {response.status_code}")
                print(message)
def restart_all_pods():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mypods'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        response = requests.get(pods_url, headers=headers)   
        mypods = response.json()
        if response.status_code == 200:
            for pod in mypods:
                uuid = pod.get('Names', 'N/A')
                ID = pod.get('id', 'N/A')
                pods_url = 'https://api.quickpod.io/api:KoOk0R5J/restartpod'
                headers = {
                    'Authorization': f'Bearer {authToken}',
                    'Content-Type': 'application/json'
                }   
                params = {
                    'pod_uuid': f'{uuid}'
                }
                response = requests.get(pods_url, headers=headers, params=params)    
                message = response.json()
                if response.status_code == 200:
                    if args.raw:
                        print(response.status_code)
                    if args.json:
                        json_parser(message)
                    else:
                        print(f"restarted pod {ID}")
                        print(message)
                else:
                    if args.raw:
                        print(response.status_code)
                    if args.json:
                        json_parser(message)
                    else:
                        print(f"Failed to restart pod. Status code: {response.status_code}")
                        print(message)

def destroy_pod():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/destroypod'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }   
        params = {
            'pod_uuid': f'{args.uuid}'
        }
        response = requests.get(pods_url, headers=headers, params=params)    
        message = response.json()
        if response.status_code == 200:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print("success!")
                print(message)
        else:
            if args.raw:
                print(response.status_code)
            if args.json:
                json_parser(message)
            else:
                print(f"Failed to destroy pod. Status code: {response.status_code}")
                print(message)

def list_machines():
    if authToken:
        machines_url = 'https://api.quickpod.io/api:KoOk0R5J/mymachines'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(machines_url, headers=headers)
        if response.status_code == 200:
            try:
                mymachines = response.json()
                if isinstance(mymachines, list):
                    if args.raw:
                        print(mymachines)
                    elif args.json:
                        json_parser(mymachines)
                    elif args.list:
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
                        if not mymachines:
                            print("No GPU Machines to List!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            machineslist = pd.DataFrame(mymachines)
                            print(machineslist[['id', 'hostname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False))
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch machines. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_cpu_machines():
    if authToken:
        pods_url = 'https://api.quickpod.io/api:KoOk0R5J/mymachines_cpu'
        headers = {
            'Authorization': f'Bearer {authToken}',
            'Content-Type': 'application/json'
        }  
        response = requests.get(pods_url, headers=headers)
        if response.status_code == 200:
            try:
                mymachines = response.json()
                if isinstance(mymachines, list):
                    if args.raw:
                        print(mymachines)
                    elif args.json:
                        json_parser(mymachines)
                    elif args.list:
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
                    else:
                        if not mymachines:
                            print("No CPU Machines to List!")
                        else:
                            pd.set_option('display.width', 1000)
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            mymachineslist = pd.DataFrame(mymachines)
                            print(mymachineslist[['id', 'hotsname', 'cpu_name', 'cpu_cores', 'cpu_ram', 'geolocation', 'public_ipaddr', 'online', 'perf_score', 'reliability', 'listed', 'max_duration', 'machine_type',]].to_string(index=False))
                else:
                    print("Error: Expected a list of machines, but received a different structure.")
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
        else:
            print(f"Failed to fetch pods. Status code: {response.status_code}")
    else:
        print("Error: AuthToken not found. Please log in first.")
def list_all_machines():
    list_machines()
    list_cpu_machines()
def print_auth_token():
    if args.raw or args.json or args.silent:
        print(authToken)
    else:
        print(f"AuthToken: {authToken}")
def delete_auth_token():
    dotenv_file = '.env'
    if os.path.exists(dotenv_file):
        try:
            os.remove(dotenv_file)  
            if silent:
                exit()
            else:
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

client_subparsers.add_parser('list-ssh-logins', help="Show all current SSH logins available.").set_defaults(func=list_ssh)
client_subparsers.add_parser('list-pods', help="List all GPU pods with details.").set_defaults(func=list_pods)
client_subparsers.add_parser('list-cpu-pods', help="List all CPU pods with details.").set_defaults(func=list_pods_cpu)
client_subparsers.add_parser('list-all-pods', help="List all pods with details.").set_defaults(func=list_all_pods)
client_subparsers.add_parser('search', help="List available GPU offers").set_defaults(func=search)
search_parser = client_subparsers.add_parser('search')
search_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_parser.set_defaults(func=search)
client_subparsers.add_parser('search-occupied', help="List NOT Available GPU offers").set_defaults(func=search_notrentable)
search_occupied_parser = client_subparsers.add_parser('search-occupied')
search_occupied_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_occupied_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_occupied_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_occupied_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_occupied_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_occupied_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_occupied_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_occupied_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_occupied_parser.set_defaults(func=search_notrentable)
client_subparsers.add_parser('search-all-gpu', help="List all GPU offers, Available or Not.").set_defaults(func=search_cpu)
search_all_parser = client_subparsers.add_parser('search-all-gpu')
search_all_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_all_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_all_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_all_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_all_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_all_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_all_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_all_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_all_parser.set_defaults(func=search_all)
#client_subparsers.add_parser('search_cpu', help="List available CPU offers").set_defaults(func=search_cpu)
search_cpu_parser = client_subparsers.add_parser('search-cpu')
search_cpu_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_cpu_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_cpu_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_cpu_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_cpu_parser.set_defaults(func=search_cpu)
#client_subparsers.add_parser('search_occupied_cpu', help="List NOT Available CPU offers").set_defaults(func=search_notrentable_cpu)
search_occupied_cpu_parser = client_subparsers.add_parser('search-occupied-cpu')
search_occupied_cpu_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_occupied_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_occupied_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_occupied_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_occupied_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_occupied_cpu_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
search_occupied_cpu_parser.add_argument('--location', type=str, help='Location to filter the pods', default='All Regions') 
search_occupied_cpu_parser.add_argument('--sortby', type=str, choices=['price', 'reliability', 'performance'], help='Sort by field', default='') 
search_occupied_cpu_parser.set_defaults(func=search_notrentable_cpu)
#client_subparsers.add_parser('search_all_cpu', help="List All CPU offers").set_defaults(func=search_all_cpu)
search_all_cpu_parser = client_subparsers.add_parser('search-all-cpu')
search_all_cpu_parser.add_argument('--num-gpus', type=int, help='Number of GPUs to filter the pods', default=0) 
search_all_cpu_parser.add_argument('--max-hourly-cost', type=float, help='Maximum hourly cost to filter the pods', default=20)  
search_all_cpu_parser.add_argument('--disk-space', type=int, help='Amount of disk space to filter the pods', default=0) 
search_all_cpu_parser.add_argument('--reliability', type=float, help='Minimum reliability level to filter the pods', default=0)
search_all_cpu_parser.add_argument('--duration', type=int, help='Minimum duration to filter the pods (in hours)', default=1)  
search_all_cpu_parser.add_argument('--gpu-type', type=str, help='Type of GPU to filter the pods', default='All GPUs')  
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




host_parser = subparsers.add_parser('host', help="Host Commands")
host_subparsers = host_parser.add_subparsers(help="Host subcommands")
host_subparsers.add_parser('print-machines', help="Show a list of all active GPU machines under this host account.").set_defaults(func=list_machines)
host_subparsers.add_parser('print-cpu-machines', help="Show a list of all active CPU machines under this host account.").set_defaults(func=list_cpu_machines)
host_subparsers.add_parser('print-all-machines', help="Show a list of all active machines under this host account.").set_defaults(func=list_all_machines)
create_subparser = host_subparsers.add_parser('create-job', help="[HOSTS] Create a Job with a Template")
create_subparser.set_defaults(func=create_job)
create_subparser.add_argument('--offer', help="Offer ID of the Pod", type=str)
create_subparser.add_argument('--template', help="UUID of the Template to use.", type=str)
create_subparser.add_argument('--disk', help="Disk Space in GB to allocate.", type=int)
create_subparser.add_argument('--name', help="Name of the Pod", type=str)

args = parser.parse_args()
if args.json or args.silent or args.raw:
    silent = 1
else:
    silent = 0
if silent:
    pass
else:
    print("QuickPod CLI Version 1.1.0.")
    print("Copyright (C) 2025 QuickPod. All Rights Reserved")
load_dotenv()
authToken = os.getenv("authToken")

if args.authtoken:
    authToken = args.authtoken
    if silent:
        pass
    else:
        print(f"Using Custom Auth Token: {authToken[:4]}")
elif authToken:
    if silent:
        pass
    else:
        #print(f"Using Auth Token: {authToken[:4]}")
        pass
elif args.bypass_login:
    pass
else:
    print("You are not logged in!") #This should not be silenced because login is required
    login()
    load_dotenv()
    authToken = os.getenv("authToken")
if args.csv:
    csv_name = args.csv
    if csv_name == "": #Failsafe against empty filename
        csv_name = latest
    else:
        pass


if hasattr(args, 'func'):
    args.func()
else:
    parser.print_help()