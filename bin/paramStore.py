#!/usr/bin/env python3

# -----------------------------------------------------------------------
#
#                             < paramStore >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : paramStore.py
#
# Author       : Josef Grosch
#
# Date         : 19 Nov 2021
#
# Modification : None
#
# Application  : paramStore
#
# Description  : A stub program to test galaga service pulling from
#                AWS parameter store
#
# Notes        :
#
# Functions    :
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                              Copyright
#
#                    (C) Copyright 2021 Appepar, Inc.
#
#                         All Rights Reserved
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# Import
#
# -----------------------------------------------------------------------
import os, sys
import boto3
import json
import argparse
import pprint
from datetime import date, datetime
from botocore.exceptions import ClientError


# -----------------------------------------------------------------------
#
# listParam
#
# -----------------------------------------------------------------------
def listParam(ssmClient, args):
    returnDict = ssmClient.describe_parameters()
    
    return returnDict
    #
    #
    #

# -----------------------------------------------------------------------
#
# deleteParam
#
# -----------------------------------------------------------------------
def deleteParam(ssmClient, args):
    returnDict = findParam(ssmClient, args)
    returnCode = returnDict['ResponseMetadata']['HTTPStatusCode']
    if returnCode == 200:        
        returnDict = ssmClient.delete_parameter(Name=args.key)

    return returnDict
    #
    #
    #
    
# -----------------------------------------------------------------------
#
# addParam
#
# -----------------------------------------------------------------------
def addParam(ssmClient, args):
    returnDict = ssmClient.put_parameter(
        Name=args.key,
        Value=args.value,
        Type='String',
        Overwrite=True,
        Tier='Standard',
        DataType='text')
    
    return returnDict
    #
    #
    #

# -----------------------------------------------------------------------
#
# jsonDatetimeSerializer
#
# -----------------------------------------------------------------------
def jsonDatetimeSerializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
    #
    #
    #
    
# -----------------------------------------------------------------------
#
# findParam
#
# -----------------------------------------------------------------------
def findParam(ssmClient, args):

    try:
        returnDict = ssmClient.get_parameter(Name=args.key,
                                             WithDecryption=True)
    except ClientError as e:
        i  = 0
        aJsonStr = '{"Parameter":{"ARN":"","DataType":"","LastModifiedDate":"","Name":"","Type":"","Value":"","Version":2},"ResponseMetadata":{"HTTPHeaders":{"connection":"","content-length":"","content-type":"","date":"","server":"","x-amzn-requestid":""},"HTTPStatusCode":9,"RequestId":"","RetryAttempts":0}}'

        aDict = json.loads(aJsonStr)
        
        if e.response['Error']['Code'] == 'ParameterNotFound':
            aDict['ResponseMetadata']['HTTPStatusCode'] = 404
            returnDict = aDict
    
    return returnDict
    #
    #
    #
    
# -----------------------------------------------------------------------
#
# processReturnDict
#
# -----------------------------------------------------------------------
def processReturnDict(returnDict, args):
    if args.add:
        i = 0
        statusCode = returnDict['ResponseMetadata']['HTTPStatusCode']
        if statusCode == 200:
            if args.debug:
                print("Value {} inserted".format(args.value))
        else:
            print("ERROR: status code {} returned".format(statusCode))
        #
    elif args.delete:
        j = 0
        statusCode = returnDict['ResponseMetadata']['HTTPStatusCode']
        if statusCode == 200:
            if args.debug:
                print("Value {} deleted".format(args.value))
        else:
            print("ERROR: status code {} returned".format(statusCode))
        #
    elif args.list:
        l = 0
        statusCode = returnDict['ResponseMetadata']['HTTPStatusCode']
        if statusCode == 200:
            pprint.pprint(returnDict)
    elif args.find:
        k = 0
        statusCode = returnDict['ResponseMetadata']['HTTPStatusCode']
        if statusCode == 200:
            if args.terse:
                key = returnDict['Parameter']['Name']
                value = returnDict['Parameter']['Value']
                print("Data found\n\tKey  : {}\n\tValue: {}\n".format(key, value))
            else:
                pprint.pprint(returnDict)
            if args.debug:
                print('Parameter information:')
                print(json.dumps(returnDict['Parameter'],
                                 indent=4,
                                 default=jsonDatetimeSerializer))
        elif statusCode == 404:
            print("ERROR: key {} not found".format(args.key))
        #
    return
    #
    #
    #
    
# -----------------------------------------------------------------------
#
# main
#
# -----------------------------------------------------------------------
def main():
    # key: /dev/ec2Instance/type

    version    = '0.5'
    earlyExit  = False
    exitCode   = 0
    toolName   = os.path.basename(__file__)
    AWS_REGION = os.environ.get('AWS_DEFAULT_REGION')

    # --arcade - /arcade/{arcade_name}/{key}

    ssmClient = boto3.client("ssm", region_name=AWS_REGION)

    parser = argparse.ArgumentParser(toolName)

    parser.add_argument('-a', '--add', help='Add key / value pair',
                        action='store_true')
    
    parser.add_argument('-d', '--debug', help='Turn on debugging output',
                        action='store_true')
    
    parser.add_argument('-D', '--delete', help='Delete key / value pair',
                        action='store_true')

    parser.add_argument('-f', '--find', help='Find a key / value pair',
                        action='store_true')

    parser.add_argument('-k', '--key', help='Parameter store key.')
    
    parser.add_argument('-l', '--list', help='List arameter store key.',
                        action='store_true')
    
    parser.add_argument('-t', '--terse', help='Terse output',
                        action='store_true')

    parser.add_argument('-v', '--value', help='Value to be stored')

    parser.add_argument('-V', '--version', help='Version of tool',
                        action='store_true')

    args = parser.parse_args()

    if args.add:
        if args.value is None:
            print(f"{toolName} ERROR: a value is required to add key / value pair.")
            earlyExit = True
            exitCode = 101
            
        if args.key is None:
            print(f"{toolName} ERROR: key value missing")
            earlyExit = True
            exitCode = 101
            
        if not earlyExit:
            returnDict = addParam(ssmClient, args)
            processReturnDict(returnDict, args)
        # End of add
    elif args.delete:
        if args.key is None:
            print(f"{toolName} ERROR: key value missing")
            earlyExit = True
            exitCode = 101

        if not earlyExit:
            returnDict = deleteParam(ssmClient, args)
            processReturnDict(returnDict, args)
        # End of delete
    elif args.find:
        if args.key is None:
            print(f"{toolName} ERROR: key value missing")
            earlyExit = True
            exitCode = 101

        if not earlyExit:
            returnDict = findParam(ssmClient, args)
            processReturnDict(returnDict, args)
        # End of find
    elif args.version:
        print(f"{toolName} version: {version}")
        exitCode = 0
        # End of version
    elif args.list:
        returnDict = listParam(ssmClient, args)
        processReturnDict(returnDict, args)
        # End of list
    else:
        print("How did we get here ?")
        print("No argument provided.")
        # 0x57 0x54 0x46 == WTF
        exitCode = 5723206 # WTF
        
        
    sys.exit(exitCode)
    #
    #
    #


# -----------------------------------------------------------------------
#
# Endtry point
#
# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()



# -----------------------------------------------------------------------
#
#                        < End of paramStore.py >
#
# -----------------------------------------------------------------------
