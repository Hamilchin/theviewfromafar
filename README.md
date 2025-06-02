This is a small repository for some of my writings. 

Its heavily inspired by the blogging philosophy of a friend of mine, Brennan Colberg - you can see his thoughts on what he calls the Minimum Viable Blog [here](https://brennancolberg.com/writing/minimum-viable-blog). It's a great read. 

This is the simplest possible blog I could dream of. It is a result of multiple failed attempts at making more complex, well styled sites that never seemed to end up completed. 


Here's what's in it: 

- A file (files.txt) that contains a basic blog structure.
- A few minimal "template" html files that define what the homepage and generic posts will look like.
- A python script that contains a few build functions that scrape markdown from my local Obsidian directory and dump it into html files using the templates.
- Some PDF files, manually exported and stored via Obsidian, to store multi-page posts. 

Here's what's not in it: 

- Any web dev frameworks whatsoever
- Any external tools other than some basic python libraries
- CSS or formatting

Here's the basic workflow:
- Write something in Obsidian (or the .md editor of your choice)
- Put the title, display-title (for links), and name of the markdown file (abs path not required) into files.txt.
- Run src/deploy.sh from the project root to build and auto-commit to remote gh-pages. 

Feel free to steal any of my code. No attribution needed. 
