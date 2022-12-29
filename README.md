# wpressarc - Convert ai1wm archives to and from tar archives

## Usage:
`wpressarc --from-tar|--to-tar`

The WordPress archive format is a simple format for storing files in a directory structure. It is used by the All-in-One WP Migration plugin.

This script converts between the WordPress archive format and the tar archive format. It is intended to be used as a filter, so it reads from standard input and writes to standard output.

## Examples:

Convert a WordPress archive to a tar archive:

```
wpressarc --from-tar < wordpress.tar > wordpress.wpress
```

Convert a tar archive to a WordPress archive:

```
wpressarc --to-tar < wordpress.wpress > wordpress.tar
```

Extract a WordPress archive:

```
wpressarc --from-tar < wordpress.tar | tar -xvf -
```

To list the contents of a WordPress archive:

```
wpressarc --from-tar < wordpress.tar | tar -tvf -
```

**Note:** Converting a WordPress archive to a tar archive is lossy, because the WordPress archive format does not store file permission, ownership, and other metadata, and it also does not store any metadata for the directories (in fact, it does not even store the directory entries).

## License

This script is licensed under the MIT license. See the LICENSE file for details.
