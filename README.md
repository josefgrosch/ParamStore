## ParamStore.py

### How to use.


    paramStore --help
    usage: paramStore.py [-h] [-a] [-d] [-D] [-f] [-k KEY] [-l] [-t] [-v VALUE] [-V]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --add             Add key / value pair
      -d, --debug           Turn on debugging output
      -D, --delete          Delete key / value pair
      -f, --find            Find a key / value pair
      -k KEY, --key KEY     Parameter store key.
      -l, --list            List arameter store key.
      -t, --terse           Terse output
      -v VALUE, --value VALUE
                        Value to be stored
      -V, --version         Version of tool

- help - Outputs the above usage message

- add - Adds a key/value pair to the AWS parameter store. Both the option --key < key > and --value < value > must be provided.  

- debug - A boolean flag that turns on the output of debugging information

- delete - Delete a key/value pair form the AWS parameter store. The option --key < key > must be provided.

- find - Find a given key/value pair in the AWS parameter store. The option --key < key > must be provided.

- key - The key of the key/value pair.

- list - List all the key/value pairs in the AWS parameter store.

- terse - A boolean flag that causes only the essential information to be outputted. 

- value - The value of the key/value painr.

- version - Returns the current version of the tool.

This tool is used to interact with the Amazon Simple Systems Manager (SSM) service. The data store that is accessed is a private store based on the AWS Account ID. A properly configured AWS environment ie. the command `aws configure` has been performed and the appropriate environment variables have been set.

### Examples

- paramStore --add --key /aracade/bad_van/user --value "Bob Dobbs"
