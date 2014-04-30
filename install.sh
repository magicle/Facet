#!/bin/sh

V4L2_CTL=/usr/bin/v4l2-ctl
V4L2LOOPBACK_CTL=./v4l2loopback/utils/v4l2loopback-ctl
PACTL=/usr/bin/pactl

$V4L2_CTL -d $2 -c timeout=1000

$V4L2LOOPBACK_CTL set-caps "video/x-raw-yuv,format=(fourcc)YUY2, width=320,     height=240" $2

$V4L2LOOPBACK_CTL set-timeout-image $1 $2

$PACTL load-module module-null-sink sink_name=Facet_Sink

