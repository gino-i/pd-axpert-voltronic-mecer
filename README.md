# pd-axpert-voltronic-mecer

I am using a MECER Inverter (3000VA/3000W (24V) Pure Sinewave) which has a USB "fat printer cable" connection on it, which I have used to connect to my raspberrypi (or lepotato in my case). Don't have PV solar panels "yet", just inverter and batteries setup at the moment.

downloaded and installed the playbackdesign software to query the inverter (https://www.playbackdesign.com/pd-axpert)

I did not use their (playbackdesign) android application - have an ios device myself, hence the reason for looking at a local webserver thingy - anyway, the playbackdesign "pd-axpert" produces a local JSON file which can be queried (see screenshot 0.json plain), also produces historical json files (20MB per file) which can be queried for historical purposes if required.

I know a bit about IT and networking, but do not know much about html code or even programming, but can find my way around - with the help of chatgpt and several weekends I got a nice realtime web interface to check on the important things :) (using local IP server - vpn/zerotier)

and have some form of historical graphs where/if required.

I am also not using any database, just the json files. At the moment it is good enough for what I would like out of it, barring beautifying the interface, the reports, and possibly using some sort of alert (ntfy) when power does go down or load is too much. but that is another weekend/project altogether it looks like.

I would unfortunately only be able to answer questions pertaining to how my setup is as I did not do it for any other inverter. So will try to answer where I can. 
