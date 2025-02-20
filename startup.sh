#!/bin/bash
apt-get update && apt-get install -y libgl1-mesa-glx
python ocr.py  # Run your Flask app