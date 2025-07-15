#!/bin/bash
set -e
./install.sh
docker run -p 8000:8000 shipping-orders-app
