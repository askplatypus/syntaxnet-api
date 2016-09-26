"""
Copyright 2016 Thomas Pellissier Tanon All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from subprocess import Popen, PIPE

_universal_languages = {
    'grc': 'Ancient_Greek-PROIEL',
    'eu': 'Basque',
    'bg': 'Bulgarian',
    'zh': 'Chinese',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'de': 'German',
    'el': 'Greek',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'la': 'Latin-PROIEL',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish'
}


_PARSEY_EVAL = 'tensorflow-models/syntaxnet/bazel-bin/syntaxnet/parser_eval'
_CONTEXT = 'tensorflow-models/syntaxnet/syntaxnet/models/parsey_universal/context.pbtxt'
_MODELS_DIR = 'tensorflow-models/syntaxnet/universal_models/'


def parsey_universal_full_conllu(text: str, language_code: str):
    if language_code not in _universal_languages:
        raise ValueError('{} is not a supported language code. The supported language codes are {}'.format(language_code, _universal_languages.keys()))

    model_dir = _MODELS_DIR + _universal_languages[language_code]

    #tokenizer
    if language_code == 'zh':
        brain_tokenizer_process = Popen([
            _PARSEY_EVAL,
            '--input=stdin-untoken',
            '--output=stdin-untoken',
            '--hidden_layer_sizes=256,256',
            '--arg_prefix=brain_tokenizer_zh',
            '--graph_builder=structured',
            '--task_context={}'.format(_CONTEXT),
            '--resource_dir={}'.format(model_dir),
            '--model_path={}/tokenizer-params'.format(model_dir),
            '--slim_model',
            '--batch_size=1024',
            '--alsologtostderr'
        ], stdin=PIPE, stdout=PIPE)
    else:
        brain_tokenizer_process = Popen([
            _PARSEY_EVAL,
            '--input=stdin-untoken',
            '--output=stdin-untoken',
            '--hidden_layer_sizes=128,128',
            '--arg_prefix=brain_tokenizer',
            '--graph_builder=greedy',
            '--task_context={}'.format(_CONTEXT),
            '--resource_dir={}'.format(model_dir),
            '--model_path={}/tokenizer-params'.format(model_dir),
            '--slim_model',
            '--batch_size=32',
            '--alsologtostderr'
        ], stdin=PIPE, stdout=PIPE)
    brain_tokenizer_process.stdin.write(text)

    #morpher
    brain_morpher_process = Popen([
        _PARSEY_EVAL,
        '--input=stdin',
        '--output=stdout-conll',
        '--hidden_layer_sizes=64',
        '--arg_prefix=brain_morpher',
        '--graph_builder=structured',
        '--task_context={}'.format(_CONTEXT),
        '--resource_dir={}'.format(model_dir),
        '--model_path={}/morpher-params'.format(model_dir),
        '--slim_model',
        '--batch_size=1024',
        '--alsologtostderr'
    ], stdin=brain_tokenizer_process.stdout, stdout=PIPE)
    brain_tokenizer_process.stdout.close()

    #tagger
    brain_tagger_process = Popen([
        _PARSEY_EVAL,
        '--input=stdin-conll',
        '--output=stdout-conll',
        '--hidden_layer_sizes=64',
        '--arg_prefix=brain_tagger',
        '--graph_builder=structured',
        '--task_context={}'.format(_CONTEXT),
        '--resource_dir={}'.format(model_dir),
        '--model_path={}/tagger-params'.format(model_dir),
        '--slim_model',
        '--batch_size=1024',
        '--alsologtostderr'
    ], stdin=brain_morpher_process.stdout, stdout=PIPE)
    brain_morpher_process.stdout.close()

    #parser
    brain_parser_process = Popen([
        _PARSEY_EVAL,
        '--input=stdin-conll',
        '--output=stdout-conll',
        '--hidden_layer_sizes=512,512',
        '--arg_prefix=brain_parser',
        '--graph_builder=structured',
        '--task_context={}'.format(_CONTEXT),
        '--resource_dir={}'.format(model_dir),
        '--model_path={}/parser-params'.format(model_dir),
        '--slim_model',
        '--batch_size=1024',
        '--alsologtostderr'
    ], stdin=brain_tagger_process.stdout)
    brain_tagger_process.stdout.close()
    return brain_parser_process.communicate()[0]
