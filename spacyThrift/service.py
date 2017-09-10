import logging
import sys
from typing import List

import click
import coloredlogs
import spacy
from spacy.language import Language
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token as SpacyToken

from spacyThrift import SpacyThrift
from spacyThrift.ttypes import Token

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class Handler:
    def __init__(self, nlp: Language) -> None:
        self.nlp = nlp

    @classmethod
    def _lemma(cls, token: SpacyToken):
        if token.lemma_ != "-PRON-":
            return token.lemma_.lower().strip()
        else:
            return token.lower_

    def tag(self, sentence: str) -> List[Token]:
        document = self.nlp(sentence, parse=False, entity=False)   # type: Doc
        return [
            Token(element.orth_, element.tag_, self._lemma(element))
            for element in document   # type: SpacyToken
        ]


@click.command()
@click.option('--port', default=9090)
@click.option('--language', default='en')
def serve(port: int, language: str) -> None:
    coloredlogs.install(stream=sys.stderr, level=logging.INFO,
                        fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

    logging.info("Loading ...")
    nlp = spacy.load(language, parser=False, entity=False) # type: Language
    nlp.pipeline = [nlp.tagger]

    handler = Handler(nlp)
    processor = SpacyThrift.Processor(handler)
    server_socket = TSocket.TServerSocket(port=port)
    transport_factory = TTransport.TBufferedTransportFactory()
    protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadedServer(processor, server_socket, transport_factory, protocol_factory)
    logging.info("Serving on port %d ...", port)
    server.serve()


if __name__ == '__main__':
    serve()

