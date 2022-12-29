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
wpressarc --from-tar | --to-tar [OPTIONS]
```

## Options to select conversion direction

One of the following options must be specified:

| Option               | Description                        |
|----------------------|------------------------------------|
| `-f` \| `--from-tar` | Convert from tar to wpress archive |
| `-t` \| `--to-tar`   | Convert from wpress to tar archive |


## Options for `--to-tar`

When converting from wpress to tar, the following options are also available:

| Option            | Description                                          |
|-------------------|------------------------------------------------------|
| `-m` \| `--mode`  | File mode for tar archive entries [default: `644`]   |
| `-u` \| `--uid`   | User ID for tar archive entries [default: `0`]       |
| `-g` \| `--gid`   | Group ID for tar archive entries [default: `0`]      |
| `-U` \| `--owner` | User name for tar archive entries [default: `root`]  |
| `-G` \| `--group` | Group name for tar archive entries [default: `root`] |

## Examples

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
