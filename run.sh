#!/bin/sh
docker rm -f social
docker attach $(docker run --name social -dit -v $(pwd):/app -p 9000:9000 -p 8000:8000 rbiondi:social)
