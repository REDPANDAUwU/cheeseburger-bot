import time


def display_time(seconds, granularity=5):
    result = []
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def get_time(data, prefix, size, region, reserve_time):
    preorderstart = 1626454800

    if reserve_time > int(time.time()):
        output = f'u put the wrong time u need to do command like "{prefix}' \
                 f'steamdick 256 us 1626476609"\n' \
                 f'it goes size, region, rtReserveTime which u can get here\n' \
                 f'https://store.steampowered.com/reservation/ajaxgetuserstate?' \
                 f'rgReservationPackageIDs=%5B595603,595604,595605%5D'
        return output
    elif reserve_time < preorderstart:
        output = f'u put the wrong time u need to do command like "{prefix}' \
                 f'steamdick 256 us 1626476609"\n' \
                 f'it goes size, region, rtReserveTime which u can get here\n' \
                 f'https://store.steampowered.com/reservation/ajaxgetuserstate?' \
                 f'rgReservationPackageIDs=%5B595603,595604,595605%5D'
        return output

    bigst = 0
    for i in data:
        m = i.split()
        if m[0] == size and m[1] == region.upper() and int(m[2]) > bigst:
            bigst = int(m[2])
    # print(bigst)

    if bigst > reserve_time:
        output = 'ur steamdick rdy'
        return output
    elif bigst > time.time():
        output = 'wtf'
        return output
    else:
        percent = ((bigst - preorderstart) / (reserve_time - preorderstart)) * 100
        time_ordered = reserve_time - preorderstart
        ordered_str = display_time(time_ordered)

        preorders_time = bigst - preorderstart
        preorders_str = display_time(preorders_time)
        output = f"you ordered ur steam dick {ordered_str} after preorders opened\n" \
                 f"preorders are {preorders_str} after preorders opened\n" \
                 f"you are {str(percent)[:5]}% of the way to ur steam dick"

    return output


if __name__ == "__main__":
    data = open('content/data.bich', 'r').read().replace('\t', ' ').split('\n')
    # size = input('enter size')
    size = '256'
    # # region = input('enter region')
    region = 'US'
    # # reserve_time = int(input('enter rtreservetime'))
    reserve_time = 1626476609
    # print(data)
    print(get_time(data, '$', size, region, reserve_time))
