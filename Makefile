.PHONY: generate

generate:
	thrift -r --gen py --out . spacy.thrift

