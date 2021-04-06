# PublicBellBoi

**Please note that information such as tokens and credentials have been removed for security purposes.**

## What is BellBoi?

BellBoi is a service created to make it easier to find out how much time is left until the next period begins or ends.

## Why do we need an electronic service for this?

These are uncertain times. As we have learned throughout this year, the schedule can change frequently and with very little notice. BellBoi is build to be quickly modifiable so that it always
    reflects the most accurate times. In addition, who really wants to do math to figure out exactly how long is left until class is over? Finally, BellBoi is also integrated with Discord to provide
    realtime notifications for the start of class, which is useful for students that choose to stay home and who may lose track of time.
    
## Can I join the Discord for more features?

Of course! Click here <a href="https://discord.gg/62XNPr26Jr">(https://discord.gg/62XNPr26Jr)</a> to join. You may need to create an account with Discord if you have not done so in the past. Once you arrive, feel free to say hello! A list of commands and other information
     can be found in the various channels. Contact voitheiamath@gmail.com or Michael Elia directly if you need more help.

## Are the times guarenteed to be accurate?

No. BellBoi is a service coded and maintained by one student, and it is not in any way affiliated with Council Rock or its infrastructure (although it will probably only be useful to students within
    Council Rock because it is based on the CR schedule). A sincere effort will be made to keep BellBoi as accurate as possible, but the final word should always come from an official CR announcement.

## Why do BellBoi's timers not line up with international clocks such as iPhones and computers?

Have we discussed how Council Rock is weird? The clocks in the schools are offset variably from international clocks. The countdown timer is synced to the school clocks at Council Rock High School South in
    order to be more useful.

## How does BellBoi work?

The service is currently composed of three main parts. First there is a Google Calendar where all of the raw period and day information is entered. Google Calendar is used because it offers an easy interface
    for repeatable events, making it much faster to enter an entire month (or several) all at once. In addition, it is easy to edit the information if the school schedule changes with little warning.<br><br>The second
    piece of the project is a Discord bot. The bot is coded in Python, and runs on a Raspberry Pi throughout the school day. As BellBoi Online came later, this bot was built solely for the purpose of connecting
    Google Calendar with Discord. Integration with Google Calendar is accomplished via the usual OAuth2 process. At any time, an admin can trigger the bot to go and "fetch" all of the future events from the calendar.
    The bot will then store these events into a local text file to remove the strain of constantly fetching events. When someone runs the $ring command, the bot will look for the next upcoming period, and calculate the
    amount of time remaining until that period begins. In addition, the bot maintains an asynchronous loop that checks whether it is time to alert users that the next period is beginning. This loop will run once per second
    until it affirms that there is more than a minute until the next period, and will then run once a minute to reduce load.<br><br>The third part of the system is BellBoi Online. This was built on top of the existing ecosystem.
    BellBoi Online is constructed like many single page data-driven websites: it consists of a single HTML file with bundled CSS and Javascript to handle structure, style, and scripting in the most minimal way possible. Minimalism is
    emphasized because the service is intended to be run on low-performance devices in situations where the internet connection is not ideal. Period and day events are stored in a MySql database hosted, like Voitheia, on Hostinger servers.
    These are refreshed in the same function as the Discord bot's Google Calendar refresh system. Server side PHP handles the time calculations, returning to Javascript only the necessary information. Javascript will then keep track of
    a single date in the future, and each second calculate the time until that future date. Otherwise, the timer can fall behind when the user clicks off the tab. When the timer reaches negative values, it automatically refreshes the page.

## What are the future plans for BellBoi? (From a normal person's perspective)

In the future, BellBoi online may offer an "extended" view where it will also show the next few upcoming periods in the day in addition to the very next one. If you have any additional ideas, please email voitheiamath@gmail.com

## What are the future plans for BellBoi? (From a nerd's perspective)

Running BellBoi's Discord bot on a Raspberry Pi is not ideal. The Pi frequently loses network connection. Fortunately, BellBoi Online is only dependent on the bot for refreshing events, and continues to run when the bot is offline. 
    The bot (and Google Calendar integration) may soon be transitioned to a NodeJS based system that can run in the cloud. This would also allow me to introduce public HTTP API endpoints, allowing anyone to implement BellBoi in their own
    applications. It would also simplify BellBoi Online because it would no longer be necessary to maintain a database of future events.
