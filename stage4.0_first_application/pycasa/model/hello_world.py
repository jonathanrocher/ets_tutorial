from traits.api import HasStrictTraits, Str


class HelloWorldModel(HasStrictTraits):

    content = Str

    def _content_default(self):
        return "Hello World!"
