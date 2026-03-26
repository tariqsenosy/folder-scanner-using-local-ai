import re

def filter_lines(lines, keywords):
    filtered_lines = []
    keyword_pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)

    for line in lines:
        if keyword_pattern.search(line):
            filtered_lines.append(line.strip())

    return filtered_lines