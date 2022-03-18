import profile
import boto3
import json
import docker
import base64
import os
import logging
import botocore
import argparse

AWS_PROFILE = "default"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
REGISTRYURL = "index.docker.io"

def aws_session(profile):
    """ Create an AWS session.
        Argument :  Name of the profile. Example : dev, production etc
        returns : Session handle
    """
    try : 
        logging.info('ESTABLISHING AWS SESSION WITH PROFILE {}'.format(profile))
        #return boto3.session.Session(aws_access_key_id="AKIAQHSSCTRGC4K4N3WJ",
                                #aws_secret_access_key="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",
                               # region_name="us-east-1")
        return boto3.session.Session(profile_name=profile)
    except botocore.exceptions.ClientError as error:
        logging.critical('ESTABLISHING AWS SESSION FAILED')
        raise error
                
def download_file_from_s3(bucket_name, s3_key, destination_path,aws_profile='default'):
    """ Download the file from s3. 
        Arguments : Bucketname , s3 filepath , destination filename, profile name
    """
    try:
        session = aws_session(aws_profile)
        logging.info('Downloading {0} from bucket {1}'.format(s3_key,bucket_name))
        s3_resource = session.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        bucket.download_file(Key=s3_key, Filename=destination_path)
    except botocore.exceptions.ClientError as error:
        logging.critical('Downloading {0} from bucket {1} failed. Check the correct filename and filepath.'.format(s3_key,bucket_name))
        raise error    

def read_file(path_to_file):
    """ This can be extended to read other type of files. Currently we parse only JSON files
        Arguments : downloaded file path
        returns : Name of the image
    """
    with open(path_to_file,"r") as rf:
        data = json.load(rf)
        return data['image_name']

def docker_registry():
    try:
        logging.info("Get docker registry url")
        client = docker.from_env()
        docker_reg = client.info()
        registry = docker_reg['IndexServerAddress']
    except:
        logging.warn("docker registry url not found")
        exit(0)
    return registry 
  
def docker_pull(imagename,username="user",password="password",registry="registryname"):
    """ Pull the docker image from the mentioned repository.
    : we will first get the docker url if available and use it to connect
    : Do a ping check if the server is reacheble
    :returns: 'docker handle'
    """
    try:
        logging.info("Pulling image {}".format(imagename))
        client = check_docker_availability()
        #docker login into private registry
        if "docker.io" not in registry:
            client.login(username, password,registry)
        image = client.images.pull(imagename)
        logging.info("pulled image {}".format(image.id))
    except APIError:
        logging.critical(docker.errors.APIError)
        raise error

def get_docker_host():
    """Get docker url.
    :returns: 'docker url'
    """
    return os.environ.get('DOCKER_HOST', 'unix://var/run/docker.sock')

def check_docker_availability():
    """check of if docker is present in the machine.
    : we will first get the docker url if available and use it to connect
    : Do a ping check if the server is reacheble
    :returns: 'docker handle'
    """
    base_docker_url = get_docker_host()
    docker_client = docker.DockerClient(base_url=base_docker_url)
    assert docker_client.ping()
    docker_version = docker_client.version()
    version  = docker_version['Version']
    logging.info("Docker version found {}".format(version))
    return docker_client

def get_docker_url(docker_image,registry_url="index.docker.io",):
    """Compose the docker url.
    :param registry_uri: The URI of the docker registry
    :param docker_image: The docker image name, with tag if desired
    :returns: '<registry_uri>/<docker_image>'
    """
    if not docker_image:
        raise NoDockerImageError('Docker url not available because there is no docker_image')
    
    docker_url = '%s/%s' % (registry_url, docker_image)
    return docker_url

def main():
    """ Assumptions : File type is JSON with key "image_name"
                      Bucket has a public access.
        STEP 1 : Download the requested file from the given s3 bucket.
        STEP 2 : Read the JSON file downloaded from STEP 1 and construct the full image name
        STPE 3 : docker pull the image from the public respository(default) or private repository
        Log and Raise an error if anything goes wrong.
    """
    download_file_from_s3(aws_profile=AWS_PROFILE, bucket_name=args.awsbucket, s3_key=args.awsfilepath, destination_path='tenant.json')
    docker_url = get_docker_url(read_file("tenantA.json"),REGISTRYURL)
    docker_pull(docker_url,username=USERNAME,password=PASSWORD,registry=REGISTRYURL)

if __name__ == "__main__":
    """ We collect few required and few optional Arguments.
        : Required Arguments -- AWS Bucketname and the FilePath.  
        : Optional Arguments -- Remote RegistryName , Registry Username and Registry Password
                             --  Name of the profile from .aws/credentials file.
    """  
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-u','--username', type=str, help="Provide the registry username")
    optional.add_argument('-p','--password', type=str, help="Provide the registry password")
    optional.add_argument('-r','--registryname', type=str, help="Provide the name of the docker registry")
    optional.add_argument('-P','--awsprofile', type=str, help="Provide the profile to use from aws credentials file")
    required.add_argument('-B','--awsbucket', type=str, help="Provide the aws bucket name",required=True)
    required.add_argument('-F','--awsfilepath', type=str, help="Provide the exact path to the file location",required=True)
    args = parser.parse_args()

    if args.awsprofile is not None:
        AWS_PROFILE = args.awsprofile
    if args.username is not None:
        USERNAME = args.username
    if args.registryname is not None:
        REGISTRYURL = args.registryname
    if args.password is not None:
        PASSWORD = args.password
    main()
