# Docgen

### Introduction
Docgen CLI tool is built for generating API documentation from code.

List of languages supported:

 * PHP
 
Supported doc generator engines:

 * Swagger

### Pre-Request
Make sure following software's requirement is satisfied in your machine before installing docgen

 * Docker 1.3 or greater (Installer: [Download Docker Engine](https://docs.docker.com/engine/installation/)) 
 * Python 2.7

### Before Installing version 1.0:
If already installed beta release of docgen, please make sure to uninstall it by using the below command.

`sudo docgen remove`


### Install
Download the attachment. Open terminal and cd to the unzipped folder. 

Change "install" script permission to "777"

   `chmod 777 install`

Run following command to install docgen

   `sudo ./install`

### Docgen Commands:
Following are the list of commands supported by docgen

    -h - Display all help commands with supported params
    
    -v - Display current docgen client and server version
    
    start - Start a docgen server 
    
    stop - Stop docgen server
    
    json - Output document generated from code to stdout/file, based on parameter supplied
    
    status - Displays the running status of docgen server
    
    log - To tail documentation logs while server running
    
    update - TBD

### Sample Usage
 * Getting docgen help
 
    `$docgen -h`

 * Start docgen server
 
   `$docgen start -d /path/to/api`
    
 * Create Json formatted docgen using direct command
 
    `$docgen json -d /path/to/api -o /local/path/json`
    
### Trouble Shooting Tips:
 
 * If prompted to check docgen internal logs:
 
     `tail -f /usr/local/bin/docgen_src/docgen.log`

### Release Notes:

#### V1.0
 - Implemented new system design Support smaller docker images
 - "https" support with  swagger 
 - Remove Click pacakge Remove Interface package
 - Added unit test cases
#### V1.1
 - Replaced site-packages with docgen_src.
 - Optimized setup.py for better readability.
 - Improved user experience for mounts failure error.
 - For improved feedback uninstall exception handled if user tries uninstall without sudo.
