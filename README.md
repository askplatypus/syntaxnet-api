SyntaxNet API
=============

A small HTTP API for SyntaxNet under Apache 2 Licence.
Live version at [http://syntaxnet.askplatyp.us](http://syntaxnet.askplatyp.us).
It relies on [syntaxnet_wrapper](https://github.com/livingbio/syntaxnet_wrapper).

Currently only provides a way to call SyntaxNet universal dependencies models.

## Install

Docker is currently the only supported installation way:

```
git clone https://github.com/askplatypus/syntaxnet-api
cd syntaxnet-api
docker build . -t syntaxnet-api
```

It creates a new Docker image called `syntaxnet-api` exposing the service on port 7000.
