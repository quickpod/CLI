This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

# CLI
A Command line python tool that interfaces with the QuickPod API to manage machines and pods.

# !!!IMPORTANT!!!
Dependencies for Dotenv and Pandas are required to run this script!
```pip install python-dotenv; pip install pandas```

# New Features:

- Commented ALL Code!
- Added `list-ssh-logins` command
- Added `restart-all` command

# Usage:
```
QPCLI.py <GLOBAL ARGUMENTS> [SUB-POSITIONAL ARGUMENTS] [COMMAND] [FILTERS]
```

- *The above explaination may be very confusing, so I have broken it down further.*
# Command Breakdowns:

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

### Pod Controls
```
Ex. python3 QPCLI.py client stop UUID
 - Replace UUID with the Pod UUID, which can be found in the list-pods function.
 - It is a required argument.
```

### Pod Creation
```
Ex. python3 QPCLI.py client create --offer-id OFFER_ID --disk DISK --template TEMPLATE_UUID --name NAME
 - Replace the placeholders after the arguments with the required information.
 - Same rules apply for Host Job Creation
```


## Auth

###### login
```
There are no available output arguments because input is required for this command. This will be improved later.

python3 QPCLI.py auth login
```

###### delete
```
Global Argument:
--silent, -s
or without arguments

python3 QPCLI.py [-s] auth delete
```

###### print
```
Global Argument:
--silent, -s
or without arguments

python3 QPCLI.py [-s] auth print
```

## client

###### list-ssh-logins
```
There are no arguments available currently.

python3 QPCLI.py client list-ssh-logins
```
###### list-pods
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] client list-pods
```
###### list-cpu-pods
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] client list-cpu-pods
```
###### list-all-pods
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] client list-all-pods
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

python3 QPCLI.py [--raw, --json, --list, --csv CSV_NAME] client search [--num-gpus NUM_GPUS --max-hourly-cost MAX_HOURLY_COST --disk-space DISK_SPACE --reliability RELIABILITY --duration DURATION --gpu-type GPU_TYPE --location LOCATION --sortby SORTBY]
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

python3 QPCLI.py [--raw, --json, --list, --csv CSV_NAME] client search [--num-gpus NUM_GPUS --max-hourly-cost MAX_HOURLY_COST --disk-space DISK_SPACE --reliability RELIABILITY --duration DURATION --gpu-type GPU_TYPE --location LOCATION --sortby SORTBY]
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

python3 QPCLI.py [--raw, --json, --list, --csv CSV_NAME] client search [--num-gpus NUM_GPUS --max-hourly-cost MAX_HOURLY_COST --disk-space DISK_SPACE --reliability RELIABILITY --duration DURATION --gpu-type GPU_TYPE --location LOCATION --sortby SORTBY]
```
###### public-templates
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] client public-templates
```
###### my-templates
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] client my-templates
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

python3 QPCLI.py [--json] client create --offer-id OFFER_ID --template TEMPLATE --disk DISK [--name NAME]
```
###### start
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID

python3 QPCLI.py [--raw, --json] client start UUID
```
###### stop
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID

python3 QPCLI.py [--raw, --json] client stop UUID
```
###### restart
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID

python3 QPCLI.py [--raw, --json] client restart UUID
```
###### destroy
```
Global Arguments:
--raw
--json
or without arguments

Required Argument:
UUID

python3 QPCLI.py [--raw, --json] client destroy UUID
```

## Host

###### print-machines
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] host print-machines
```
###### print-cpu-machines
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] host print-cpu-machines
```
###### print-all-machines
```
Global Arguments:
--raw
--json
--list
or without arguments

python3 QPCLI.py [--raw, --json, --list] host print-all-machines
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

python3 QPCLI.py [--json] client create --offer-id OFFER_ID --template TEMPLATE --disk DISK [--name NAME]
```
# COMING SOON:

- Account Settings, creation, deletion, etc.
- Host List machines for rental
- Fix Sort Function
- Host Earning Stats
- Client Billing Stats
- CPU Search!
