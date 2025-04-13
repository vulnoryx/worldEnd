#!/bin/bash

wal -i $1 -n

swww img $1 --transition-step 1 --transition-fps 165 --transition-type wipe