import locale


_TIME_LOCALE = None
_NUMERIC = None


def format_datetime(value, pattern='%d %b, %Y', locale_value=None):
    global _TIME_LOCALE
    if locale_value and (_TIME_LOCALE != locale_value):
        locale.setlocale(locale.LC_TIME, locale_value)
        _TIME_LOCALE = locale_value

    return value.strftime(pattern)


def format_decimal(value, digits, locale_value=None):
    global _NUMERIC
    if locale_value and (_NUMERIC != locale_value):
        locale.setlocale(locale.LC_NUMERIC, locale_value)
        _NUMERIC = locale_value

    value = round(value, digits)
    return locale.format('% .' + str(digits) + 'f', value)


def format_timedelta(value, digits):
    days, hours = divmod(value, 86400)
    hours, minutes = divmod(hours, 3600)
    minutes, seconds = divmod(minutes, 60)

    days, hours, minutes = [int(value) for value in [days, hours, minutes]]
    seconds = round(seconds, digits)

    output = '{} d'.format(days) if days else ''
    output = output + ' {} h'.format(hours) if hours else output
    output = output + ' {} min'.format(minutes) if minutes else output
    output = output + ' {} s'.format(seconds) if seconds else output

    return output
