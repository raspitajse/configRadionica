#!/bin/bash
hostname -I | sed -r "s/([^\s]*)(\s+)([^\s*])/\1\n\3/g" > /tmp/IP
leafpad /tmp/IP