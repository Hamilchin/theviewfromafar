import markdown as md
import os
import json

extensions = ['nl2br']
vault_dir = "/Users/alexanderchin/Library/Mobile Documents/iCloud~md~obsidian/Documents/Home"


#do DFS. takes in filenames, finds their paths, returns map file_name -> abs_path
def find_paths_from_filenames(filenames, current_dir, path_dict):

    for child in os.listdir(current_dir): 
         if os.path.isfile(os.path.join(current_dir, child)):
            if child.lower() in [name.lower() for name in filenames]:

                path = os.path.join(current_dir, child)

                if child.lower in path_dict:
                    print(f"Error, duplicate for {child.lower}: {path_dict[child.lower]} replaced for {path}")

                path_dict[child.lower()] = path                    

    dir_paths = [os.path.join(current_dir, child) for child in os.listdir(current_dir) if not os.path.isfile(os.path.join(current_dir, child))]

    for path in dir_paths:
        find_paths_from_filenames(filenames, path, path_dict)
    
    return path_dict


def make_html_links(posts): #posts being posts from post_structure
    return "".join([f'<a href="{posts[title]["page_path"]}">{posts[title]["display"]}</a> </br>' for title in posts])


def make_html_from_template(template_string, **kwargs):
    for key in kwargs:
        template_string = template_string.replace("{{" + key + "}}", kwargs[key])
    return template_string


def parse_file_structure(filename): 
    with open(os.path.join("src",filename), "r") as f:
        s = f.read()

    lines = [l.strip() for l in s.split('\n') if l.strip() != ""]

    file_structure = {}
    for line in lines:
        if line[-1] == ":":
            file_structure[line[:-1]] = {}
            current_category = line[:-1]
        else:
            post = {}
            data = [x.strip() for x in line.split("|")]
            post["display"], post["file_name"] = data[1].lower(), data[2]
            post["local_path"], post["page_path"]= None, None
            title = data[0]
            file_structure[current_category][title] = post
    return file_structure



def main():
    post_structure = parse_file_structure("files.txt")

    #data completion: find local paths
    for category in post_structure:
        posts = post_structure[category]
        filenames = [posts[title]["file_name"] for title in posts]
        path_dict = find_paths_from_filenames(filenames, vault_dir, {})
        for title in posts:
            filename = posts[title]["file_name"]
            posts[title]["local_path"] = path_dict[filename] if filename in path_dict else print(f"error: {filename} not found in vault")


    print(json.dumps(post_structure, indent=2))

    #writing post html files
    for category in post_structure:
        if category not in ["sketches"]: #auto-constructing categories (need to make html)

            os.makedirs(category, exist_ok=True)

            for title in post_structure[category]:

                page_template = open(os.path.join("src","page_template.html"), "r").read()
                local_path = post_structure[category][title]["local_path"]
                md_content = open(local_path, "r").read()
                html = make_html_from_template(page_template, title=title, content=md.markdown(md_content, extensions=extensions))
                page_path = os.path.join(category, title + ".html")
                post_structure[category][title]["page_path"] = page_path
                with open(page_path, "w") as f:
                    f.write(html)

        else: #manual categories (assume already have files)
            for title in post_structure[category]:
                filename = post_structure[category][title]["file_name"]
                post_structure[category][title]["page_path"] = os.path.join(category, filename)


    template = open(os.path.join("src", "index_template.html"), "r").read()


    index_html = make_html_from_template(template, poem_links=make_html_links(post_structure["poems"]), 
                                        sketches_links=make_html_links(post_structure["sketches"]),
                                        idea_garden_links=make_html_links(post_structure["idea-garden"]))
    with open("index.html", "w") as f:
                f.write(index_html)


main()
