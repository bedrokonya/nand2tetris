import re


class ParserHelper:
    @staticmethod
    def normalize(line: str):
        """
        S.normalize(line) -> str

        Removes from the line a comment if it exists (removes '//' and everything after it),
        removes leading and trailing whitespaces and blank lines,
        replaces arbitrary amount of whitespaces between literals and replaces them with one whitespace
        """
        return ParserHelper.remove_arbitrary_amount_of_whitespaces(line.split('//', maxsplit=1)[0].strip())

    @staticmethod
    def remove_arbitrary_amount_of_whitespaces(line: str):
        return ' '.join(line.split())

    @staticmethod
    def is_comment_or_empty(line: str) -> bool:
        line = line.strip()
        return line == '' or (len(line) > 1 and line[0] == '/' and line[1] == '/')

    @staticmethod
    def remove_content_of_curly_brackets(line: str) -> str:
        """
        ParserHelper.remove_content_of_curly_brackets(line) -> str

        If initial line was:
            'Hello there {your_name}! My name is {amother_name}',
        the result string will be:
            'Hello there {}! My name is {}'
        """

        return re.sub(r'{[^}]*}', "{}", line)
