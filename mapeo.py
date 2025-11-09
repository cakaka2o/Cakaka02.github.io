#!/usr/bin/env python3
"""mapeo.py - Emojíaco translator (improved)
Features:
- Optional slash separators (words: '/', lines: '//')
- Uppercase marker: '👀'
"""
import json, argparse
from pathlib import Path
HERE = Path(__file__).parent
with open(HERE / 'mapping.json','r',encoding='utf-8') as f:
    data = json.load(f)
MAPPING = data['mapping']
U = data.get('upper_marker','👀')
REVERSE = {v:k for k,v in MAPPING.items()}
TOKENS = sorted(REVERSE.keys(), key=len, reverse=True)
TOKENS_UP = [t+U for t in TOKENS]

def text_to_emoji(text, include_n=True, use_slash=False, keep_unknown=True):
    lines = text.split('\n')
    out_lines = []
    for ln in lines:
        words = ln.split()
        em_words = []
        for w in words:
            em = ''
            for ch in w:
                if ch.lower()=='ñ' and not include_n:
                    ch = 'n'
                k = ch.lower()
                if k in MAPPING:
                    token = MAPPING[k]
                    em += token + (U if ch.isupper() else '')
                else:
                    if keep_unknown:
                        em += ch
            em_words.append(em)
        out_lines.append(' / '.join(em_words) if use_slash else ' '.join(em_words))
    return ' // '.join(out_lines) if use_slash else '\n'.join(out_lines)

def emoji_to_text(emoji_text, include_n=True, use_slash=False, keep_unknown=True):
    i=0; L=len(emoji_text); out_chars=[]
    while i < L:
        # newline separators
        if emoji_text.startswith(' // ', i):
            out_chars.append('\n'); i += 4; continue
        if emoji_text.startswith('//', i):
            out_chars.append('\n'); i += 2; continue
        # single word separators
        if emoji_text.startswith(' / ', i):
            out_chars.append(' '); i += 3; continue
        if emoji_text.startswith('/', i):
            out_chars.append(' '); i += 1; continue
        matched=False
        for token in TOKENS_UP:
            if emoji_text.startswith(token, i):
                base = token[:-len(U)]
                ch = REVERSE.get(base, None)
                if ch is not None:
                    out_chars.append(ch.upper())
                else:
                    if keep_unknown: out_chars.append(token)
                i += len(token); matched=True; break
        if matched: continue
        for token in TOKENS:
            if emoji_text.startswith(token, i):
                ch = REVERSE.get(token, None)
                if ch is not None:
                    out_chars.append(ch)
                else:
                    if keep_unknown: out_chars.append(token)
                i += len(token); matched=True; break
        if matched: continue
        out_chars.append(emoji_text[i]); i += 1
    result = ''.join(out_chars)
    if not include_n:
        result = result.replace('ñ','n').replace('Ñ','N')
    return result

def main():
    parser = argparse.ArgumentParser(description='Emojíaco mapeo (improved)')
    sub = parser.add_subparsers(dest='cmd', required=True)
    p1 = sub.add_parser('to-emoji')
    p1.add_argument('text', help='Text to convert')
    p1.add_argument('--no-ñ', dest='include_n', action='store_false', help='Map ñ to n')
    p1.add_argument('--slashes', dest='use_slash', action='store_true', help='Use slash separators (words: /, lines: //)')
    p1.set_defaults(include_n=True, use_slash=False)
    p2 = sub.add_parser('to-text')
    p2.add_argument('emoji', help='Emoji text to convert')
    p2.add_argument('--no-ñ', dest='include_n', action='store_false', help='Map ñ to n')
    p2.add_argument('--slashes', dest='use_slash', action='store_true', help='Treat / as space and // as newline')
    p2.set_defaults(include_n=True, use_slash=False)
    args = parser.parse_args()
    if args.cmd == 'to-emoji':
        print(text_to_emoji(args.text, include_n=args.include_n, use_slash=args.use_slash))
    else:
        print(emoji_to_text(args.emoji, include_n=args.include_n, use_slash=args.use_slash))

if __name__=='__main__':
    main()
