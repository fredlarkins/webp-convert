from typing import Union
from PIL import Image
from pathlib import Path
import tqdm
import sys
from argparse import ArgumentParser
from humanize import naturalsize

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
    default='.'
)

# the second arg: the target directory for the converted images
parser.add_argument(
    '-d',
    '--destination',
    type=str,
    help='Path of the target directory for the converted images.',
    required=False,
    default='.'
)

# the third argument is a group: user needs to specify either a width or a height
# credit to StackOverflow for this answer: https://stackoverflow.com/questions/11154946/require-either-of-two-arguments-using-argparse
dimensions = parser.add_mutually_exclusive_group()

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
SOURCE = Path(args.source)
DESTINATION = Path(args.destination)
WIDTH = args.width
HEIGHT = args.height


'''
Step 2: checking whether the input and output directories exist, then loading all the images into a list to iterate over
'''
# checking that the input directory exists
if not SOURCE.exists():
    sys.exit(f'Input directory {SOURCE} does not exist. Check the arguments you provided when running the script and try again!')


# saving the images that have already been converted in a variable
# we can use this to ensure that we're not converting images over and over again unnecessarily
if not DESTINATION.exists():
    
    # asking the user to create the directory
    create_directory_choice = input(f'\nThe directory "{DESTINATION}" does not exist. Would you like to create it? (Y/n) > ')
    
    if not create_directory_choice or create_directory_choice.lower().strip() == 'y':
        DESTINATION.mkdir(parents=True)
    
    else:
        sys.exit('User chose not to create a new directory. Try running the script again.')

# if the destination directory has just been created, this'll merely return an empty list
already_converted = [file.stem for file in DESTINATION.iterdir() if file.suffix == '.webp']

# now generating our list of file paths of the images to convert
images_to_convert = [image for image in SOURCE.iterdir()          # iterating through the source dir with iterdir()
                     if image.stem not in already_converted             # checking whether the image has already been converted
                     and image.suffix in ['.jpg', '.jpeg', '.png']]     # also checking whether the image is a JPG, JPEG or PNG


# in case there's nothing new to convert
if not images_to_convert:
    sys.exit('No (new) images to convert found in source directory. Exiting program.')

'''
Step 3: defining a function that'll do our converting and resizing
'''

def save_as_webp(original_image_filename:Path, destination_directory:Path=DESTINATION, resize:bool=False, width:Union[int, None]=WIDTH, height:Union[int, None]=HEIGHT):
    """Function to convert an image to webp and - optional - resizing it to a given width or height (maintaining aspect ratio).
    
    Args:
        original_image_filename (Path): The filename of the image that is being converted to webp.
        destination_directory (Path, optional): The directory where the converted images will be saved. Defaults to DESTINATION.
        resize (bool, optional): A bool telling the' function whether to resize the image. Defaults to False.
        width (Union[int, NoneType], optional): The target width of the resized image. Defaults to WIDTH.
        height (Union[int, NoneType], optional): The target height of the resized image. Defaults to HEIGHT.

    Returns:
        int: The total bytes of the converted image.
    """
    
    # opening the original image
    with Image.open(original_image_filename) as im:
        
        # generating the new filename for the converted file
        destination_filename = Path(destination_directory, f'{original_image_filename.stem}.webp')
        
        # generating the width/height of the image if the resize argument has been set to True
        if resize:
            if width:
                height = int(im.height * (width / im.width))
            else:
                width = int(im.width * (height / im.height))
        
            # checking whether the resize dimensions are smaller than the original dimensions; if so, then resize. If not, leave the image as is.
            if (width + height) < (im.width + im.height):
                im = im.resize(size=(width, height))

        # saving the image as webp
        im.save(destination_filename, format='webp')
        
        # returning the number of bytes of the converted image for the little calculation at the end ;)
        return destination_filename.stat().st_size

'''
Step 4: iterating through each image, converting to webp and resizing if necessary
'''
total_original_bytes = sum([im.stat().st_size for im in images_to_convert])
total_new_bytes = 0

print('\nConverting images...')
for image in tqdm.tqdm(images_to_convert):
    if WIDTH:
        new_bytes = save_as_webp(image, resize=True)
    elif HEIGHT:
        new_bytes = save_as_webp(image, resize=True)
    else:
        new_bytes = save_as_webp(image)
    
    total_new_bytes += new_bytes

bytes_saved = total_original_bytes - total_new_bytes
num_images_converted = len(images_to_convert)

print(
f'''
Converted {num_images_converted} images to WEBP, saving {naturalsize(bytes_saved)} - a {int((bytes_saved) * 100 / total_original_bytes)}% decrease.
'''
)


            


















# '''
# Step 3: defining a function that'll resize and convert an image
# '''
# def resize_and_convert_to_webp(im:Image.Image, filename:Path, dimensions:tuple):
#     print(dimensions)
    
#     # first checking whether the user even supplied a dimensions argument - perhaps they don't want to resize the image
#     if dimensions != (None, None):
        
#         # checking whether the dimensions supplied are actually smaller than the image
#         # if so, skip the resize stage
#         if (im.height + im.width) < (dimensions[0] + dimensions[1]):
#             pass
#         else:
#             im = im.resize(size=dimensions)
    
#     converted_im_path = Path(DESTINATION, f'{filename.stem}.webp')
#     im.save(converted_im_path, format='webp')
#     return converted_im_path.stat().st_size



# '''
# Step 4: iterating through the list of images to convert and, you guessed it, converting them!
# '''
# total_original_bytes = sum([image.stat().st_size for image in images_to_convert])
# total_new_bytes = 0

# for path in tqdm(images_to_convert):
#     with Image.open(path) as im:
#         if WIDTH or HEIGHT:
#             if WIDTH:
#                 HEIGHT = int(im.height * (WIDTH/im.width))
#             elif HEIGHT:
#                 WIDTH = int(im.width * (HEIGHT/im.height))
#     converted_image_bytes = resize_and_convert_to_webp(im, path, (WIDTH, HEIGHT))
#     total_new_bytes += converted_image_bytes

# print(
# f'''
# Converted {len(images_to_convert)} images to WEBP, saving {total_original_bytes - total_new_bytes} bytes - a {int((total_original_bytes - total_new_bytes) * 100 / total_original_bytes)}% decrease.
# '''
# )