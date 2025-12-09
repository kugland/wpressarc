#!/bin/bash

set -eux

python3 ./test.py

tar -C test_assets --mtime=1980-01-01T00:00:00Z -c ./{database.sql,package.json,uploads/test.jpg} | ./wpressarc -f > test.wpress
sha256="$(sha256sum test.wpress | cut -d' ' -f1)"
test "$sha256" = "dc4f6551d51f47a78998bb44bf2d69235ab36bdb60085f6110d89e1cb059c670"

files="$(./wpressarc -t < test.wpress | tar -t | sort | xargs echo)"
test "$files" = "database.sql package.json uploads/ uploads/test.jpg"

files="$(./wpressarc -t '*.sql' '*.json' < test.wpress | tar -t | sort | xargs echo)"
test "$files" = "database.sql package.json"

# shellcheck disable=SC2002
files="$(cat test.wpress | ./wpressarc -t '*.sql' '*.json' | tar -t | sort | xargs echo)"
test "$files" = "database.sql package.json"

./wpressarc -t --mode=000 '*.sql' < test.wpress | tar -tv | grep -F -- "----------"
./wpressarc -t --dmode=000 < test.wpress | tar -tv | grep -F -- "d---------"
./wpressarc -t --owner=owner --group=group '*.sql' < test.wpress | tar -tv | grep -F -- "owner/group"
./wpressarc -t --uid=1234 --gid=5678 '*.sql' < test.wpress | tar -tv --numeric-owner | grep -F -- "1234/5678"

./wpressarc -t < test.wpress | ./wpressarc -f > test2.wpress
cmp test.wpress test2.wpress

rm test.wpress test2.wpress

echo 'Everything looks OK !!!'
