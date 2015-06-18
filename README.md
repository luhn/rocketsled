# Rocketsled — Immutable cloud files

[![Build Status](https://travis-ci.org/luhn/rocketsled.svg?branch=master)](https://travis-ci.org/luhn/rocketsled)

Rocksled uploads your static files to a cloud storage service.  (Currently only
Amazon S3 is supported.)  These uploaded files are immutable.  This means that
they can be heavily cached and that your application will always be loading the
correct static files, even if you're running two or more versions of the
application simultaneously.

## CORS

Cross Origin Resource Sharing allows a website to interact with resources from
other domains.  CORS is necessary to load some resources, such as webfonts,
from S3.  To enable CORS, paste the following into your S3 bucket policy.

```xml
<CORSConfiguration>
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
    </CORSRule>
</CORSConfiguration>
```

For more information on CORS with S3, see Amazon's
[documentation](http://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html).
