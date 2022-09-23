# MediaSorter

This project aims to provide a simple but efficient way to sort your media, primarily images and videos.
PyQt5 is used to provide a clean and stable UI, as well as some common useful features.

## Installation

You will need to install Python3 (version 3.8 at least). Then, install required packaged in `requirements.txt`.
Qt5 is used via the pyQt bindings. Version 3.15 at least is required.
This project hasn't been tested on another platform than Linux, so run it at your own risks if you want to use it on other OSes

## Usage

The main windows are `imageSorter.py` and `videoSorter.py`. Run either of these scripts to start the program.

The main UI consists of a list of bindings, and a media viewer.

### Bindings
Each key can be bound to a given action:
- "move" to move a file to a given folder. It will then be removed from the list
- "copy" to only copy it. It won't be removed from the list
- "nothing" to not do anything (consider this as a placeholder)

#### Default
In addition, some keys are bound by default to some actions and cannot (yet) be edited:
- "Backspace"=>"hide" will remove current entry from the list
- "Home"/"End" respecitvly go to the first/last entry in the list
- "Del" will delete the file (by putting it to your trash folder)
- "Left"/"Right" allows you go to previous/next media
- "Esc" will close the application

#### Specific to imageSorter
- "+"/"-" will zoom-in
- "0" will reset zoom to 100%
- "1" will reset zoom to the original "ideal" ratio
- "Inser" will try to copy the current image to your clipboard 

#### Specific to videoSorter
- "+"/"-" will increase/decrease volume
- "0" will reset the volume to 50
- "Space" will pause/resume video

#### Mouse
In addition, some mouse actions are available:

For imageSorter:
- Maintain mouseMiddleClick and move the mouse to move the image
- mouseWheel will increase/decrease image zoom

For videoSorter:
- mouseWheel will increase/decrease the volume

### Quick start
- First, go to "File"->"Open Directory" and select the directory you want to sort media from.
Files will be indexed, and all media compatible with current mode will be displayed.
- Go to "File"->"New Config", and choose where you want to save your configuration.
- Then, go to "Edit"->"Edit Configuration". This will open a new Dialog.
- Click on the "New binding" button, click on the "Record" button, press the key you want to bind an action to, then "Validate"
- Choose from the list the action you want to bind to this key, then select the path you want this action to apply to
- Validate, and the configuration will be automaticaly saved

Later, when you'll restart the program, you can select your previous config file by going to "Open Configuration"

### Directory Index & Cache
For huge directories, you might want to save the indexing results in a file to avoid reindexing the whole folder each time.
You can do this by going to "File"->"Save Directory Index", and you can load it with "File"->"Load Directory Index"

### Random filenames
By default, when you copy/move a file to a directory, it will check if the file doesn't already exist.
If that's the case, it will append to the filename a random string

### Zooming and image ratio conservation
One of the important features of imageSorter is that it preserves the original image ratio.
By default, when displaying an image, the program will calculate the zoom ratio required so that the whole image can fit in the current viewport while not altering the ratio.
This works pretty well for regular images without weird ratios, but can be require some adaptation for example for comics.

## TODOs
See `TODO.md` file

## Contributions
Contributions are hugely appreciated. It is basically my first "own" open-source project so feel free to also give appreciations, comments and constructive criticism!

## License
This project is provided under the `Mozilla Public License 2.0`. See `LICENSE.md`
