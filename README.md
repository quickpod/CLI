This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

# CLI
A Command line python tool that interfaces with the QuickPod API to manage machines and pods.

# !!!IMPORTANT!!!
Dependencies for Dotenv and Pandas are required to run this script!
```pip install python-dotenv; pip install pandas```

# New Features:

- Search Function!
- Direct API Sort and filter optiopns for the Search Function.
- Create, Start, Stop, Restart, and Destroy Pods; and Create Host Jobs.
- Upgraded Login System!
- Template Finder!

# New Global Arguments:

- Raw API Output.
- Json Output.
- CSV File Export.
- Machine-by-machine List.
- Row-and-Column List (Default)
- Silent Mode.

# Usage:

```QPCLI.py -h```

# Command Breakdowns:

### Auth

### Client
###### list-pods
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### list-cpu-pods
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### list-all-pods
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### search
```
Global Arguments:
--raw
--json
--list
--csv CSV_NAME
or without arguments

Filters:
--num-gpus NUM_GPUS   Number of GPUs to filter the pods # EX. --num-gpus 4
--max-hourly-cost MAX_HOURLY_COST   Maximum hourly cost to filter the pods  # EX. --max-hourly-cost 0.2
--disk-space DISK_SPACE   Amount of disk space to filter the pods # EX. --disk-space 100
--reliability RELIABILITY   Minimum reliability level to filter the pods # EX. --reliability 90
--duration DURATION   Minimum duration to filter the pods (in Days) # EX. --duration 60
--gpu-type GPU_TYPE   Type of GPU to filter the pods  # EX. --gpu-type 'NVIDIA GeForce RTX 3060'
--location LOCATION   Location to filter the pods  #Nonfunctional currently

Sort:
--sortby SORTBY
  - price
  - reliability
  - performance
Ex. --sortby price

Examples:
python3 QPCLI.py --json client search --num-gpus 1 --gpu-type 'NVIDIA GeForce RTX 3060'
python3 QPCLI.py --csv mycsv1 client search
```
###### search-occupied
###### search-all-gpu
###### public-templates
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### my-templates
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### create
###### start
```
Global Arguments:
--raw
--json
or without arguments
```
###### stop
```
Global Arguments:
--raw
--json
or without arguments
```
###### restart
```
Global Arguments:
--raw
--json
or without arguments
```
###### destroy
```
Global Arguments:
--raw
--json
or without arguments
```

### Host


# COMING SOON:

- Host Earning Stats
- Client Billing Stats
- CPU Search!