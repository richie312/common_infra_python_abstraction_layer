#!/bin/sh
echo "127.0.0.1 broker" >> /etc/hosts
exec "$@"