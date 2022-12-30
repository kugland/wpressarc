# wpressarc

Convert ai1wm wpress archives to and from tar archives.

## Description

This script converts between the wpress archive format and the tar
archive format. It is intended to be used as a filter, so it reads from
standard input and writes to standard output.

The wpress archive format is a simple format for storing files in a
directory structure, used by the
[All-in-One WP Migration plugin](https://wordpress.org/plugins/all-in-one-wp-migration/).

## Usage

```
wpressarc --from-tar | --to-tar [OPTIONS] [FILE ...]
```

## Options to select conversion direction

One of the following options must be specified:

| Option               | Description                        |
|----------------------|------------------------------------|
| `-f` \| `--from-tar` | Convert from tar to wpress archive |
| `-t` \| `--to-tar`   | Convert from wpress to tar archive |


## Options for `--to-tar`

When converting from wpress to tar, the following options are also available:

| Option                    | Description                                          |
|---------------------------|------------------------------------------------------|
| `-m` \| `--mode` `MODE`   | File mode for tar archive entries [default: `644`]   |
| `-u` \| `--uid` `UID`     | User ID for tar archive entries [default: `0`]       |
| `-g` \| `--gid` `GID`     | Group ID for tar archive entries [default: `0`]      |
| `-U` \| `--owner` `OWNER` | User name for tar archive entries [default: `root`]  |
| `-G` \| `--group` `GROUP` | Group name for tar archive entries [default: `root`] |

## Examples

For example, to convert a tar archive to a wpress archive:

    wpressarc --from-tar < wordpress.tar > wordpress.wpress

To convert a wpress archive to a tar archive:

    wpressarc --to-tar < wordpress.wpress > wordpress.tar

To extract a wpress archive:

    wpressarc --to-tar < wordpress.wpress | tar -xvf -

To list the contents of a wpress archive:

    wpressarc --to-tar < wordpress.wpress | tar -tvf -

To extract only files matching a pattern from an archive (wpress or tar):

    wpressarc --to-tar '*.sql' < wordpress.wpress | tar -xvf -

## Notes

Converting a wpress archive to a tar archive is lossy, because the
wpress archive format does not store file permission, ownership,
and other metadata, and it also does not store any metadata for the
directories (in fact, it does not even store the directory entries).

When the `FILE` arguments are specified, they are interpreted as
patterns to match against the file names in the archive. If stdin
is seekable, *i.e.* if it is redirected directly from a file, then
the unmatched entries will be skipped entirely, which will be much
faster than reading and discarding the entries.

## License

This script is licensed under the MIT license. See the
[LICENSE](./LICENSE) file for details.
