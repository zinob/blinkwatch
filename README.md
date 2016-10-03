# blinkwatch

A simple script to monitory an URL for falsy JSON values.

Currently the LED mappings are made in 2 places, just to make the code confusing, one for indexing GPIO ports to "easy to remember" numbers in blinkenq.py and one in the ini-file.

This is a quick-hack and might thus not be fit for any purpose what so ever.

## "Installation"

    cd /home/pi
    git clone github.com:zinob/blinkwatch.git`
   
"You probbably need to apt or pip some modules that i have forgotten to mention"

Run this to find what modules and packages i have installed and forgotten about

    /home/pi/blinkwatch.py
   
Copy system-files to relevant directories:

    cp blinkwatch.service /etc/systemd/system/blinkwatch.service
    cp gpiopff /etc/init.d/gpiooff
    cp gpiooff.py /usr/local/bin/gpiooff.py
   
enable the service with

     sudo update-rc.d -f gpiooff  defaults
     sudo systemctl enable  /etc/systemd/system/blinkwatch.service
     sudo systemctl start  blinkwatch.service

Why YES i do mix where i put executables, dont cry, it wont help.

ie if http://example.com/status

would return a JSON-struct of the form

    { 'juicemaker': true, 'webserver': true}

And you want to check it ever 10 seconds the config could look like this:

    [LEDS]
    working=0
    warning=1
    error=2
    [TARGET]
    URL=http://example.com/status
    INTERVAL=10
    [KEYS]
    juicemaker
    webserver

