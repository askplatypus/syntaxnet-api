SyntaxNet API
=============

## This repository is obsolete

Much better alternative to SyntaxNet now exists like [Spacy](https://spacy.io/) and [StanfordNLP](https://stanfordnlp.github.io/stanfordnlp/). They are much more usable, provides similar performances and much better tokenization.




## Old documentation

A small HTTP API for SyntaxNet under Apache 2 Licence.
Live version at [http://syntaxnet.askplatyp.us](http://syntaxnet.askplatyp.us).
It relies on [syntaxnet_wrapper](https://github.com/livingbio/syntaxnet_wrapper).

Currently only provides a way to call SyntaxNet universal dependencies models.

### Install

Docker is currently the only supported installation way:

```
git clone https://github.com/askplatypus/syntaxnet-api
cd syntaxnet-api
docker build . -t syntaxnet-api
```

It creates a new Docker image called `syntaxnet-api` exposing the service on port 7000.
