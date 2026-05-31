import markdown as md
import os
import time
import fire
import re
import html as html_lib


extensions = ['nl2br', 'tables', 'fenced_code', 'footnotes']
vault_dir = "/Users/alexanderchin/non-icloud/obsidian-vaults/Home"
links_dir = "links"

# LaTeX math ($...$ inline, $$...$$ display) is pulled out before markdown runs
# (so markdown can't mangle subscripts/asterisks), then restored afterwards as
# MathJax-native \(...\) / \[...\] delimiters for client-side rendering.
math_store = {}
MATH_DISPLAY_RE = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
MATH_INLINE_RE = re.compile(r'(?<![\\$])\$(?!\s)(.+?)(?<![\s\\])\$(?!\$)')
# Fenced ```...``` and inline `...` code, so $ inside code isn't treated as math.
CODE_RE = re.compile(r'(```.*?```|`[^`\n]*`)', re.DOTALL)

# {{name}}        -> inject the rendered content of vault file <name>.md inline
# [[name|display]] -> link to a built page links/<name>.html, building it recursively
OPERATOR_RE = re.compile(
    r'\{\{\s*(?P<inject>[^}]+?)\s*\}\}'
    r'|\[\[(?P<file>[^|\]]+)\|(?P<display>.+?)\]\]'
)


def clean(root_dir="."):

    has_template = False

    for root, dirs, files in os.walk(root_dir):
        if "src" in root.split(os.sep):
            continue
        if any(not f.endswith(".html") for f in files):
            continue
        for name in files:
            if name.endswith(".html") and "template" in name.lower():
                print(f"Found template file: {os.path.join(root, name)}")
                has_template = True

    if has_template:
        response = input("Some .html files contain 'template'. Continue anyway? [y/n]: ").strip().lower()
        if response not in ("y", "yes"):
            print("Aborting.")
            exit(1)

    for root, dirs, files in os.walk(root_dir):
        if "src" in root.split(os.sep):
            continue
        if any(not f.endswith(".html") for f in files):
            continue
        for name in files:
            if name.endswith(".html"):
                os.remove(os.path.join(root, name))

    # Remove empty directories
    for root, dirs, _ in os.walk(root_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Remove .html files in the current dir
    for f in os.listdir():
        if f.endswith(".html"):
            os.remove(f)


# DFS the vault for a file named `filename` (case-insensitive); return its path
def find_path_from_filename(filename, current_dir):
    for child in os.listdir(current_dir):
        child_path = os.path.join(current_dir, child)
        if os.path.isfile(child_path):
            if child.lower() == filename.lower():
                return child_path
        elif os.path.isdir(child_path):
            result = find_path_from_filename(filename, child_path)
            if result is not None:
                return result
    return None


# Replace each math span with an inert placeholder token (markdown leaves it
# alone); the original is kept in math_store keyed by the token.
def protect_math(text):
    def stash(kind):
        def repl(match):
            token = f"MATHJAXSPAN{len(math_store)}END"
            math_store[token] = (kind, match.group(1))
            return token
        return repl

    def protect_span(span):
        span = MATH_DISPLAY_RE.sub(stash("display"), span)
        span = MATH_INLINE_RE.sub(stash("inline"), span)
        return span

    # CODE_RE.split keeps code spans at odd indices; only touch the gaps.
    parts = CODE_RE.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = protect_span(parts[i])
    return "".join(parts)


# Swap placeholder tokens back into final HTML as escaped MathJax delimiters.
def restore_math(html):
    for token, (kind, body) in math_store.items():
        if token not in html:
            continue
        body = html_lib.escape(body, quote=False)
        wrapped = f"\\[{body}\\]" if kind == "display" else f"\\({body}\\)"
        html = html.replace(token, wrapped)
    return html


# Resolve <name>.md in the vault, strip %%obsidian comments%%, render to HTML
def render_markdown(name):
    local_path = find_path_from_filename(name + ".md", vault_dir)
    if local_path is None:
        print(f"File {name}.md not found in vault")
        return None
    with open(local_path, "r") as f:
        raw_text = f.read()
    md_content = re.sub(r'%%.*?%%', '', raw_text, flags=re.DOTALL)
    md_content = protect_math(md_content)
    return md.markdown(md_content, extensions=extensions)


def fill_template(template_string, **kwargs):
    for key, value in kwargs.items():
        template_string = template_string.replace("{" + key + "}", value)
    return template_string


# Expand {{injections}} and [[links]] in already-rendered HTML.
# page_dir: directory of the host page, used for relative link hrefs.
# built:    names already written to links/ (shared across the whole build).
# stack:    names currently being injected, to break injection cycles.
def process(html, page_dir, built, stack):

    def expand(match):
        name = match.group("inject")
        if name is not None:
            return inject(name, page_dir, built, stack)

        filename = match.group("file")
        display = match.group("display")
        build_page(filename, built)
        if page_dir == links_dir:
            href = filename + ".html"
        else:
            href = os.path.relpath(os.path.join(links_dir, filename + ".html"), page_dir)
        return f'<a href="{href}">{display}</a>'

    return OPERATOR_RE.sub(expand, html)


# Inline the rendered content of <name>.md (no link, no separate page).
def inject(name, page_dir, built, stack):
    if name in stack:
        print(f"Injection cycle on {name}, skipping")
        return ""
    rendered = render_markdown(name)
    if rendered is None:
        return ""
    return process(rendered, page_dir, built, stack | {name})


# Build links/<name>.html (once), expanding operators in its content.
def build_page(name, built):
    if name in built:
        return
    built.add(name)
    rendered = render_markdown(name)
    if rendered is None:
        return
    content = process(rendered, links_dir, built, {name})
    template = open(os.path.join("src", "page_template.html"), "r").read()
    html = fill_template(template, title=name, content=content)
    html = restore_math(html)
    os.makedirs(links_dir, exist_ok=True)
    with open(os.path.join(links_dir, name + ".html"), "w") as f:
        f.write(html)


def main():
    math_store.clear()
    built = set()
    template = open(os.path.join("src", "index_template.html"), "r").read()
    index_html = process(template, ".", built, set())
    index_html = restore_math(index_html)
    with open("index.html", "w") as f:
        f.write(index_html)


def watch():
    secs = 0
    clean()
    while True:
        try:
            print(f"rebuilt, active for {secs} secs")
            main()
            time.sleep(2)
            secs += 2
        except Exception as e:
            with open("index.html", "w") as f:
                f.write(str(e))
            raise


if __name__ == "__main__":
    fire.Fire(lambda command="build": {
        "build": main,
        "clean": clean,
        "watch": watch
    }[command]())
