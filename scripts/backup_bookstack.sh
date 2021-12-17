#!/bin/bash

ssh rroche@192.168.0.79 ~/bookstack_backup.sh;scp "rroche@192.168.0.79:~/bookstack-files_*" ~/Downloads/;ssh rroche@192.168.0.79 rm "~/bookstack-files_**"
