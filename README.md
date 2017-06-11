# zfsmon
A simple python script to health check ZFS pools and notify via email if there are faults.  
I wrote this script to monitor my own zfs instances, because ZFS itself doesn't have any built in monitoring or alerting capabilities, hope this is useful for anyone else with the same issue.

# Features
+ Health checks ZFS pools with "zpool status -x"
+ Sends out email notification if there is an issue

# Usage
Update the script config parameters at the top with your own SMTP mail settings.  
This script should be executed periodically via crontab or any other third party monitoring application, such as Nagios, Puppet, Ansible etc...

# TODO
+ Make into standalone service daemon