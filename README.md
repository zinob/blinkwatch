# blinkwatch

A simple script to monitory an URL for falsy JSON values.

Currently the LED mappings are made in 2 places, just to make the code confusing, one for indexing GPIO ports to "easy to remember" numbers in blinkenq.py and one in the ini-file.

This is a quick-hack and might thus not be fit for any purpose what so ever.

## "Installation"
`cd /home/pi` 
`git clone github.com:zinob/blinkwatch.git`
"You probbably need to apt or pip some modules that i have forgotten to mention"
`/home/pi/blinkwatch.py`
To find what modules and packages i have installed and forgotten about
`cp gpiopff /etc/init.d/gpiooff`
`cp gpiooff.py /usr/local/bin/gpiooff.py`
enable it with
`sudo update-rc.d -f gpiooff  defaults`
`cp blinkwatch.service /etc/systemd/system/blinkwatch.service`
`sudo systemctl enable  /etc/systemd/system/blinkwatch.service`
`sudo systemctl start  blinkwatch.service`

Why YES i do mix where i put executables, dont cry, it wont help.

ie if http://examplep.com/status

would return a JSON-struct of the form
   { 'juicemaker': true, 'webserver': true}

the config could look like
   []
