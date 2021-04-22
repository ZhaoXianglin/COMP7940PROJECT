#!/bin/bash
set -e
  
echo '载入环境变量'
export GOOGLE_APPLICATION_CREDENTIALS=secert.json
python3 app/main.py