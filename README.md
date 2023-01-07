# BocalWaves
An Audacity script aimed to ease sonification-based glitch art. ***Non commercial use only***. Please reach out if you're a studio or an agency interested in working with bocalwaves.

You will need to have up-to-date versions of thoses softwares :
-  audacity
-  python
-  SoX
-  ffmpeg
-  nomacs
in order to use this script as intended.


(user guide is a complete WIP, use at your own discretion) 
### Setting up Bocalwaves 

##### 1. Python
The script uses several python plugin to work so be sure to install them:
- pip install colorama
- pip install sox
- pip install ffmpy

You might need a proper version of sox and a proper version of ffmpeg installed on your machine and in your PATH.

##### 2. Audacity
Audacity must be installed (of course) and should have a certain way to import raw files set up. In order to do this you just need to import manually one raw file like this:
1.  Open Audacity
2. File > Import > Raw Data
3. Choose a .bmp image file, as we will use that later (you can do that with any file tbh, but bmp should be used just to be sure)

4. Settings to use :
Encoding: U-Law /
Bytes order: Little endian /
Channels: 1 Channel (Mono) /
Leave the rest as it is (0, 100, 44100) and click on import

5. Export the file; File>Export>Export audio..
6. Choose "other, uncompressed formats" in the dropdown menu as your export format and "header : Raw, headerless" then "Encoding: U-Law" in the options below.
7. Do not bother with the metadata and click OK. You should now have a .raw file nearly identical to your source material. You will use **nomacs** to open it as it's a more robust image viewer than the default windows one and, while our image isn't glitched yet, it will soon be a lot harder for usual apps to deal with it.
8. Audacity import and export are now set up ! You shouldn't touch that too much.

One last thing to do is to activate the pipe scripts in audacity, which allow us to communicate with audacity with python. It's in the preferences Under "Modules" enable mod-script-pipe if it isn't already.

##### 3. Folder structure
Here's how to set up your folder to work with Bocalwaves:
1. Create a folder named "Bocalwaves" on a disk with several gigabytes available to make room for the script to work and place **bocalwaves.py** inside, along with **pipeclient.py**, a script you'll get directly from Audacity themselves here : https://github.com/audacity/audacity/blob/d5685fe034bf0f3138480893a65190b7f51b7890/scripts/piped-work/pipeclient.py

2. Inside, create the several folders :
- input
- inputMP4
- output
- ExportedBMP

Then, open Audacity and directly save a *blank* project in the Bocalwaves folder. Call it Open_along_with_py_script for example, as you will use it to launch audacity directly from our Bocalwaves folder. Hopefully, you're done.


## Using Bocalwaves

If you want to work with a video, it should be a .mp4 file and named *input.mp4*. Place it in the inputMP4 folder.
If you're working with a single image, skip this part and place your image in the ExportedBMP folder. You can convert any picture into .bmp files with most image editors out there, even Paint should do that.

Close any remaining instance of Audacity and open your blank project by double clicking on it. It is important to open Audacity that way as it permits Audacity and our scripts to communicate within the same folder.
Once everything is set up, start a powershell terminal by shift+right-clicking in your Bocalwaves folder and launch the script with "python bocalwaves.py"

You'll be greeted with the version number and a numbered list of options. 
***Start with 0*** it will automatically convert each frame of your video (if there isn't a video it will throw an error, don't worry about it if you're just using a single pic) into BPM pictures which will be put in the exportedBMP folder. It will then pick what's in that folder to convert it again into .wav sound files (basically, it cuts a tiny part of the file called the header and replace it as a .wav header to trick Audacity into treating our files as sound).

As the script exits after each use, relaunch it by typing "python bocalwaves.py" or using you up-arrow key to retrieve the last command used. You're now free to chose any other numbered option, or export files again with 0.

All the effects and options of Audacity are yet to be implemented and probably will not be before a long time but it's quite easy to do if you're motivated and know python (i'm neither)

Important precision to make about Bocalwaves commands; for mosts effect it asks for  min(imum) values and max(imum) values Thoses are the values the effect will start with and ends with. They're currently applied following a linear progression, I'd love to have some fancy ease-in and ease-out curves but I don't know how to lol.

It also asks for the number of outputs. If you use a single image, this image will be exported as many times as the output number you entered. The first image will have the min values applied, and the last will have the max values applied, with a progression toward theses values applied in a linear way to the images in between theses two.

If you uses a video, it will disregard the number of output you entered and instead use the first exported frame as your first, minimum values export and the last frame as your maximum values export and treat every frame inbetween accordingly.

All outputs are made in the "output" folder and they will overwrite each other so be careful.  The outputs are in .raw file formats

Some output files can be unreadables by standard image viewers, and I recommend using nomacs and its batch processing functions to convert everything in PNG or jpeg, and then using ffmpeg or any standard video editor (but ffmpeg is *much quicker* to make a video out of your work. Some ffmpeg commands are included as examples.

PS: Bocalwaves wasn't intended to function as an image editor or another easy plug n play glitch art app but more as an experimental art program and a another way to make glitch art while keeping its core *raison d'être*; being a reflective way to look at errors in general, and being amazed and pleasantly surprised by the random beauty the machine can output. Bugs and errors (most of them at least), ugly and undesirable ouputs are parts of the exploratory process. There's no guide or rule to get a perfect render but you can look at the notes included in the github to read what I found interesting about some commands. please reach out or open an issue if you have questions about it.

Good luck !
