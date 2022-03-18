# docker_pull_python

This python script accepts 2 required arguments and others are optional. 
Required Arguments : s3 bucketname and the filepath
Optional Arguments : Registry name, username , password and awsprofile name

The script will run only if the required arguments are provided. 
Use Optional arguments in the below scenarios 
a) Use awsprofile , When you want to use a particular AWS profile. Example : Dev , Production etc. Please check the .aws/credentials file for more info.
b) Use the rest of optional arguments , When you want to use a registry other than hub.docker.io. 


How to use with examples : 

There is a help section to the script. Use the **-h** argument. 

**/usr/local/opt/python/bin/python3.7 /Users/sasikantpamuru/Desktop/python/aws1.py **-h****
usage: aws1.py [-h] [-u USERNAME] [-p PASSWORD] [-r REGISTRYNAME]
               [-P AWSPROFILE] -B AWSBUCKET -F AWSFILEPATH

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -B AWSBUCKET, --awsbucket AWSBUCKET
                        Provide the aws bucket name
  -F AWSFILEPATH, --awsfilepath AWSFILEPATH
                        Provide the exact path to the file location

optional arguments:
  -u USERNAME, --username USERNAME
                        Provide the registry username
  -p PASSWORD, --password PASSWORD
                        Provide the registry password
  -r REGISTRYNAME, --registryname REGISTRYNAME
                        Provide the name of the docker registry
  -P AWSPROFILE, --awsprofile AWSPROFILE
                        Provide the profile to use from aws credentials file


Example : 
A user has the file in a s3 bucket named testcis1. Inside the bucket there is a folder called docker and inside which is he saved to file tenantA.json. The user can will use

**python3.7 aws1.py -B "testcis1" -F "docker/tenantA.json"**


