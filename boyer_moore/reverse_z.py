
def z_suffix(string):
    """ Returns a z_array, such that for all i, z_array[i] contains
    the length of the longest substring starting at position i to the
    start of the string that matches string's suffix

    :time complexity: O(n)
    :space complexity: O(n), where n is the length of the string
    """
    z_array = [0]*len(string)
    z_array[-1] = len(string)
    left = right = len(string)

    index = len(string) - 2
    while index >= 0:
        # when index is outside the current Z-box
        # explicit comparisons start from rightmost character to the left
        if index < left:
            left, right, counter = z_character_comparison(string, index, left, right, 0)
            z_array[index] = counter
        # when index is in the current Z-box
        else:
            remaining = index - left + 1
            reference_index = len(string) - (right - index) - 1
            if z_array[reference_index] < remaining:
                z_array[index] = z_array[reference_index]
            elif z_array[reference_index] > remaining:
                z_array[index] = remaining
            else:
                # explicit comparisons starting from the left - 1
                number_known_same_char = index - left + 1
                left, right, counter = z_character_comparison(string, left - 1, left, right, number_known_same_char)
                z_array[index] = counter
        index -= 1

    return z_array


def z_character_comparison(string, pointer, left, right, number_known_same_char):
    """ Does explicit character comparison starting
    from the last character of the string and pointer to the left,
    and redraws the Z-box (indicated by left & right) if necessary

    :time complexity: O(n);
    :space complexity: O(n), where n is the length of the string
    """
    counter = number_known_same_char*-1 - 1
    start = pointer
    while pointer >= 0 and string[counter] == string[pointer]:
        counter -= 1
        pointer -= 1
    counter = (counter + 1)*-1

    # redraws the Z-box if its length is greater than 0
    if counter > 0:
        right = start + number_known_same_char
        if pointer + 1 < left:
            left = pointer + 1
    return left, right, counter



