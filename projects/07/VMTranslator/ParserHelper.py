import re


def normalize(line: str):
    """
    S.normalize(line) -> str

    Removes from the line a comment if it exists (removes '//' and everything after it),
    removes leading and trailing whitespaces and blank lines,
    replaces arbitrary amount of whitespaces between literals and replaces them with one whitespace
    """
    return remove_arbitrary_amount_of_whitespaces(line.split('//', maxsplit=1)[0].strip())


def remove_content_of_curly_brackets(line: str) -> str:
    """
    ParserHelper.remove_content_of_curly_brackets(line) -> str

    If initial line was:
        'Hello there {your_name}! My name is {another_name}',
    the result string will be:
        'Hello there {}! My name is {}'
    """

    return re.sub(r'{[^}]*}', "{}", line)


def remove_arbitrary_amount_of_whitespaces(line: str) -> str:
    return ' '.join(line.split())


def is_comment_or_empty(line: str) -> bool:
    line = line.strip()
    return line == '' or (len(line) > 1 and line.startswith('//'))


def is_empty(line: str) -> bool:
    return line == ''
