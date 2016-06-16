Simpletar
=========

Simpletar is a simple command-line wrapper around the UNIX 'tar' tool. It includes
options for creating and extracting tar, xz, bzip2 and gzip files, as well as
for listing archive contents and updating/deleting uncompressed archives.

----

Simpletar includes 2 files: 

- `lib.py` contains the wrapper functions used in simpletar
as well as a utility for determining a set of commonly used file extensions
for each archive type available in simpletar.

- `simpletar` is the main script that uses the name of the archive file and/or
  its header's "magic bytes" to try and determine the used compression type,
  if any.


## Examples
Create a new .gzip archive file from files `A, B, C`:

```shell
$ simpletar -c archive.tar.gz -f A B C
```

List the contents of that archive file:

```shell
$ simpletar -l archive.tar.gz
A
B
C
```

Now extract it:

```shell
$ simpletar -x archive.tar.gz
```

For plain `.tar` archives, you can also use the `update` or `delete` commands,
which are pretty self-explanatory. 

`delete` removes a file from the archive:

```shell
$ simpletar -c archive.tar -f A B C
$ simpletar -l archive.tar
A
B
C
$ simpletar -d archive.tar -f B
$ simpletar -l archive.tar
A
C
```

`update` appends a set of files if their editions are newer than the copies
already existing in the archive (if any).

```shell
$ simpletar -c archive.tar -f A B C
$ simpletar -u archive.tar -f A
$ simpletar -l archive.tar
A
B
C
$ touch A
$ simpletar -u archive.tar -f A
$ simpletar -l archive.tar
A
B
C
A
```

# License
Simpletar is available under the GPLv3 license.
