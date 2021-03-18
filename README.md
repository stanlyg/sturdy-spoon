# sturdy-spoon
A Calendar Reading and Scheduling widget

## Why is this called Sturdy Spoon?
Why not? It's an easy enough name to remember. And this does spoonfeed me alerts related to my calendar.

Really, there's no meaning to the name. The name was vaguely inspired by [Screaming Liquid Tiger](https://github.com/herrbischoff/screaming-liquid-tiger).

## Prerequisites
Python 3.4 or newer. (Built using Python 3.7)
- ConfigArgParse (available via pip, or likely as a module for your OS)
- ICalendar (available via pip, or likely as a module for your OS)
- PathLib (Python Standard Library, may not actually be required)
- DateTime (Python Standard Library)
- OS (Python Standard Library)
- Requests (available via pip, or likely as a module for your OS)

## Usage via command line:

```sh
python calreader2.py --url http://some.url/calendar.ics --verbose
```

The script will read the file at http://some.url/calendar.ics, and create an `at` event for each event occurring "today". 

## Usage with a configuration file:

Create the file ~/.config/calreader.ini with content similar to the following:

```ini
[calreader]
url = https://some.url/calendar.ics
prefix = /home/stanlyg/scripts
suffix = .sh
queue = s
verbose = False
everything = False
```

Then run
```sh
python calreader2.py
```

The script will read the file from the url designated in the config file, http://some.url/calendar.ics, 3
and create an `at` event for each event occurring "today" (based on the local clock/timezone)

## External Scripts

You will need to create the appropriate scripts. One script I use is:

*meeting.sh*
```sh
#!/bin/sh
notify-send -u low -t 60000 -i appointment-now 'Meeting'
/usr/bin/ogg123 -q -d alsa -o 'dev:plughw:2,1' /home/stanlyg/sounds/meeting.ogg
```

That script pops a notification in the system tray, and then immediately plays the meeting.ogg sound file. 
The 'dev:plughw:2,1' forces the particular sound card that meets my requirements. 

## Daily Use
You could run this manually every day, but I have a cronjob configured to run at 06:00 local time every morning, and it retrieves my events for the day. 
My calendar can change on a daily basis, so there's no advantage to me in going past one day. 
