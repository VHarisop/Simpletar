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


Simpletar is available under the GPLv3 license.
