import os
import os.path
import re
import subprocess
import json

directory_path = 'docs/markdown'

def replace_parameter_block(matchobj):
    data = json.loads(matchobj.group(1))
    cols, rows = data["cols"], data["rows"]
    assert all(x == "left" for x in data["align"])

    result =  "| " + " | ".join(data["data"][f"h-{i}"] for i in range(cols)) + " |"
    result += "\n"
    result += "| " + " | ".join(":---" for i in range(cols)) + " |"
    result += "\n"
    for x in range(rows):
        result += "| " + " | ".join(data["data"][f"{x}-{y}"].replace("\n", "<br>") for y in range(cols)) + " |"
        result += "\n"
    return result

def replace_admonition(matchobj):
    type_ = {
        "📘": "note",
        "👍": "success",
        "🚧": "warning",
        "❗️": "danger",
    }[matchobj[1]]

    lines = "\n".join(f"    {line[2:]}" for line in matchobj[3].splitlines())

    return f'!!! {type_} "{matchobj[2]}"\n{lines}\n'

# ======================================

subprocess.check_call(["git", "checkout", "--", "docs/markdown"])
subprocess.check_call(["git", "clean", "-df", "docs/markdown"])


# @TODO: Do slugification
# - Rename dirs/files
#   - Introduction
#mv docs/markdown/Introduction docs/markdown/introduction
#   - Getting Started
#mv "docs/markdown/Getting Started" docs/markdown/getting-started
#mv docs/markdown/getting-started/getting-started.md docs/markdown/getting-started/index.md
#mv docs/markdown/getting-started/getting-started/*.md docs/markdown/getting-started
#rm -rf docs/markdown/getting-started/getting-started
#   - Getting Help
#mv "docs/markdown/Getting Help" docs/markdown/getting-help
#mv docs/markdown/getting-help/the-pants-community.md docs/markdown/getting-help/the-pants-community/index.md
#   - Using Pants
#mv "docs/markdown/Using Pants" docs/markdown/using-pants
# ... on and on and so forth

page_by_slug = {}
for root, _, filenames in os.walk(directory_path):
    for filename in filenames:
        file_path = os.path.join(root, filename)
        with open(file_path, "r") as file:
            text = file.read()
            match = re.search(r'slug: "(.*?)"', text)
            page_by_slug[match[1]] = file_path



for root, _, filenames in os.walk(directory_path):
    for filename in filenames:
        file_path = os.path.join(root, filename)
        with open(file_path, "r") as file:
            text = file.read()

        newtext = text

        # Get rid of metadata
        newtext = re.sub(
            r'---.*?title: "(.*?)".*?(excerpt: "(.*?)")?.*?---',
            r'# \1\n\n\2\n\n---\n\n',
            newtext,
            flags=re.DOTALL
        )

        # block:image
        newtext = re.sub(
            r"\[block:image\].*?(https:.*?)\",.*?\"(.*?)\".*?\"caption\":.*?\"(.*?)\".*?\[/block\]",
            r'<figure markdown>![\2](\1 "\2")<figcaption>\3</figcaption></figure>',
            newtext,
            flags=re.DOTALL
        )

        # @TODO: block:embed

        # block:parameters
        newtext = re.sub(
            r"\[block:parameters\](.*?)\[/block\]",
            replace_parameter_block,
            newtext,
            flags=re.DOTALL
        )

        # Code snippet titles
        newtext = re.sub(
            r"```(.*) (.*)",
            r'```\1 title="\2"',
            newtext,
        )

        # Admonitions
        newtext = re.sub(
            r"> (📘|👍|🚧|❗️) (.*?)\n((>.*?\n)+)",
            replace_admonition,
            newtext,
        )

        # doc: links
        def replace_doc_link(matchobj):
            slug = matchobj[2]
            if slug.startswith("reference"):
                return f"[{matchobj[1]}](doc:{slug})"

            print(file_path)
            slug, hashsign, anchor = slug.partition("#")
            target_page = page_by_slug[slug]
            relative_path = os.path.relpath(file_path, start=os.path.dirname(target_page))
            return f"[{matchobj[1]}]({relative_path}{hashsign}{anchor})"


        newtext = re.sub(
            r"\[(.*?)\]\(doc:(.*?)\)",
            replace_doc_link,
            newtext,
        )

        if newtext != text:
            print(f"replacing: {file_path}")
            with open(file_path, "w") as file:
                file.write(newtext)

# subprocess.check_call(["npx", "prettier", "--write docs/"])
