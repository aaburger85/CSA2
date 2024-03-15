# Tools for Aurora2 

These are a few python scripts to interact directly with Switches running Aurora2
These tools use netmiko to interact with a catalyst switch, requiring SSH access to the host to be useful.
Please ensure you remove any resrictions on the VTY lines prior to trying

all scripts are run using `python3 {python.py script} {switch ip} {username} {password}`
## CS-A2-CONFIG.py

The configuration python file provides the following tools in a selection format:
- Poke switch config - tells switch to download config from dashboard
- Check Status - Checks connectivity state and if there are errors with configuration deployment, output the error lines
- If you've fixed the config in dashboard, clear the downloaded config, clear the error xml file (then manually re-run a.)
- Capture information into a text file (nested under the subdirectory debug_files/)

The information captured in the Check status are the following outputs:
- Show Meraki Connect
- Show Meraki Config Upater
- if an error: reads the contents of update_err.xml and filters lines for "bad-command"

The delete config and log does the following:
- deletes the dwnld_running.config file
- deletes the update_err.xml file

The Capture information for bug triage:
- version
- update_err.xml file parsed for bad-command
- downloaded config xml
- running-config (CLI)
- running-config (XML)

## CS-A2-TDL.py

The TDL python file provides a filterable parsing of the following data:
- Get TDL Models on box
- Get a specific TDL path's hierarchy
- Get tables from a model
- get records from a table entry
- get N recursive