# Rocketsled — Immutable cloud files

[![Build Status](https://travis-ci.org/luhn/rocketsled.svg?branch=master)](https://travis-ci.org/luhn/rocketsled)

Rocksled uploads your static files to a cloud storage service.  (Currently only
Amazon S3 is supported.)  These uploaded files are immutable.  This means that
they can be heavily cached and that your application will always be loading the
correct static files, even if you're running two or more versions of the
application simultaneously.
