from enum import Enum, unique


@unique
class State(Enum):
    initial = 0
    array = 1
    row = 2
    string = 3
    quoted_string = 4


@unique
class Token(Enum):
    new_row = 1


class PostgresArrayLexer(object):
    def __init__(self, source):
        self._state = State.initial
        self._source = source
        self._source_len = len(source)
        self._begin_ind = 0
        self._end_ind = 0

    def to_state(self, state):
        self._state = state

    def begin_with(self, val):
        if self._source[self._end_ind:].startswith(val):
            self.advance(len(val))
            return True
        return False

    def advance(self, pos=1):
        self._end_ind += pos

    def have_more(self):
        return self._end_ind < self._source_len

    def discard_token(self):
        self._begin_ind = self._end_ind

    @property
    def token(self):
        return self._source[self._begin_ind: self._end_ind]

    def error(self):  # pragma: no cover
        return Exception(
            '%s: Encountered unanticipated chars %s (whole string was "%s")' % (
                self._state, self._source[self._begin_ind: self._end_ind + 1], self._source
            )
        )

    def cleaned_string(self, raw_str):
        while r'\\' in raw_str:
            raw_str = raw_str.replace(r'\\', '\\')
        raw_str = raw_str.replace(r'\"', '"').replace('""', '"').strip('"')
        return unicode(raw_str, 'utf8')

    def swallow(self):
        while self.have_more():
            if self._state == State.initial:
                if self.begin_with('{'):
                    self.discard_token()
                    self.to_state(State.array)
                else:  # pragma: no cover
                    raise self.error()
            elif self._state == State.array:
                if self.begin_with('"('):
                    self.discard_token()
                    yield Token.new_row
                    self.to_state(State.row)
                elif self.begin_with(','):
                    self.discard_token()
                elif self.begin_with('}'):
                    self.discard_token()
                    self.to_state(State.initial)
                else:  # pragma: no cover
                    raise self.error()
            elif self._state == State.row:
                if self.begin_with(','):
                    yield None
                    self.discard_token()
                elif self.begin_with('\\"'):
                    self.to_state(State.quoted_string)
                elif self.begin_with(')"'):
                    yield None
                    self.discard_token()
                    self.to_state(State.array)
                else:
                    self.advance()
                    self.to_state(State.string)
            elif self._state == State.string:
                if self.begin_with(','):
                    yield unicode(self.token[:-1], 'utf8')
                    self.discard_token()
                    self.to_state(State.row)
                elif self.begin_with(')"'):
                    yield unicode(self.token[:-2], 'utf8')
                    self.discard_token()
                    self.to_state(State.array)
                else:
                    self.advance()
            elif self._state == State.quoted_string:
                if self.begin_with('\\\\\\\\\\"\\"'):
                    pass
                if self.begin_with('\\"\\"'):
                    pass
                elif self.begin_with('\\",'):
                    yield self.cleaned_string(self.token[:-1])
                    self.discard_token()
                    self.to_state(State.row)
                elif self.begin_with('\\")"'):
                    yield self.cleaned_string(self.token[:-2])
                    self.discard_token()
                    self.to_state(State.array)
                else:
                    self.advance()


def parse_postgres_row_array(array):
    result = []
    row = []
    for val in PostgresArrayLexer(array).swallow():
        if val == Token.new_row:
            if len([val for val in row if val is not None]) > 0:
                result.append(tuple(row))
            row = []
        else:
            row.append(val)
    if len([val for val in row if val is not None]) > 0:
        result.append(tuple(row))
    return result
