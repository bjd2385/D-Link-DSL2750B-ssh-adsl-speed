#!/bin/bash
result=$(expect "$(pwd)/scriptSSH" | tr -d " " | grep -P "RXbytes:")
echo "$result"