import re

class RegexSanitization:

    def sanitise_dates(self, text):
        text_without_date = re.sub("((((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))|(((0[1-9]|[12]\d|3[01])(0[13578]|1[02])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|[12]\d|30)(0[13456789]|1[012])((1[6-9]|[2-9]\d)?\d{2}))|((0[1-9]|1\d|2[0-8])02((1[6-9]|[2-9]\d)?\d{2}))|(2902((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00))))", "[Date]", text)
        return (text_without_date)


    def sanitise_days(self, text):
        text_without_day = re.sub(
            "Monday|Tuesday|Wednseday|Thursday|Friday|Saturday|Sunday", "[Day], ", text)
        return (text_without_day)


    def sanitise_months(self, text):
        text_without_month = re.sub(
            "January|February|March|April|May|June|July|August|September|October|November|December", "[Month], ", text)
        return (text_without_month)

    def sanitise_email_addresses(self, text):
        text_without_email = re.sub("\w+@\w+[.]\w+", "[Email]", text)
        return(text_without_email)
