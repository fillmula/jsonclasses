from jsonclasses import jsonclass


@jsonclass
class SimpleArticle:
    title: str
    content: str
