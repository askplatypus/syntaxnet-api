SyntaxNet API
=============

A small HTTP API for SyntaxNet under Apache 2 Licence.
Live version at [http://syntaxnet.askplatyp.us](http://syntaxnet.askplatyp.us).

Currently only provides a way to call Parsey trained with universal dependencies.

The API documentation is availlable as a Swagger API description in the swagger.yaml file.

Are available languages with the following Universal Dependencies training sets:

* grc: Ancient_Greek-PROIEL
* eu: Basque
* bg: Bulgarian
* zh: Chinese
* hr: Croatian
* cs: Czech
* da: Danish
* nl: Dutch
* en: English
* et: Estonian
* fi: Finnish
* fr: French
* gl: Galician
* de: German
* el: Greek
* he: Hebrew
* hi: Hindi
* hu: Hungarian
* id: Indonesian
* it: Italian
* la: Latin-PROIEL
* no: Norwegian
* pl: Polish
* pt: Portuguese
* sl: Slovenian
* es: Spanish
* sv: Swedish

## Install

On Debian/Ubuntu

```
git clone --recursive --recurse-submodules https://github.com/askplatypus/syntaxnet-api
sh install-syntaxnet-debian.sh
pip3 install -r requirements.txt
python3 flask_server.py
```
