#!/bin/bash

ssh rroche@192.168.0.79 ~/backup_firefly_db.sh;scp "rroche@192.168.0.79:~/firefly_backup*" ~/Downloads/;ssh rroche@192.168.0.79 rm "~/firefly_backup*"
