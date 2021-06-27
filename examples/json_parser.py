from yarp_parser.recursive_parser import *

#json_lexemes = {'{', '}', ',', '[', ']', ':', 'true', 'false', 'null', '"'}#, '\\'}
NUMBER_REGEX = "^[0-9]+$"

class JSONParser(Parser):

    @lexemes({'{', '}', ',', '[', ']', ':', 'true', 'false', 'null', '"'})
    def parse(self):
        super().parse()
        self.value()

    @ast("value")
    def value(self):
        self.consume_whitespace()
        self.parse_alternatives([(['{'], self.json_object),
                                 (['['], self.json_array),
                                 (['"'], self.string),
                                 (['true'], self.true_val),
                                 (['false'], self.false_val),
                                 (['null'], self.null_val),
                                 ([RegularExpression(NUMBER_REGEX)], self.number)],
                                "value")
        self.consume_whitespace()

    @ast("object", require=['{'], description="object")
    def json_object(self, tokens):
        self.consume_whitespace()
        while (not self.match_pattern('}')):
            self.member()
            self.accept(',')
        self.accept('}')

    @ast("member")
    def member(self):
        self.consume_whitespace()
        self.string()
        self.consume_whitespace()
        self.accept(':')
        self.value()

    @ast("array", require=['['], description="array")
    def json_array(self, tokens):
        self.consume_whitespace()
        while (not self.match_pattern(']')):
            self.value()
            self.accept(',')
        self.accept(']')

    @lexemes({'"', '\\', RegularExpression('^[^\\\\"]*')})
    @ast("string", require=['"'], description="string")
    def string(self, tokens):
        #TODO implement escaped strings
        #TODO implement hex/unicode characters
        str_value = ""
        while (not self.match_pattern('"')):
            str_value += str(self.consume())
        self.create_append(str_value)
        self.accept('"')

    @ast("number")
    def number(self):
        #TODO implement scientific notation
        #TODO implement decimal notation
        #TODO implement signs (+, _)
        num_str = ""
        while self.match_pattern([RegularExpression(NUMBER_REGEX)]):
            t = self.consume()
            num_str += str(t)
        self.create_append(num_str)

    @ast("true", require=['true'], description="boolean")
    def true_val(self, tokens):
        pass

    @ast("false", require=['false'], description="boolean")
    def false_val(self, tokens):
        pass

    @ast("null", require=['null'], description="null")
    def null_val(self, tokens):
        pass
