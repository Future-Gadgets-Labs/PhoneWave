def trim_with_ellipsis(text, max_length):
    """
    checking if provided string is longer than given value, if so then it needs to be cut and 3 dots need to be added
    """
    if len(text) > max_length and max_length > 3:
        text = text[0 : max_length - 3] + "..."
    return text


def shorten_big_number(number):
    """
    making number into human redable from, by shortening long numbers with adding K (for example 235000 will be transformed into 235K)
    note that this method doesn't return exact values, it rounds values to 1000
    note that input is int, and output is string
    """
    if number > 999:
        number = int(number / 1000)
        number = str(number) + "K"
    return number
