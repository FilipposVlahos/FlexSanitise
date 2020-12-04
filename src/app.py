from common_components import DocumentRetrieval
from regex_sanitizations import RegexSanitization

import os

print (os.getcwd())

regex_sanitiser = RegexSanitization()
documt_retriever = DocumentRetrieval()

def main():
    doc = documt_retriever.get_document()
    san_text = regex_sanitiser. sanitise_dates(doc)
    san_text = regex_sanitiser. sanitise_days(san_text)
    san_text = regex_sanitiser. sanitise_months(san_text)
    san_text = regex_sanitiser. sanitise_email_addresses(san_text)
    print(san_text)

main()
