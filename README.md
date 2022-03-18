# docker_pull_python

This python script accepts 2 required arguments and others are optional. The script will run only if the required arguments are provided. 

Required Arguments : s3 bucketname and the filepath. </br>
Optional Arguments : Registry name, username , password and awsprofile name.

**Use Optional arguments in the below scenarios**  </br>
a) Use awsprofile , When you want to use a particular AWS profile. Example : Dev , Production etc. Please check the .aws/credentials file for more info. </br>
b) Use the rest of optional arguments , When you want to use a registry other than hub.docker.io. </br>


**How to use with examples** : </br>
Use **-h** argument for help. 

**/usr/local/opt/python/bin/python3.7 /Users/sasikantpamuru/Desktop/python/aws_docker.py **-h****. </br> </br>
usage: aws1.py [-h] [-u USERNAME] [-p PASSWORD] [-r REGISTRYNAME] </br>
               [-P AWSPROFILE] -B AWSBUCKET -F AWSFILEPATH
</br>
**optional arguments**: </br>
  -h, --help            show this help message and exit </br>
</br>
**required arguments**: </br>
  -B AWSBUCKET, --awsbucket AWSBUCKET, Provide the aws bucket name. </br>
  -F AWSFILEPATH, --awsfilepath AWSFILEPATH, Provide the exact path to the file location </br>
</br>
**optional arguments**: </br>
  -u USERNAME, --username USERNAME Provide the registry username. </br>
  -p PASSWORD, --password PASSWORD Provide the registry password. </br>
  -r REGISTRYNAME, --registryname REGISTRYNAME Provide the name of the docker registry. </br>
  -P AWSPROFILE, --awsprofile AWSPROFILE Provide the profile to use from aws credentials file. </br>


**Example** : 
A user has the file in a s3 bucket named testcis1. Inside the bucket there is a folder called docker and inside which is he saved to file tenantA.json. The user will use </br>
</br>
**python3.7 aws_docker.py -B "testcis1" -F "docker/tenantA.json"**


