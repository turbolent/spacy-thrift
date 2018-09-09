import logging
import sys
from typing import List, Optional

import click
import coloredlogs
import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token as SpacyToken

from spacyThrift import SpacyThrift
from spacyThrift.ttypes import Token

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class Handler:
    def __init__(self, tagging_nlp: Language, ner_nlp: Optional[Language] = None) -> None:
        self.tagging_nlp = tagging_nlp
        self.ner_nlp = ner_nlp

    @classmethod
    def _lemma(cls, token: SpacyToken):
        if token.lemma_ != "-PRON-":
            return token.lemma_.lower().strip()
        else:
            return token.lower_

    def tag(self, sentence: str) -> List[Token]:
        document = self.tagging_nlp(sentence)   # type: Doc
        return [
            Token(element.orth_, element.tag_, self._lemma(element))
            for element in document   # type: SpacyToken
        ]

    def ner(self, sentence: str) -> List[Token]:
        if not self.ner_nlp:
            return None
        document = self.ner_nlp(sentence)  # type: Doc
        return [
            Token(element.orth_, element.tag_, self._lemma(element),
                  '-'.join([element.ent_iob_, element.ent_type_])
                  if element.ent_type_ else None)
            for element in document  # type: SpacyToken
        ]


@click.command()
@click.option('--port', default=9090)
@click.option('--language', default='en')
@click.option('--ner', is_flag=True)
def serve(port: int, language: str, ner: bool) -> None:
    coloredlogs.install(stream=sys.stderr, level=logging.INFO,
                        fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

    logging.info("Loading ...")

    tagging_nlp = spacy.load(language, disable=['ner'])  # type: Language
    tagging_nlp.remove_pipe('parser')
    logging.info("Tagging pipeline: %s", ', '.join(tagging_nlp.pipe_names))

    ner_nlp = None
    if ner:
        ner_nlp = spacy.load(language)  # type: Language
        logging.info("NER pipeline: %s", ', '.join(ner_nlp.pipe_names))

    handler = Handler(tagging_nlp, ner_nlp)

    processor = SpacyThrift.Processor(handler)
    server_socket = TSocket.TServerSocket(port=port)
    transport_factory = TTransport.TBufferedTransportFactory()
    protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadedServer(processor, server_socket, transport_factory, protocol_factory)
    logging.info("Serving on port %d ...", port)
    server.serve()


if __name__ == '__main__':
    serve()
