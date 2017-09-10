# spacy-thrift

[spaCy](https://github.com/explosion/spaCy) as a service using [Thrift](https://thrift.apache.org)


## Usage

Download spaCy's parser model for English:

- `python3 -m spacy download en`

Run the service:

- `python3 -m spacyThrift.service`


## Development

- The Thrift code can be updated using:

  `thrift -r --gen py --out . spacy.thrift`
  
- If a new version of Thrift is used, also ensure the version is specified in `requirements.txt`
