AC_INIT([Facet], [0.1])

AM_INIT_AUTOMAKE
AM_PATH_PYTHON([2.7])




# check for gstreamer0.10-ffmpeg

AC_DEFUN([AC_GST_MODULE],
         [AC_MSG_CHECKING(for module $1 in Gstreamer)
         dpkg-query -l $1 > /dev/null
         if test $? -ne 0 ; then
           AC_MSG_RESULT(not found)
           AC_MSG_ERROR(You need the module $1 available to Gstreamer for this package)
           fi
           AC_MSG_RESULT(found)
           ])

AC_GST_MODULE(gstreamer0.10-ffmpeg)


# check gstreamer...
AC_CHECK_PROG(GST_CHECK, gst-launch-0.10, yes)

if test x"${GST_CHECK}" != x"yes"; then
  AC_MSG_ERROR([gstreamer is not installed!])
fi

# check youtube-dl

AC_CHECK_PROG(YOUTUBE_CHECK, youtube-dl, yes)

if test x"${YOUTUBE_CHECK}" != x"yes"; then
  AC_MSG_ERROR([youtube-dl is not installed!])
fi


# check v4l-utils

AC_CHECK_PROG(V4L_CHECK, v4l2-ctl, yes)
if test x"${V4L_CHECK}" != x"yes"; then
  AC_MSG_ERROR([v4l-utils is not installed!])
fi


# check for Skype4Py

AC_DEFUN([AC_PYTHON_MODULE],
[AC_MSG_CHECKING(for module $1 in python)
echo "import $1" | python
if test $? -ne 0 ; then
AC_MSG_RESULT(not found)
AC_MSG_ERROR(You need the module $1 available to python for this package)
fi
AC_MSG_RESULT(found)
])

AC_PYTHON_MODULE(Skype4Py)


## Check for v4l2loopback module

AC_DEFUN([AC_KERNEL_MODULE],
         [AC_MSG_CHECKING(for module $1 in kernel)
         modinfo $1 > /dev/null 
         if test $? -ne 0 ; then
           AC_MSG_RESULT(not found)
           AC_MSG_ERROR(You need the module $1 available to kernel for this package)
           fi
           AC_MSG_RESULT(found)
           ])


AC_KERNEL_MODULE(v4l2loopback)



###########

AC_CONFIG_FILES([Makefile src/Makefile])

AC_OUTPUT
