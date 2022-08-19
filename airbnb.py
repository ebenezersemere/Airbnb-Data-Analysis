import matplotlib.pyplot as plt
from scipy.stats.stats import spearmanr


def price_satisfaction(filename):
    """
    price_satisfaction takes a filename as a string and creates a list of lists (of float) where each sublist contains
    a pair of data: the price and the overall_satisfaction.
    :param filename: a file name (str)
    :return: data as a list of lists (list)
    """
    # open file
    with open(filename, "r", encoding="utf-8") as file_in:
        # initialize list
        satisfaction_list = []
        # read header
        header = file_in.readline()
        # split header
        split_header = header.split(",")
        # iterate through header and assign relevant columns
        for column in range(len(split_header)):
            # discovers price column
            if split_header[column] == "price":
                price_index = column
            # discovers overall satisfaction column
            if split_header[column] == "overall_satisfaction":
                overall_satisfaction_index = column
            # discovers reviews column
            if split_header[column] == "reviews":
                reviews_index = column
        # reads data
        data = file_in.readlines()
        # iterates through data lines
        for line in data:
            # splits data within each line
            list_data = line.split(",")
            # assigns price
            price = float(list_data[price_index])
            # assigns overall satisfaction
            overall_satisfaction = float(list_data[overall_satisfaction_index])
            # assigns reviews
            reviews = int((list_data[reviews_index]))
            # checks to see if reviews are positive
            if reviews > 0:
                # collects data to list
                satisfaction_list.append([price, overall_satisfaction])

    # returns list
    return satisfaction_list


def correlation(l):
    """
    correlation takes a list from the function price_satisfaction and returns the correlation between the price and the
    overall satisfaction.
    :param l: a list from price_satisfaction (list)
    :return: correlation between the price and the overall satisfaction (SpearmanrResult)
    """
    # initialize price list
    price_list = []
    # initialize overall satisfaction list
    overall_satisfaction_list = []
    # iterate through price_satisfaction list
    for i in range(len(l)):
        # collect price
        price = l[i][0]
        # collect overall satisfaction
        overall_satisfaction = l[i][1]
        # append price list
        price_list.append(price)
        # append overall satisfaction list
        overall_satisfaction_list.append(overall_satisfaction)
    # calculate spearmanr
    result = spearmanr(price_list, overall_satisfaction_list)
    # create correlation value tuple
    correlation_value = (result.correlation, result.pvalue)

    # return correlation value
    return correlation_value


def host_listings(filename):
    """
    host_listings takes a filename as a string. it returns a dictionary where the keys are host_ids (int) and the values
    are a list of room_ids (int) associated with each host_id.
    :param filename: a filename (str)
    :return: a dictionary (dict) of host_ids (keys) and associated room_ids (list of ints)
    """
    # open file
    with open(filename, "r", encoding="utf-8") as file_in:
        # initialize dictionary
        listings_dict = {}
        # read header
        header = file_in.readline()
        # split header
        split_header = header.split(",")
        # iterate through header and assign relevant columns
        for column in range(len(split_header)):
            # discovers host_id column
            if split_header[column] == "host_id":
                host_index = column
            # discovers room_id column
            if split_header[column] == "room_id":
                room_index = column
        # reads data
        data = file_in.readlines()
        # iterates through data lines
        for line in data:
            # splits data within each line
            list_data = line.split(",")
            # assigns host_id
            host_id = int(list_data[host_index])
            # assigns room_id
            room_id = int(list_data[room_index])
            # checks if host_id in dictionary keys. if yes, adds value to key. if no, creates new key with value.
            if host_id in listings_dict.keys():
                listings_dict[host_id] += [room_id]
            else:
                listings_dict[host_id] = [room_id]

    # returns listings_dict
    return listings_dict


def num_listings(d):
    """
    num_listings takes a dictionary (dict) from the function host_listings and returns a list l where l[i] is the number
    of hosts with exactly i listings.
    :param d: a dictionary (dict)
    :return: a list l where l[i] is the number of hosts with exactly i listings (list)
    """
    # initialize l
    l = []
    # initialize count_list
    count_list = []
    # assign listings_dictionary to host_listings dictionary values
    listings_dict = d.values()
    # iterate through values in listings_dictionary
    for item in listings_dict:
        # counts the number of values in each key:value pair
        count = int(len(item))
        # appends count_list with each value count
        count_list.append(count)

    # initialize highest number
    highest = 0
    # iterates through count_list to determine highest value
    for num in count_list:
        # updates num(ber) with highest value
        if num > highest:
            highest = num

    # iterates through to the highest amount of values
    for i in range(highest + 1):
        # initialize counter
        counter = 0
        # iterates through count_list
        for num in count_list:
            # checks if current index and value count are equivalent. if yes, counter increases by 1.
            if i == num:
                counter += 1
        # l is appended with the number of hosts with exact number of indexed listings
        l.append(counter)

    # return l
    return l


def room_prices(filename_list, roomtype):
    """
    room_prices is a function that takes a list of filenames (str) and one of several roomtypes (str). this
    function returns a dictionary where the keys are room_ids (int) and the values are a list of the prices (float)
    over time from oldest to most recent data.
    :param filename_list: a list of filenames (str)
    :param roomtype: a roomtype (str)
    :return: a dictionary (dict) with room_ids (int) as keys and list of prices (float) from oldest to most recent as
    values.
    """
    # initialize sort_dict
    sort_dict = {}

    # initialize sorted_file_list
    sorted_file_list = []
    # iterates through filename_list
    for file in filename_list:
        # strips date from filename into raw integer
        date = int(file[-14:-4].replace("-", ""))
        # appends list with file and date
        sorted_file_list.append([file, date])
        # sorts list in numerical order
        sorted_file_list.sort()

    # files orderly pass in
    for file in sorted_file_list:
        # opens file
        with open(file[0], "r", encoding="utf-8") as file_in:
            # read header
            header = file_in.readline()
            # split header
            split_header = header.split(",")
            # iterate through header and assign relevant columns
            for column in range(len(split_header)):
                # discovers price column
                if split_header[column] == "price":
                    price_index = column
                # discovers room_id column
                if split_header[column] == "room_id":
                    room_id_index = column
                # discover room_type column
                if split_header[column] == "room_type":
                    room_type_index = column
            # reads data
            data = file_in.readlines()
            # iterates through data lines
            for line in data:
                # splits data within each line
                list_data = line.split(",")
                # assigns room_type
                room_type = list_data[room_type_index]
                # checks room_type
                if room_type == roomtype:
                    # assigns price
                    price = float(list_data[price_index])
                    # assigns overall satisfaction
                    room_id = int((list_data[room_id_index]))
                    # checks if room_id already in sort_dict. yes? adds value to key. no? creates new key-value pair.
                    if room_id in sort_dict:
                        sort_dict[room_id] += [price]
                    else:
                        sort_dict[room_id] = [price]

    # returns sort_dict
    return sort_dict


def price_change(d):
    """
    price_change takes a dictionary from the function room_prices and returns a tuple with the following three elements:
    1. maximum percentage change among the listed properties, 2. starting price for the property with highest maximum
    percentage change, and 3. ending price for the property with the highest maximum percentage change.
    :param d: a dictionary (dict)
    :return: a tuple (tuple)
    """
    # initialize maximum change
    maximum_change = 0

    # iterate through dictionary values
    for values in d.values():
        # check length of each dictionary key's values
        val_length = len(values)
        # calculate change with arithmetic using latest and earliest date
        change = abs((((values[val_length - 1]) - values[0]) / values[0]) * 100)
        # checks if absolute change is greater than or equal to current greatest change
        if change >= maximum_change:
            # reassigns maximum change
            maximum_change = change
            # assigns starting price
            start_price = values[0]
            # assigns ending price
            end_price = values[val_length - 1]
    # tuple containing maximum change, start price, and end price
    price_values = (maximum_change, start_price, end_price)

    # return price_values
    return price_values


def price_by_neighborhood(filename):
    """
    price_by_neighborhood is a function that takes the name of a file (str) and returns a dictionary where each key
    is a neighborhood (str) that appears in the file and the value for a key is the average price for an
    â€œEntire home/aptâ€ listing in that neighborhood.
    :param filename:
    :return:
    """
    # initialize price and counter
    total_price = 0
    total_count = 0
    # open file
    with open(filename, "r", encoding="utf-8") as file_in:
        # initialize dictionary
        neighbor_dict = {}
        # read header
        header = file_in.readline()
        # split header
        split_header = header.split(",")
        # iterate through header and assign relevant columns
        for column in range(len(split_header)):
            # discovers neighborhood column
            if split_header[column] == "neighborhood":
                neighborhood_index = column
            # discovers price column
            if split_header[column] == "price":
                price_index = column
            if split_header[column] == "room_type":
                room_type_index = column
        # reads data
        data = file_in.readlines()
        # iterates through data lines
        for line in data:
            # splits data within each line
            list_data = line.split(",")
            # assigns neighborhood
            neighborhood = list_data[neighborhood_index]
            # assigns price
            price = int(float(list_data[price_index]))
            # assigns room type
            room_type = list_data[room_type_index]
            # checks if room type is "Entire home/apt"
            if room_type == "Entire home/apt":
                # adds price to total price and tick to counter
                total_price += price
                total_count += 1

    # average price arithmetic
    average_price = total_price / total_count
    # creates dictionary entry with neighborhood as key and average price as value
    neighbor_dict[neighborhood] = average_price

    return neighbor_dict


def plot_data():
    """
    plot_data is a function that creates a scatter plot comparing price and overall satisfaction for AirBnb listings
    in the city of Brno on 2017-07-20.
    """
    # initialize x - axis (price)
    x = []
    # initialize y - axis (overall satisfaction)
    y = []

    # iterate through data from price_satisfaction and append to 'x' and 'y'
    plot_list = price_satisfaction("tomslee_airbnb_brno_1500_2017-07-20.csv")
    for values in plot_list:
        x.append(values[0])
        y.append(values[1])

    # plot data
    plt.plot(x, y, "ro", label="data")

    # labels
    plt.title("Airbnb 2017-07-20 Brno 'Price v Overall Satisfaction'")
    plt.xlabel("Price")
    plt.ylabel("Overall Satisfaction")

    # display
    plt.legend()
    plt.show()


def main():
    """
    main calls plot_data
    """
    plot_data()

if __name__ == '__main__':
    main()
