This is a small repository for some of my writings. It is currently hosted at https://hamilchin.github.io/theviewfromafar. 

It's heavily inspired by the blogging philosophy of a friend of mine, Brennan Colberg - you can see his thoughts on what he calls the Minimum Viable Blog [here](https://brennancolberg.com/writing/minimum-viable-blog). I highly recommend. 

This is the simplest possible blog I could dream of. It is a result of multiple failed attempts at making more complex, well styled sites that never seemed to end up completed. 


Here's what's in it: 

- A couple of minimal "template" html files that define what the homepage and generic posts will look like.
- A python script that contains a few build functions that scrape markdown from my local Obsidian directory and dump it into html files using the templates.

Everything is driven by two operators, which can appear in any markdown file or in the html templates:

- `[[name|display]]` — renders an `<a>` linking to `links/name.html`, and recursively builds that page from the vault file `name.md`.
- `{{name}}` — injects the rendered content of the vault file `name.md` inline (no link, no separate page), recursively expanding any operators inside it.

The homepage structure lives in a vault markdown file (written with `[[...]]` links), injected into `index_template.html` via `{{TVFA Home}}`. There is no manifest file — a page is built only if it's reachable by `[[...]]` from the index.

Markdown niceties that are supported: Obsidian-style footnotes (`[^1]` ... `[^1]: text`) render as linkable superscripts with a footnote section, and LaTeX math (`$inline$` / `$$display$$`) renders via MathJax (math is protected from markdown and `$` inside code is left alone).

Here's what's not in it: 

- Any web dev frameworks whatsoever
- Any external tools other than some basic python libraries
- CSS or formatting

Here's the basic workflow:
- Write something in Obsidian (or the .md editor of your choice)
- Reference it from `home.md` (or any already-linked page) with `[[filename|display text]]`
- Run src/deploy.sh from the project root to build and auto-commit to remote gh-pages. 

Feel free to steal any of my code. No attribution needed. 
