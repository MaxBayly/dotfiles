#!/bin/bash
convert "$1" -format %c -colorspace LAB -colors 6 histogram:info:- | cut -d "s" -f 2 | tr -d "srgb" | tr -d "(" | tr -d ")" | python3 palette.py