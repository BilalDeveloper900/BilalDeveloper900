import re
from pathlib import Path

README = Path(__file__).resolve().parents[1] / 'README.md'
text = README.read_text(encoding='utf-8')

# Count languages table images (look for img tags in the Languages section)
langs_section = re.search(r"<h3 align=\"left\">Languages[\s\S]*?<div", text)
if not langs_section:
    # fallback: count img tags between Languages and Tools headings
    langs_section = re.search(r"<h3 align=\"left\">Languages[\s\S]*?<h3 align=\"left\">Tools", text)

langs_text = langs_section.group(0) if langs_section else ''
langs_count = len(re.findall(r"<img[^>]+>", langs_text))

# Count tools section images between Tools heading and the next section (github-stats)
tools_section = re.search(r"<h3 align=\"left\">Tools[\s\S]*?(<p><img|$)", text)
if not tools_section:
    tools_section = re.search(r"<h3 align=\"left\">Tools[\s\S]*$", text)

tools_text = tools_section.group(0) if tools_section else ''
tools_count = len(re.findall(r"<img[^>]+>", tools_text))

total = langs_count + tools_count

new_header = f"<h3 align=\"left\">Skills: {total} ({langs_count} languages, {tools_count} tools)</h3>"

# Replace existing Skills header
new_text, n = re.subn(r"<h3 align=\"left\">Skills:[\s\S]*?<\/h3>", new_header, text, count=1)
if n == 0:
    # Insert after Fun fact line
    new_text = re.sub(r"(\- ⚡ Fun fact \*\*I like to help others\*\*)", r"\1\n\n" + new_header, text, count=1)

if new_text != text:
    README.write_text(new_text, encoding='utf-8')
    print(f"Updated README skills header: {total} total")
else:
    print("No changes needed")
