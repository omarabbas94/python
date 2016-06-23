import nltk


class Field():
    def __init__(self, manager, analyst):
        """
        Determines a portion of an Ontology.

        Arguments:
        manager -- The application's Manager.
        analyst -- The Analyst processing this Field's ontology.
        """
        self.manager = manager
        self.analyst = analyst

    def analyze(self, item, dataset):
        """
        Exports Field data to the dataset

        Arguments:
        item -- A Item containing organic data.
        dataset -- A Dataset containing an ontology's processed data.
        """
        self.value = ''
        self.why = 'Default value or blank.'

    def document(self, key, dataset):
        """
        Returns this Field's value after saving it's why and outputing both.

        Arguments:
        key -- The human readable name of this Field.
        dataset -- This ontology's Dataset containing processed data.
        """
        dataset.whys[key] = self.why
        try:
            print('The value for', key, 'is', self.value, 'because', self.why)
        except(UnicodeEncodeError):
            print("UnicodeEncodeError")
        return self.value

    def restrict(self, item, value, term, removals=[], nears=[]):
        """
        Check a term with special exceptions

        Arguments:
        item -- An Item containing organic data.
        value -- The potential Field value.
        term -- The term to be checked in the text.
        removals -- Strings, typically containing the term, which should be.
        removed from the text to prevent false positives.
        nears -- Strings which, if they appear near the term, should invalidate
        the term's presence.
        """
        term = nltk.word_tokenize(term)

        tokens = []
        for removal in removals:
            removal = nltk.word_tokenize(removal)
            tokens = tokens or item.tokens

            new_tokens = []
            index = 0
            while index < len(tokens):
                result = tokens[index:index + len(removal)]
                if result == removal:
                    index += len(removal)
                else:
                    new_tokens.append(tokens[index])
                    index += 1

            tokens = new_tokens

        for index, token in enumerate(tokens):
            result = tokens[index:index + len(term)]
            if result == term:
                for near in nears:
                    close = tokens[index - 5:index + len(term) + 5]
                    if near in close:
                        break
                else:

                    self.save(item, value, term, index)

    def save(self, item, value, terms, index):
        """
        Saves a value and documents its explanation.

        Arguments:
        item -- An Item containg organic data.
        value -- The confirmed value that will be delivered to the Dataset.
        term -- The term that was found within the text
        which justifies the value.
        index -- The position of the term in the incident.tokens list.
        """
        term = ' '.join(terms)
        context = ' '.join(item.tokens[index - 20:index + 20])
        self.why = '"' + term + '" in text: "' + context + '."'
        self.value = value

    def text_check(self, item, value, *args):
        """
        Checks if a set of terms are in the Incident's text

        Arguments:
        item -- An Item containing organic data.
        *args -- the list of terms to check in the text.
        """
        for arg in args:
            terms = nltk.word_tokenize(arg)
            for index, token in enumerate(item.tokens):
                result = item.tokens[index:index + len(terms)]
                if result == terms:
                    self.save(item, value, terms, index)

