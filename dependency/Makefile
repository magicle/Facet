

all:	youtube-dl v4l2loopback skype4py

youtube-dl:
	sudo apt-get install youtube-dl
#	sudo wget --no-check-certificate https://yt-dl.org/downloads/2014.03.21.5/youtube-dl -O ./youtube-dl; sudo chmod a+x ./youtube-dl	

v4l2loopback:	
	sudo apt-get install git v4l-utils;
	git clone https://github.com/umlaeute/v4l2loopback.git;
	cd v4l2loopback/; \
	sudo make; \
	sudo make install; \
	sudo modprobe v4l2loopback video_nr=4; \
	cd utils \
	sudo cp v4l2loopback-ctl /usr/local/bin/


search:
	cd /usr/local/share/; \
	sudo wget http://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-i686.tar.bz2; \
	sudo tar xjf phantomjs-1.9.7-linux-i686.tar.bz2; \
	sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-i686/bin/phantomjs /usr/local/share/phantomjs;
	sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-i686/bin/phantomjs /usr/local/bin/phantomjs
	sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-i686/bin/phantomjs /usr/bin/phantomjs
skype4py: 
	git clone https://github.com/awahlig/skype4py.git;
	sudo apt-get install python-setuptools
	cd skype4py; \
	sudo python setup.py build; \
	sudo python setup.py install; 
install:
	sudo apt-get install gstreamer0.10-ffmpeg
	./install.sh timeout.png /dev/video4
