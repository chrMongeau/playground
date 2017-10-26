import textwrap
from PIL import Image, ImageDraw, ImageFont
from xml.dom.minidom import parse
from os import path

files_source = '/sdf/arpa/af/c/chr/tmp/files.txt'
dir_to_save = '/sdf/arpa/af/c/chr/html/stst/'

margin = 4

image_height = 560
image_width = 300

size_title = 17
size_abstract = 12

width_title = 65
width_abstract = 82

colour_title = '#000000'
colour_abstract = '#0000aa'

font = "/usr/X11R7/lib/X11/fonts/TTF/Vera.ttf"

font_title = ImageFont.truetype(font, size_title, encoding='unic')
font_abstract = ImageFont.truetype(font, size_abstract, encoding='unic')







all_files = open(files_source, 'r')
file_list = all_files.readlines()
all_files.close()

# XXX file names as v%3A080%3Ab02.amf.xml won't show in browser
# (html encode issues?)
for xml_file in file_list:

    xml_file = xml_file.rstrip('\n')

    xml_doc = parse(xml_file)

    text_title_node = xml_doc.getElementsByTagName('title')
    text_abstract_node = xml_doc.getElementsByTagName('abstract')

    if len(text_title_node) > 0:
        text_title = text_title_node[0].firstChild.nodeValue
    else:
        text_title = 'No title'

    if len(text_abstract_node) > 0:
        text_abstract = text_abstract_node[0].firstChild.nodeValue
    else:
        text_abstract = 'No abstract'

    text_title_vec = textwrap.wrap(text_title, width = width_title)
    text_abstract_vec = textwrap.wrap(text_abstract, width = width_abstract)

    text_title_len = len(text_title_vec)
    text_abstract_len = len(text_abstract_vec)

    offset_title = 0
    offset_abstract = text_title_len * size_title + size_abstract

    img = Image.new("RGBA", (image_height, image_width), (255,255,255))
    draw = ImageDraw.Draw(img)

    max_lines = int(round((image_height - text_title_len * size_title) / (text_abstract_len))) + 1

    if max_lines < text_abstract_len:
        text_abstract_vec_fit = text_abstract_vec[:max_lines]
        text_abstract_vec_fit[max_lines - 1] += ' ...'
    else:
        text_abstract_vec_fit = text_abstract_vec

    for line in text_title_vec:
        draw.text((margin, offset_title), line, font = font_title, fill = colour_title)
        offset_title += font_abstract.getsize(line)[1]

    for line in text_abstract_vec_fit:
        draw.text((margin, offset_abstract), line, font = font_abstract, fill = colour_abstract)
        offset_abstract += font_abstract.getsize(line)[1]

    file_to_save = dir_to_save + path.basename(xml_file) + '.png'

    img.save(file_to_save)
