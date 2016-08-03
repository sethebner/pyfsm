import re
import sys


class Tokenizer(object):
    def __init__(self):
        self.start_node_name = 'START'
        self.delimiters = '->', '::', '{', '}'
        self.regex_pattern = '|'.join(map(re.escape, self.delimiters))

    def strip_list(self, l):
        return list(map(str.strip, l))

    def tokenize(self, spec_file_name):
        lines = []
        tokens = []
        with open(spec_file_name, 'r') as f:
            lines = f.readlines()
            lines = self.strip_list(lines)

        for line in lines:
            line_tokens = re.split(self.regex_pattern, line)
            line_tokens = self.strip_list(line_tokens)
            line_tokens = list(filter(None, line_tokens))
            tokens.append(line_tokens)
        tokens = list(filter(None, tokens)) # remove empty strings from list

        return tokens

def main():
    t = Tokenizer()
    if len(sys.argv) < 2:
        sys.exit()
    tokens = t.tokenize(sys.argv[1])
    print(tokens)
    
if __name__ == '__main__':
    main()
