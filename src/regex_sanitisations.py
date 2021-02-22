import re

class RegexSanitisation:

    def sanitise_document_regex(self, documents, regex_type):
        docs_to_return = documents
        if ("dates" in regex_type):
            docs_to_return = self.sanitise_dates(docs_to_return)
        if ("days" in regex_type):
            docs_to_return = self.sanitise_days(docs_to_return)
        if ("months" in regex_type):
            docs_to_return = self.sanitise_months(docs_to_return)
        if ("emails" in regex_type):
            docs_to_return = self.sanitise_email_addresses(docs_to_return)
        return docs_to_return

    def sanitise_dates(self, documents):
        dates_regex = "((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))|(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00))))"
        document_without_dates = self.sanitise(dates_regex, "[Date]", documents["sanitisedDocument"])
        highlighted_document = self.highlight(dates_regex, documents["highlightedDocument"])
        return ({"sanitisedDocument": document_without_dates, "highlightedDocument": highlighted_document})

    def sanitise_days(self, documents):
        days_regex = "Monday|Tuesday|Wednseday|Thursday|Friday|Saturday|Sunday"
        document_without_days = self.sanitise(days_regex, "[Day]",  documents["sanitisedDocument"])
        highlighted_document = self.highlight(days_regex, documents["highlightedDocument"])
        return ({"sanitisedDocument": document_without_days, "highlightedDocument": highlighted_document})

    def sanitise_months(self, documents):
        months_regex = "January|February|March|April|May|June|July|August|September|October|November|December"
        document_without_months = self.sanitise(months_regex, "[Month]",  documents["sanitisedDocument"])
        highlighted_document = self.highlight(months_regex, documents["highlightedDocument"])
        return ({"sanitisedDocument": document_without_months, "highlightedDocument": highlighted_document})

    def sanitise_email_addresses(self, documents):
        email_regex = "\w+@\w+[.]\w+"
        document_without_emails = self.sanitise(email_regex, "[Email]",  documents["sanitisedDocument"])
        highlighted_document = self.highlight(email_regex, documents["highlightedDocument"])
        return({"sanitisedDocument": document_without_emails, "highlightedDocument": highlighted_document})

    def sanitise(self, regex, replace_with, document):
        return(re.sub(regex, replace_with, document))

    def highlight(self, regex, document):
        matches = re.findall(regex, document)
        highlighted_document = document
        print(matches)
        for match in matches:
            highlighted_document = highlighted_document.replace(match, "<span style=\"background-color: orange\">" + match + "</span>")
        return highlighted_document
