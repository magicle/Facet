#!/bin/sh

GST_LAUNCH=/usr/bin/gst-launch-0.10


gst-launch-0.10 souphttpsrc location="$1" ! decodebin name=dec dec. ! queue !videoscale ! videorate ! ffmpegcolorspace ! "video/x-raw-yuv,                   format=(fourcc)YUY2" ! v4l2sink device=$2 dec. ! queue ! pulsesink              device=Facet_Sink

