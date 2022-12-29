# wpressarc

Convert ai1wm wpress archives to and from tar archives.

## Usage

```
wpressarc --from-tar|--to-tar
```

## Description

The wpress archive format is a simple format for storing files in a
directory structure, used by the
[All-in-One WP Migration plugin](https://wordpress.org/plugins/all-in-one-wp-migration/).

This script converts between the wpress archive format and the tar
archive format. It is intended to be used as a filter, so it reads from
standard input and writes to standard output.

## Examples

For example, to convert a wpress archive to a tar archive:

For example, to convert a tar archive to a wpress archive:

    wpressarc --from-tar < wordpress.tar > wordpress.wpress

To convert a wpress archive to a tar archive:

    wpressarc --to-tar < wordpress.wpress > wordpress.tar

To extract a wpress archive:

    wpressarc --to-tar < wordpress.wpress | tar -xvf -

To list the contents of a wpress archive:

    wpressarc --to-tar < wordpress.wpress | tar -tvf -

## Notes

Converting a wpress archive to a tar archive is lossy, because the
wpress archive format does not store file permission, ownership,
and other metadata, and it also does not store any metadata for the
directories (in fact, it does not even store the directory entries).

## License

This script is licensed under the MIT license. See the LICENSE file
for details.
