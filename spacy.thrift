namespace py spacyThrift

struct Token {
  1: string text,
  2: string tag,
  3: string lemma
  4: optional string entity
}

service SpacyThrift {
  list<Token> tag(1: string sentence)
  list<Token> ner(1: string sentence)
}
