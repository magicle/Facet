#!/bin/sh

v4l2-ctl -d $2 -c timeout=1000

v4l2loopback-ctl set-caps "video/x-raw-yuv,format=(fourcc)YUY2, width=320,     height=240" $2

v4l2loopback-ctl set-timeout-image $1 $2

pactl load-module module-null-sink sink_name=Facet_Sink

