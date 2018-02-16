"""General utilities are here."""
from StringIO import StringIO
import base64
import gzip


class Utility(object):
    @classmethod
    def pack_message(cls, message):
        """Gzip and base-64 encode message."""
        ram_file = StringIO()
        gz_ram_file = gzip.GzipFile(fileobj=ram_file, mode='wb')
        gz_ram_file.write(message)
        gz_ram_file.close()
        b64_gz_str = base64.b64encode(ram_file.getvalue())
        return b64_gz_str

    @classmethod
    def unpack_message(cls, b64_gz_str):
        """Base64-decode then gunzip string."""
        ram_file = StringIO(base64.b64decode(b64_gz_str))
        gz_ram_file = gzip.GzipFile(fileobj=ram_file, mode='rb')
        message = str(gz_ram_file.read())
        gz_ram_file.close()
        return message
