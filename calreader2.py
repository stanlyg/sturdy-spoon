import configargparse
from pathlib import Path 
from icalendar import Calendar, Event
import datetime
import os
import requests

parser = configargparse.ArgParser(default_config_files=['~/.config/calreader.ini'],description="""
        Downloads a webcal file and schedules an external file to run at 
        the beginning of each event. This can be used to play a sound or 
        show an alert with an external script.""")
parser.add("-c","--config", help="""
        Specify configration file to use. Command line options override 
        the config file. Defaults to ~/.config/calreader.ini""",is_config_file=True)

#ArgumentParser(description="Downloads a webcal file and schedules an external file to run at the beginning of each event. This can be used to play a sound or show an alert with an exteranl script.")
parser.add_argument("--url",help="URL of a webcal or ICS file to parse",default="",required=True)
parser.add_argument("-p","--prefix", help="Prefix or path to executable script. Defaults to ~/",default="~/")
parser.add_argument("-s","--suffix", help="Suffix of path to executable script. Defaults to .sh",default=".sh")
parser.add_argument("-d","--dryrun", "--debug", help="Dry run mode. Shows commands to be executed, but does not schedule them",action="store_true",default=False)
parser.add_argument("-q","--queue", help="Queue to use for the at command. Limited to a single letter. Defaults to s (as in schedule or sound)",default="s")
parser.add_argument("-v","--verbose", help="Show details about the process.",action="store_true",default=False)
parser.add_argument("-e","--everything", help="Process all events in the file. Defaults to today only",action="store_true",default=False)

options = parser.parse_args()

resp = requests.get(options.url)

if resp.status_code != 200:
    print (f'Unable to download calendar from URL:\n{options.url}\nPlease check your schedule elsewhere!')
    exit(-1)

cal = Calendar.from_ical(resp.content)

today = datetime.datetime.now()
if options.everything == False:
    print (f'Loading events for {today.date()}.')
else:
    print (f'Loading all events in calendar.')

for c in cal.walk():
    if c.name == 'VEVENT':
        dtstart = c.decoded('DTSTART')
        dtend = c.decoded('DTEND')
        if options.everything or dtstart.date() == today.date():
            if options.verbose:
                print (f"{c['DESCRIPTION']} begins at {dtstart.astimezone()} and ends at {dtend.astimezone()}.")
            exefile = c['DESCRIPTION'].replace(' ','-').lower()
            timestr = dtstart.astimezone().strftime('%Y%m%d%H%M')
            if options.dryrun:
                print ('Command not executed: ',end='')
            atcmd = f"at -q {options.queue} -f {options.prefix}{exefile}{options.suffix} -t {timestr}"
            if options.dryrun or options.verbose:
                print(atcmd)
            if not options.dryrun:
                os.system(atcmd)
