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

## Explaination of the Search Filter and Sort functions:
### Filter
```
 - --num-gpus NUM_GPUS   Number of GPUs to filter the pods # EX. --num-gpus 4
 - --max-hourly-cost MAX_HOURLY_COST   Maximum hourly cost to filter the pods  # EX. --max-hourly-cost 0.2
 - --disk-space DISK_SPACE   Amount of disk space to filter the pods # EX. --disk-space 100
 - --reliability RELIABILITY   Minimum reliability level to filter the pods # EX. --reliability 90
 - --duration DURATION   Minimum duration to filter the pods (in Days) # EX. --duration 60
- --gpu-type GPU_TYPE   Type of GPU to filter the pods  # EX. --gpu-type 'NVIDIA GeForce RTX 3060'
- --location LOCATION   Location to filter the pods  #Nonfunctional currently please leave blank.
```
### Sort
#### Sortby currently does NOT WORK on the API Side. We are working on a fix for this.
```
--sortby SORTBY
  - price
  - reliability
  - performance
Ex. --sortby price
```

# Usage:
```
QPCLI.py <GLOBAL ARGUMENTS> [SUB-POSITIONAL ARGUMENTS] [COMMAND] [FILTERS]
```

- *The above explaination may be very confusing, so I have broken it down further.*
# Command Breakdowns:

### Auth

###### login
```
There are no available output arguments because input is required for this command. This will be improved later.
```

###### delete
```
Global Argument:
--silent, -s
or without arguments
```

###### print
```
Global Argument:
--silent, -s
or without arguments
```

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
--num-gpus NUM_GPUS
--max-hourly-cost MAX_HOURLY_COST
--disk-space DISK_SPACE
--reliability RELIABILITY
--duration DURATION
--gpu-type GPU_TYPE
--location LOCATION

Sort:
--sortby SORTBY # Currently not working.
```
###### search-occupied
```
Global Arguments:
--raw
--json
--list
--csv CSV_NAME
or without arguments

Filters:
--num-gpus NUM_GPUS
--max-hourly-cost MAX_HOURLY_COST
--disk-space DISK_SPACE
--reliability RELIABILITY
--duration DURATION
--gpu-type GPU_TYPE
--location LOCATION

Sort:
--sortby SORTBY # Currently not working.
```
###### search-all-gpu
```
Global Arguments:
--raw
--json
--list
--csv CSV_NAME
or without arguments

Filters:
--num-gpus NUM_GPUS
--max-hourly-cost MAX_HOURLY_COST
--disk-space DISK_SPACE
--reliability RELIABILITY
--duration DURATION
--gpu-type GPU_TYPE
--location LOCATION

Sort:
--sortby SORTBY # Currently not working.
```
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
```
Global Arguments:
--json
or without arguments (Raw is Default)

Required Arguments:
--offer-id OFFER-ID
--template TEMPLATE
--disk DISK

Optional Argument:
--name NAME

```
###### start
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID
```
###### stop
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID
```
###### restart
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID
```
###### destroy
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID
```

### Host

###### print-machines
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### print-cpu-machines
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### print-all-machines
```
Global Arguments:
--raw
--json
--list
or without arguments
```
###### create-job
```
Global Arguments:
--json
or without arguments (Raw is Default)

Required Arguments:
--offer-id OFFER-ID
--template TEMPLATE
--disk DISK

Optional Argument:
--name NAME
```

# COMING SOON:

- Host Earning Stats
- Client Billing Stats
- CPU Search!