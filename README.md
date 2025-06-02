This is a small repository for some of my writings. 

Its heavily inspired by the blogging philosophy of a friend of mine, Brennan Colberg - you can see his thoughts on what he calls the Minimum Viable Blog (here)[https://brennancolberg.com/writing/minimum-viable-blog]. It's a great read. 

This is the simplest possible blog I could dream of. It is a result of multiple failed attempts at making more complex, well styled sites that never seem to end up completed. 


Here's what's in it: 

- A file (files.txt) that contains a basic blog structure.
- A python script that contains a few build functions that scrape markdown files from my local Obsidian directory and dump them into html files.
- A few minimal "template" html files that define what posts will look like, and the homepage. 
- Some PDF files to store multi-page posts. 

Here's what's not in it: 

- Any web dev frameworks whatsoever
- Any external tools other than some basic python libraries
- CSS or formatting

Here's the basic workflow: 
- Write something in Obsidian (or the .md editor of your choice)
- Put the title, display-title (for links), and name of the markdown file (abs path not required) into files.txt.
- Run deploy.sh to build and auto-commit to remote gh-pages. 

Feel free to steal any of my code. No attribution needed. 
