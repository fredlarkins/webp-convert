# webp-convert
Convert PNG and JPG images into WEBP images automatically.

## Installation

Clone the repo:
```
git clone https://github.com/fredlarkins/webp-convert.git
```

Activate your virtual environment (optional):
```
cd webp-convert
python3 -m venv venv
```

Install dependencies:
```
pip install -r requirements.txt
```
'''

## Usage
Using the script is as simple as:
```
python converter.py
```

Running this command will:
- Look for `.png`, `.jpg` and .`jpeg` images in the present working directory;
- Convert them into `.webp` images;
- Save them in the same working directory with the same filename (plus the `.webp` extension)

## Command-line arguments

The script takes a few command-line arguments to make it a little more flexible.

### `-s, --source`
The directory containing the images to be converted - i.e. the source. For instance:

```
python converter.py -s holiday-snaps
```
Would convert all images in the `holiday-snaps` folder, saving them in the present working directory.

### `-d, --destination`
A directory in which to save the converted images - i.e. the destination.

**Note:** if this directory does not exist, the script will ask you to confirm whether you'd like to create it before proceeding. I found this helped escape instances where I mis-typed the destination.

For instance:
```
python converter.py -s holiday-snaps -d optimised-holiday-snaps
```
Would convert all images in `holiday-snaps` and save them in `optimised-holiday-snaps`.

### `-w, --width` **or** `-g, --height`
The width or height in px of the converted images. **Note:** you can use _either_ the `-w` _or_ the `-g` flag, but not both.

The images will be resized to be a maximum of width/height in px. If the original image is _smaller_ than the width/height supplied, it will be left untouched (i.e. not scaled up).

The aspect ratio of the image will be preserved: as such, only one of these two flags can be supplied. For instance:
```
python converter.py -s holiday-snaps -d optimised-holiday-snaps -w 1000
```
Would convert all images in `holiday-snaps`, save them to `optimised-holiday-snaps` and resize them to be a maximum width of 1000px.


## Applications
Like most of the Python scripts I write (😅), I'll be running this as a Cron Job. In my case, it'll be on [my blog](https://freddielarkins.xyz) server to optimise my images. That way, I don't have to worry about manually converting them every time I write an article.

Otherwise, you could use it as a one-off to batch convert a load of images. The terminal will display a progress bar 

```console
$ python converter.py -s holiday-snaps -d optimised-holiday-snaps -w 1000

The directory "optimised-holiday-snaps" does not exist. Would you like to create it? (Y/n) > y

Converting images...
100%|██████████████████████████████████████████████████████████████| 25/25 [00:10<00:00,  2.30it/s]

Converted 25 images to WEBP, saving 14.2 MB - a 93% decrease.
```