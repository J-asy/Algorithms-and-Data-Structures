

def counting_sort(num_list, b, col):
    """ Given a list of positive integers and a base, b, sorts the list
    using base b and returns it in ascending numerical order according
    to the col-th digit.

    :time complexity: O(n + b)
    :space complexity: O(n + b)
    :auxiliary space: O(b)
    where n is the length of num_list and b is the base that the list is sorted by
    """
    # initialize count array
    count_array = []
    for i in range(b):
        count_array.append([])

    # update count_array based on a particular column of the integers
    for item in num_list:
        count_array[(item // b ** col) % b].append(item)

    # update output
    index = 0
    for i in range(len(count_array)):
        for j in range(len(count_array[i])):
            num_list[index] = count_array[i][j]
            index += 1


def numerical_radix_sort(num_list, b):
    """ Given a list of positive integers and a base, b, sorts the list using base b
    and returns it in ascending numerical order by calling counting_sort() multiple times.

    :time complexity: O((n + b)*log_b M)
    :space complexity: O(n log_b M)
    :auxiliary space: O(n)
    where n is the length of num_list, b is the base and M is the numerical value of the
    greatest element in num_list
    """
    # if num_list contains less than 2 items, it is already sorted
    if len(num_list) > 1:

        # find max number: O(m)
        max_item = num_list[0]
        for item in num_list:
            if item > max_item:
                max_item = item

        # find number of columns of max number in base b
        # this loop takes log_b m, where b is the base and m is the max number
        num_col = 1
        while max_item >= b:
            max_item //= b
            num_col += 1

        # call counting_sort log_b m times
        for col in range(num_col):
            counting_sort(num_list, b, col)

    return num_list












