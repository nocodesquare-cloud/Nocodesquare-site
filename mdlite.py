"""A small Markdown-to-HTML converter for blog posts written in the admin dashboard.

Standard library only, so the Cloudflare build needs no extra packages. It covers what the
admin editor produces: headings, paragraphs, bullet and numbered lists, quotes, images,
bold, italic, links, inline code and line breaks. Lines that start with an HTML tag pass through.
"""
import html, re

_TAG_START = re.compile(r'^\s*</?[a-zA-Z][^>]*>')


def _escape(text):
    # Escape &, < and > unless they are already part of an entity or a real tag
    text = re.sub(r'&(?!#?\w+;)', '&amp;', text)
    text = re.sub(r'<(?![a-zA-Z/!])', '&lt;', text)
    return text


def _inline(text):
    codes = []
    def keep_code(m):
        codes.append('<code>' + html.escape(m.group(1)) + '</code>')
        return f'\x00{len(codes) - 1}\x00'
    text = re.sub(r'`([^`]+)`', keep_code, text)
    text = _escape(text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)',
                  lambda m: f'<img src="{m.group(2)}" alt="{html.escape(m.group(1))}" loading="lazy">', text)
    def link(m):
        label, href = m.group(1), m.group(2)
        ext = href.startswith('http') and 'nocodesquare.com' not in href
        return f'<a href="{href}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', link, text)
    text = re.sub(r'(\*\*|__)(.+?)\1', r'<b>\2</b>', text)
    text = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'  \n|\\\n', '<br>\n', text)
    return re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m.group(1))], text)


def to_html(md):
    lines = md.replace('\r\n', '\n').split('\n')
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append('<p>' + _inline('\n'.join(para)) + '</p>')
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            flush()
            level = max(2, len(m.group(1)))   # the page title is the only h1
            out.append(f'<h{level}>{_inline(m.group(2).strip())}</h{level}>')
            i += 1; continue
        if re.match(r'^(\*\s*){3,}$|^(-\s*){3,}$', s):
            flush(); out.append('<hr>'); i += 1; continue
        if s.startswith('>'):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append('<blockquote>' + to_html('\n'.join(quote)) + '</blockquote>')
            continue
        lm = re.match(r'^([-*+]|\d+[.)])\s+(.*)$', s)
        if lm:
            flush()
            ordered = lm.group(1)[0].isdigit()
            items = []
            while i < len(lines):
                cur = lines[i].strip()
                im = re.match(r'^([-*+]|\d+[.)])\s+(.*)$', cur)
                if im and im.group(1)[0].isdigit() == ordered:
                    items.append(im.group(2)); i += 1
                elif cur and items and not im and lines[i].startswith((' ', '\t')):
                    items[-1] += ' ' + cur; i += 1   # continuation of the last item
                else:
                    break
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{_inline(t)}</li>' for t in items) + f'</{tag}>')
            continue
        if _TAG_START.match(line) and not para:
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i]); i += 1
            out.append('\n'.join(block))
            continue
        para.append(s); i += 1
    flush()
    return '\n'.join(out)


if __name__ == '__main__':
    sample = "## Hello\n\nSome **bold**, *italic*, `code` & a [link](https://n8n.io).\n\n- one\n- two\n\n1. first\n2. second\n\n> a quote\n\n![Alt](img/blog/x.jpg)"
    print(to_html(sample))
