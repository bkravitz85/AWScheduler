#!/usr/bin/python
#
# Auto-start and stop EC2 instances through GMTIME
#
import boto, datetime, sys
import boto.ec2
from time import gmtime, strftime, sleep

# AWS credentials
aws_key = ""
aws_secret = ""

# The instances that we want to auto-start/stop
instances = [
    # You can have tuples in this format:
    # [instance-id, name/description, startHour, stopHour, ipAddress]
    ["", " Integration Test Server", "18", "19", ""],
    ["", " Onboarding Demo", "18", "19", ""]

]

# --------------------------------------------

# If its the weekend, then quit
# If you don't care about the weekend, remove these three 
# lines of code below.
weekday = datetime.datetime.today().weekday()
if (weekday == 5) or (weekday == 6):
    sys.exit()

# Connect to EC2
#conn = boto.connect_ec2('us-west-2')
conn = boto.ec2.connect_to_region("us-west-2")

# Get current hour
hh = strftime("%H", gmtime())

# For each instance
for (instance, description, start, stop, ip) in instances:
    # If this is the hour of starting it...
    if (hh == start):
        # Start the instance
        print('Starting now!')
        conn.start_instances(instance_ids=[instance])
        # Sleep for a few seconds to ensure starting
        sleep(60)
        # Associate the Elastic IP with instance
        print('Resuming... Start')
        if ip:
            conn.associate_address(instance, ip)

    # If this is the hour of stopping it...
    if (hh == stop):
        # Stop the instance
        print('Instance Stopped for this Hour')
        conn.stop_instances(instance_ids=[instance])
