def z_algorithm(string):
    """ Returns a z_array, such that for all i, z_array[i] contains
    the length of the longest substring starting at position i of the
    string that matches its prefix

    :time complexity: O(n)
    :space complexity: O(n), where n is the length of the string
    """
    z_array = [0] * len(string)
    z_array[0] = len(string)
    left = right = -1
    index = 1
    while index < len(string):
        # when index is outside the current Z-box
        # explicit comparisons starting from first character
        if index > right:
            left, right, counter = character_comparison(string, index, left, right, 0)
            z_array[index] = counter
        # when index is in the current Z-box
        else:
            remaining = right - index + 1
            reference_index = index - left
            if z_array[reference_index] < remaining:
                z_array[index] = z_array[reference_index]
            elif z_array[reference_index] > remaining:
                z_array[index] = remaining
            else:
                # explicit comparisons starting from the right + 1
                number_known_same_char = right - index + 1
                left, right, counter = character_comparison(string, right + 1, left, right, number_known_same_char)
                z_array[index] = counter
        # print("index:" + str(index) + "; z val: " + str(z_array[index]) + " left: " + str(left)
        #       + " right: " + str(right))
        index += 1

    return z_array


def character_comparison(string, pointer, left, right, number_known_same_char):
    """ Does explicit character comparison starting
    from the first character of the string and pointer,
    and redraws the Z-box (indicated by left & right) if
    necessary

    :time complexity: O(n);
    :space complexity: O(n), where n is the length of the string
    """
    counter = number_known_same_char
    start = pointer
    while pointer < len(string) and string[counter] == string[pointer]:
        counter += 1
        pointer += 1

    # redraws the Z-box if its length is greater than 0
    if counter > 0:
        left = start - number_known_same_char
        if pointer - 1 > right:
            right = pointer - 1
    return left, right, counter


def z_algo_tester():
    f = open("ZAlgoTests(abc).txt")
    contents = f.read().splitlines()
    f.close()

    ans_list = []
    for test_case in contents:
        ans_list += [z_algorithm(test_case)]

    output_file = open("test output.txt", "w")
    for ans in ans_list:
        output_file.write(str(ans) + "\n")
    output_file.close()


if __name__ == "__main__":
    # z_algo_tester()
    t = "abdabdabcbcd"
    p = "abcd"
    my_str = p + "$" + t
    print(z_algorithm(my_str))