#!/bin/bash
echo "Changing theme to $1...""
(feh -q --bg-fill ~/Pictures/"$1".jpg && picker("$1".jpg)) || (feh -q --bg-fill ~/Pictures/"$1".png && picker("$1".png)
