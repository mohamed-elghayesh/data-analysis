#!/usr/bin/python3
from bs4 import BeautifulSoup
import os, shutil, sys

def create_copy(jupyter_slides_name):
    """ input: file name (located in the same directory).
        process: copy file to new path.
        return: string (copied file new path).
    """
    cwd = os.getcwd()
    name = jupyter_slides_name
    new_path = cwd + '/toggle_enabled_' + name
    # copies the file to a new file
    if(os.path.isfile('./' + name)):
        shutil.copy(name, new_path)
    else:
        print('file not found, check the file name.')
    return new_path

def enable_input_toggle(jupyter_slides_path):
    """Embeds javascript to enable input cells show/hide toggling and saves the copy.
    Note: the jupyter slides and the script should be in the same folder.
    TODO1: check if its a jupyter slides html file before proceeding.
    TODO2: check major and minor versions to decide class names (if changed)"""

    html = open(jupyter_slides_path, 'r')
    soup = BeautifulSoup(html, features="lxml")
    input_toggle_script = soup.new_tag('script')

    # jquery or javascript code to be used
    input_toggle_script.string = """$(document).ready(function(){
      $('.jp-RenderedText[data-mime-type="application/vnd.jupyter.stderr"]').hide();
      $('.jp-CodeMirrorEditor jp-Editor jp-InputArea-editor').hide()
      $(".jp-Cell-outputWrapper").click(function(){
        $(this).closest("div").prev().toggle(500);
      });
      $(".jp-Cell-outputWrapper").click(); //start hidden by toggling once
    });
    """

    # soup insert the script last before head close
    soup.head.insert(len(soup.head.contents), input_toggle_script)
    html.close()

    # write to file and close
    html = open(jupyter_slides_path,'w')
    html.write(str(soup))
    html.close()
    print('jupyter "input toggle" script inserted.')

# Enables toggle to jupyter slides file copy
# validate argument existance
if (len(sys.argv) > 1 and sys.argv[1].strip() != ""):
    copied_file_path = create_copy(sys.argv[1])
    enable_input_toggle(copied_file_path)
else:
    print('Please add <jupyter-slides.html> file name.')
