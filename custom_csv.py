"""
Custom CSV parser project.

This file will contain:
- CustomCsvReader class
- CustomCsvWriter class
"""

class CustomCsvReader:
    """
    Simple CSV reader that:
    - Reads the file character by character.
    - Handles commas, quotes, and newlines.
    - Yields one row at a time as a list of strings.
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj      # opened text file
        self.delimiter = delimiter
        self.quotechar = quotechar

        # Internal buffers / state
        self._buffer = ""             # leftover text from previous reads
        self._eof = False             # did we reach end of file?

    def __iter__(self):
        # For "for row in CustomCsvReader(...)" usage. [web:54][web:58]
        return self

    def __next__(self):
        # Will return the next row (list of fields) or raise StopIteration.
        row = self._read_next_row()
        if row is None:
            raise StopIteration
        return row

    def _fill_buffer(self, chunk_size=4096):
        """
        Read a chunk of data from the file and append to internal buffer.
        """
        chunk = self.file_obj.read(chunk_size)
        if chunk == "":
            # No more data in file
            self._eof = True
        else:
            self._buffer += chunk

    def _read_next_row(self):
        """
        Parse characters until one complete CSV row is built,
        or return None if no more rows.
        """
        fields = []          # list of field strings for this row
        field_chars = []     # characters of current field
        in_quotes = False    # are we inside a quoted field? [web:46][web:49]
        i = 0                # position in buffer

        while True:
            # If buffer is empty or fully consumed, read more data
            if i >= len(self._buffer):
                if self._eof:
                    # End of file: flush last field/row if any
                    if field_chars or fields:
                        fields.append("".join(field_chars))
                        return fields
                    else:
                        return None
                self._buffer = self._buffer[i:]  # drop used part
                i = 0
                self._fill_buffer()
                continue

            ch = self._buffer[i]
            i += 1

            if in_quotes:
                if ch == self.quotechar:
                    # Could be end-of-quotes or escaped quote ("")
                    if i < len(self._buffer) and self._buffer[i] == self.quotechar:
                        # Escaped quote: add one quote to field [web:46][web:49]
                        field_chars.append(self.quotechar)
                        i += 1
                    else:
                        # Closing quote
                        in_quotes = False
                else:
                    # Any character inside quotes goes to field
                    field_chars.append(ch)
            else:
                if ch == self.quotechar:
                    # Starting quoted field
                    in_quotes = True
                elif ch == self.delimiter:
                    # End of field
                    fields.append("".join(field_chars))
                    field_chars = []
                elif ch == "\n":
                    # End of row [web:55]
                    fields.append("".join(field_chars))
                    self._buffer = self._buffer[i:]  # keep remaining for next call
                    return fields
                elif ch == "\r":
                    # Ignore bare \r (handle Windows \r\n)
                    continue
                else:
                    field_chars.append(ch)


class CustomCsvWriter:
    """
    Simple CSV writer that:
    - Takes rows as lists of strings.
    - Escapes internal quotes by doubling them.
    - Wraps fields in quotes when needed (comma, quote, or newline inside). [web:42][web:61]
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar

    def _escape_field(self, value):
        """
        Turn a single value into a CSV-safe field string. [web:60][web:68]
        """
        if value is None:
            value = ""
        else:
            value = str(value)

        needs_quotes = (
            self.delimiter in value
            or self.quotechar in value
            or "\n" in value
            or "\r" in value
        )

        # First escape any existing quotes by doubling them: " -> "" [web:63][web:68]
        if self.quotechar in value:
            value = value.replace(self.quotechar, self.quotechar * 2)

        if needs_quotes:
            return f'{self.quotechar}{value}{self.quotechar}'
        else:
            return value

    def writerow(self, row):
        """
        Write a single CSV row (list/tuple of values) to the file. [web:22][web:73]
        """
        fields = [self._escape_field(v) for v in row]
        line = self.delimiter.join(fields) + "\n"
        self.file_obj.write(line)

    def writerows(self, rows):
        """
        Write many rows (iterable of lists/tuples).
        """
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    # ---- Test writer ----
    rows = [
        ["name", "age", "comment"],
        ["Ram", 20, "hello, world"],
        ["Sita", 25, 'He said "Hi"'],
        ["Multi", 30, "line1\nline2"],
    ]

    with open("writer_sample.csv", "w", newline="") as f:
        writer = CustomCsvWriter(f)
        writer.writerows(rows)

    print("Wrote writer_sample.csv using CustomCsvWriter")

    # ---- Test reader on the file just written ----
    with open("writer_sample.csv", "r", newline="") as f:
        reader = CustomCsvReader(f)
        for row in reader:
            print(row)
