#!/bin/bash
./dockerclean.sh
./dockerbuild.sh
docker run --publish 5000:80 -d --name briserver bricontroller --restart always
