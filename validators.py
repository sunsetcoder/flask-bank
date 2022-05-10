import re

def numberInBounds(number):
    return (number >= 0) and (number < 4294967296)

def validNumericFractionTwoDigits(fraction_input):
    if re.fullmatch(r'[0-9]{2}', fraction_input) is not None:
        return True
    return False

def validNumericNoLeadingZeros(numeric_input):
    if (re.fullmatch(r'(0|[1-9][0-9]*)', numeric_input) is not None):
        return True
    return False

def validAccountNameOrPassword(user_input_data):
    validLength = (len(user_input_data)>=1) and (len(user_input_data)<=127)
    if not validLength:
        return False
    if re.fullmatch(r'[_\-\.0-9a-z]*', user_input_data) is not None:
        return True
    return False


#print(validNumericNoLeadingZeros('01'))
#print(re.fullmatch(r'[0-9]{2}', 'a1'))
#print(validAccountNameOrPassword('$')) 