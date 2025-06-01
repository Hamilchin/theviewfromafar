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


def make_html_links(paths):
    return ".".join([f'<a href="{path}">{".".join(os.path.basename(path).split(".")[:-1])}</a> </br>' for path in paths])


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
            file_structure[line[:-1]] = []
            current_category = line[:-1]
        else:
            file_structure[current_category].append([x.strip() for x in line.split("|")])
            # (display, file_name)
    
    return file_structure



def main():
    file_structure = parse_file_structure("files.txt")

    print(json.dumps(file_structure, indent=2))

    category_page_paths = {}

    for category in file_structure:

        if category not in ["sketches"]: #auto-constructing md
            os.makedirs(category, exist_ok=True)

            
                template = open(os.path.join("src","page_template.html"), "r").read()
                md_content = open(path, "r").read()

                html = make_html_from_template(template, title=doc_name, content=md.markdown(md_content, extensions=extensions))

                page_path = os.path.join(category, doc_name + ".html")
                page_paths.append(page_path)

                with open(page_path, "w") as f:
                    f.write(html)

        else: #manual control; every file in files.txt must map to a real file
             
             category_page_paths[category] = file_structure[category]


    template = open(os.path.join("src", "index_template.html"), "r").read()
    index_html = make_html_from_template(template, poem_links=make_html_links(category_page_paths["poems"]), 
                                        sketches_links=make_html_links(category_page_paths["sketches"]),
                                        idea_garden_links=make_html_links(category_page_paths["idea-garden"]))
    with open("index.html", "w") as f:
                f.write(index_html)


main()
