from __future__ import annotations

import unittest
import hashlib
import argparse
import tarfile
import io
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

spec = spec_from_loader("wpressarc", SourceFileLoader("wpressarc", "./wpressarc"))
if spec is None:
    raise ImportError("Unable to load wpressarc")
wpressarc = module_from_spec(spec)
if spec.loader is None:
    raise ImportError("Unable to load wpressarc")
spec.loader.exec_module(wpressarc)

EntryHeader = wpressarc.EntryHeader
Archive = wpressarc.Archive


class TestEntryHeader(unittest.TestCase):
    def test_write_read(self):
        """Test writing and reading a header."""
        header = EntryHeader("path", "name", 123, 456)
        buf = io.BytesIO()
        header.write_header(buf)
        buf.seek(0)
        sha256 = hashlib.sha256()
        sha256.update(buf.read())
        self.assertEqual(
            sha256.hexdigest(),
            "a2f29ff31bc22f8ab56c032dda5f5dbac253929ab903cfddd5e632861a59a15e",
        )
        buf.seek(0)
        header2 = EntryHeader.read_header(buf)
        self.assertIsNotNone(header2)
        if header2 is not None:
            self.assertEqual(header.path, header2.path)
            self.assertEqual(header.name, header2.name)
            self.assertEqual(header.size, header2.size)
            self.assertEqual(header.mtime, header2.mtime)

    def test_write_read_empty(self):
        """Test writing and reading an empty header."""
        buf = io.BytesIO()
        buf.write(b"\0" * (255 + 14 + 12 + 4096))
        buf.seek(0)
        header2 = EntryHeader.read_header(buf)
        self.assertIsNone(header2)

    def test_from_tarinfo(self):
        """Test converting a TarInfo object to a header."""
        tarinfo = tarfile.TarInfo()
        tarinfo.name = "path/name"
        tarinfo.size = 123
        tarinfo.mtime = 456
        tarinfo.type = tarfile.REGTYPE
        header = EntryHeader.from_tarinfo(tarinfo)
        self.assertIsNotNone(header)
        if header is not None:
            self.assertEqual(header.path, "path")
            self.assertEqual(header.name, "name")
            self.assertEqual(header.size, 123)
            self.assertEqual(header.mtime, 456)

    def test_from_tarinfo_dotdir(self):
        """Test converting a TarInfo object to a header."""
        tarinfo = tarfile.TarInfo()
        tarinfo.name = "name"
        tarinfo.size = 123
        tarinfo.mtime = 456
        tarinfo.type = tarfile.REGTYPE
        header = EntryHeader.from_tarinfo(tarinfo)
        self.assertIsNotNone(header)
        if header is not None:
            self.assertEqual(header.path, ".")
            self.assertEqual(header.name, "name")
            self.assertEqual(header.size, 123)
            self.assertEqual(header.mtime, 456)

    def test_from_tarinfo_dir(self):
        """Test converting a TarInfo object to a header."""
        tarinfo = tarfile.TarInfo()
        tarinfo.name = "path/name"
        tarinfo.size = 123
        tarinfo.mtime = 456
        tarinfo.type = tarfile.DIRTYPE
        header = EntryHeader.from_tarinfo(tarinfo)
        self.assertIsNone(header)

    def test_to_tarinfo(self):
        """Test converting a header to a TarInfo object."""
        header = EntryHeader("path", "name", 123, 456)
        tarinfo = header.to_tarinfo(
            argparse.Namespace(
                mode=0o755, uid=234, gid=567, owner="owner", group="group"
            )
        )
        self.assertEqual(tarinfo.name, "path/name")
        self.assertEqual(tarinfo.size, 123)
        self.assertEqual(tarinfo.mtime, 456)
        self.assertEqual(tarinfo.type, tarfile.REGTYPE)
        self.assertEqual(tarinfo.mode, 0o755)
        self.assertEqual(tarinfo.uid, 234)
        self.assertEqual(tarinfo.gid, 567)
        self.assertEqual(tarinfo.uname, "owner")
        self.assertEqual(tarinfo.gname, "group")


class TestArchive(unittest.TestCase):
    def test_read_write(self):
        """Test reading a WordPress archive."""
        file = io.BytesIO()
        archive = Archive(file)
        entry = EntryHeader("path", "name", 7, 456)
        archive.write(entry, io.BytesIO(b"content"))
        archive.finalize()
        archive.file.seek(0)
        entry2 = archive.next_entry()
        self.assertIsNotNone(entry2)
        if entry2 is not None:
            self.assertEqual(entry.path, entry2.path)
            self.assertEqual(entry.name, entry2.name)
            self.assertEqual(entry.size, entry2.size)
            self.assertEqual(entry.mtime, entry2.mtime)
            buf = archive.file.read(entry2.size)
            self.assertEqual(buf, b"content")
        entry2 = archive.next_entry()
        self.assertIsNone(entry2)


if __name__ == "__main__":
    unittest.main()
