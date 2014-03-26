#!/bin/sh
# Shuts down pyramid application
# Created by David Hietpas (hietpasd@uwosh.edu)

kill -9 $(cat lock.pid)
sleep 1
echo "Shutting Down Pyramid App..." >> event.log
rm lock.pid