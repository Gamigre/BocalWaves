# BocalWaves
An Audacity script aimed to ease sonification-based glitch art. Non commercial use only
You'll need to have up-to-date vrsions of thoses softwares :
 audacity
 python
 SoX
 ffmpeg
 nomacs
in order to use this script as intended.


user guide is a complete WIP 

Use the script by activating scripts in audacity, then opening the .au blank project that comes with Bocalwaves, then launch bocalwaves.py with your terminal.
bocalwaves will apply audacity effects with specified settings, gradually, on a specified number of images
You can work with a mp4 file, (the number of frames will be the span of the effect) or a single .bmp image (you specify the span of the effect)

Start by putting your bmp file in the ExportedBMP folder, then launche the "0" command on the terminal, a SoX command will automatically convert your BMP in a WAV file that will go in the "input" folder, relaunch the script then apply the effect you want and voila !

If you're using a video, start by putting your video in the InputMP4 folder and a ffmpeg script will export your vid as bmp files for you, before exporting thoses bmp frames in wav.

Some output files can be unreadables by standard image viewers, and I recommend using nomacs and its batch processing functions to convert everything in PNG or something, and then using ffmpeg to make a video out of your work. Some ffmpeg commands are included as examples.

I'm sorry because i hate unclear instructions especially when you're an artist that doesn't really know any of this nerd stuff like me lol but I'm in a hurry, i'll made a guide properly, one day.
Good luck !
