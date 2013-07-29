#!/bin/sh
HOST=ec2-23-22-149-13.compute-1.amazonaws.com
scp -i ~/.ssh/kp1.pem coffee.py hadoop@$HOST:udfs/coffee.py
scp -i ~/.ssh/kp1.pem tw_stream.py hadoop@$HOST:udfs/tw_stream.py
scp -i ~/.ssh/kp1.pem twitter_places.py hadoop@$HOST:udfs/twitter_placs.py
scp -i ~/.ssh/kp1.pem pig_util.py hadoop@$HOST:udfs/pig_utils.py

