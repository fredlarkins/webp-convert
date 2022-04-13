from PIL import Image
from pathlib import Path
from tqdm import tqdm
import sys
from argparse import ArgumentParser

'''
Step 1: parse the command-line arguments for the script.
'''

# instantiating an ArgumentParser object
parser = ArgumentParser(description='Convert JPG and PNG images into WEBP.')


# the first arg: the source directory containing images to convert
parser.add_argument(
    '-s',
    '--source',
    type=str,
    help='Path to the source directory containing the images to be converted.',
    required=True
)

# the second arg: the target directory for the converted images
parser.add_argument(
    '-d',
    '--destination',
    type=str,
    help='Path of the target directory for the converted images.',
    required=False,
    default='output'
)

# the third argument is a group: user needs to specify either a width or a height
# credit to StackOverflow for this answer: https://stackoverflow.com/questions/11154946/require-either-of-two-arguments-using-argparse
dimensions = parser.add_mutually_exclusive_group(required=True)

# width
dimensions.add_argument(
    '-w',
    '--width',
    type=int,
    help='''
    The width in px for the image to be resized to. 
    If the image is smaller than the width specified, it will be left as is.
    ''',
    
)

# height
dimensions.add_argument(
    '-g',
    '--height',
    type=int,
    help='''
    The height in px for the image to be resized to.
    If the image is smaller than the height specified, it will be left as is.
    '''
)


# parsing the arguments provided when running the script, saving them to an args variable
args = parser.parse_args()


# extracting the arguments from our args variable
SOURCE = args.source
DESTINATION = args.destination
WIDTH = args.width
HEIGHT = args.height

if not Path(SOURCE).exists():
    sys.exit(f'Input directory "{SOURCE}" does not exist. Check the arguments you provided when running the script and try again!')

# making the output directory if it doesn't already exist

'''
Step 2: loading all the images into a list to iterate over
'''
# saving the images that have already been converted in a variable
# we can use this to ensure that we're not converting images over and over again unnecessarily
if Path(DESTINATION).exists():
    already_converted = [file.stem for file in Path(DESTINATION).iterdir()]

    # now iterating through the source destination files, checking they're not in the 'already_converted' list
    images_to_convert = [image for image in Path(SOURCE).iterdir() if image.stem not in already_converted]

    # in case there's nothing new to convert
    if not images_to_convert:
        sys.exit('No (new) images to convert found in source directory. Exiting program.')

else:
    create_directory_choice = input(f'The directory "{DESTINATION}" does not exist. Would you like to create it? (Y/n) > ')
    
    if not create_directory_choice or create_directory_choice.lower().strip() == 'y':
        Path(DESTINATION).mkdir(parents=True)
        images_to_convert = [image for image in Path(SOURCE).iterdir()]
    
    else:
        sys.exit('User chose not to create a new directory. Try running the script again.')


'''
Step 3: defining a function that'll resize and convert an image
'''
def resize_and_convert_to_webp(im:Image.Image, filename:Path, dimensions=tuple):
    # checking whether the dimensions supplied are actually smaller than the image
    # if so, skip the resize stage
    if (im.height + im.width) < (dimensions[0] + dimensions[1]):
        pass
    else:
        im = im.resize(size=dimensions)
    
    converted_im_path = Path(DESTINATION, f'{filename.stem}.webp')
    im.save(converted_im_path, format='webp')
    return converted_im_path.stat().st_size



'''
Step 4: iterating through the list of images to convert and, you guessed it, converting them!
'''
total_original_bytes = sum([image.stat().st_size for image in images_to_convert])
total_new_bytes = 0

for path in tqdm(images_to_convert):
    with Image.open(path) as im:
        if WIDTH:
            HEIGHT = int(im.height * (WIDTH/im.width))
        else:
            WIDTH = int(im.width * (HEIGHT/im.height))

        converted_image_bytes = resize_and_convert_to_webp(im, path, (WIDTH, HEIGHT))
        total_new_bytes += converted_image_bytes

print(
f'''
Converted {len(images_to_convert)} images to WEBP, saving {total_original_bytes - total_new_bytes} bytes - a {int((total_original_bytes - total_new_bytes) * 100 / total_original_bytes)}% decrease.
'''
)
        
        

