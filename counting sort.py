"""
File contains:
counting_sort_numerical, counting_sort_stable, counting_sort_alpha

"""


def counting_sort_numerical(new_list):
    """ Non-stable counting sort for numbers, assuming new_list has at least one item.

    :time complexity: O(n + m),
    :space complexity: O(n + m),
    :auxiliary space: O(m)
    where n is the number of items in the list and m is the greatest element of the list
    """
    # find the maximum: O(n)
    max_item = new_list[0]
    for i in range(1, len(new_list)):
        if new_list[i] > max_item:
            max_item = new_list[i]

    # initialize count array: O(m)
    count_array = [0] * (max_item + 1)

    # update count array: O(n)
    # just incrementing the frequency, not stable
    for item in new_list:
        count_array[item] += 1

    # update output: O(m+n)
    index = 0
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for _ in range(frequency):
            new_list[index] = item
            index += 1

    return new_list


def counting_sort_stable(new_list):
    """ Stable counting sort for numbers, assuming new_list has at least one item.

    :time complexity: O(n + m),
    :space complexity: O(n + m),
    :auxiliary space: O(n + m)
    where n is the number of items in the list and
    m is the greatest element of the list
    """
    # find the maximum: O(n)
    max_item = new_list[0]
    for i in range(1, len(new_list)):
        if new_list[i] > max_item:
            max_item = new_list[i]

    # initialize count array: O(m)
    count_array = [[] for _ in range(max_item + 1)]

    # update count array: O(n)
    for item in new_list:
        count_array[item].append(item)

    # update output array: O(m+n)
    # to make it stable, we append the actual item into count array
    index = 0
    for i in range(len(count_array)):
        for j in range(len(count_array[i])):
            new_list[index] = count_array[i][j]
            index += 1

    return new_list


def counting_sort_alpha(new_list):
    """ Stable counting sort for alphabets, assuming new_list has at least one letter.

    :time complexity: O(n + m),
    :space complexity: O(n + m),
     :auxiliary space: O(n + m)
    where n is the number of items in the list and
    m is the greatest element of the list
    """
    # find the maximum: O(n)
    max_item = ord(new_list[0]) - 97
    for i in range(1, len(new_list)):
        item = ord(new_list[i]) - 97
        if item > max_item:
            max_item = item

    # initialize count array: O(m)
    count_array = [0] * (max_item + 1)

    # update count array: O(n)
    for alpha in new_list:
        count_array[ord(alpha) - 97] += 1

    # update output array: O(m+n)
    index = 0
    for i in range(len(count_array)):
        item = chr(i + 97)
        frequency = count_array[i]
        for _ in range(frequency):
            new_list[index] = item
            index += 1

    return new_list

