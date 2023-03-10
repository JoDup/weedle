#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

raspistill -o /home/weedle/weedlecode/plantdiagnostic/photo/$DATE.jpg
