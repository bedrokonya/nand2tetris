
class ParserHelper:
    @staticmethod
    def normalize_line(line):
        return ParserHelper.remove_arbitrary_amount_of_whitespaces(line.split('//', maxsplit=1)[0].strip())

    @staticmethod
    def remove_arbitrary_amount_of_whitespaces(line):
        return ' '.join(line.split())

    @staticmethod
    def is_comment_or_empty(line):
        line = line.strip()
        return line == '' or (len(line) > 1 and line[0] == '/' and line[1] == '/')