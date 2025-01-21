# CLI
A Command line python tool that interfaces with the QuickPod API to manage machines and pods.

```QPCLI.py -h```

```positional arguments:
  {auth,clients,hosts}  Available categories of commands
    auth                Authentication commands
    clients             Client Commands
    hosts               Host Commands

optional arguments:
  -h, --help            show this help message and exit
  --authtoken AUTHTOKEN
                        Set a temporary auth token. This will not be stored and the existing stored authtoken will not be affected.
  --bypass-login        Send API calls without asking for authentication. This is simply a bypass, the API calls WILL NOT go through.
```
ALL CURRENT COMMANDS:

```QPCLI.py auth login
QPCLI.py auth print-auth-token
QPCLI.py --bypass-login auth set-auth-token  #--bypass-login will no longer be needed in a future update.
QPCLI.py --bypass-login auth delete-auth-token   #--bypass-login will no longer be needed in a future update.
QPCLI.py hosts listmachines
QPCLI.py clients listpods
```

Usage:

```
QPCLI.py [OPTIONAL ARGUMENTS] [POSITIONAL ARGUMENTS] [SECONDARY-POSITIONAL ARGUMENTS] [FLAGS] #Flags coming soon in a future update!
```


COMING SOON:

- JSON exporter for all commands (--json, -j)
- CSV exporter for certain commands (--csv, -c)
- Silent Mode for pod controls (--silent, -s)
- Pod Controls(Start, Stop, Destroy, Create)
- Host Earning Stats
- Client Billing Stats
- GPU/CPU Search!