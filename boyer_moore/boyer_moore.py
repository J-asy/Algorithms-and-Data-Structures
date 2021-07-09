from reverse_z import z_suffix
from z_algorithm import z_algorithm


def bad_character_preprocess(pattern, alphabet_size):
    """ Returns an array of size alphabet_size*len(pattern), where each position bad_char_array[i][j]:
    i represents a character in pattern and
    j represents the position of the rightmost same such character on the left of position i in pattern.

    :time complexity: O(n*alphabet_size) ~ O(n);
    :space complexity: O(n*alphabet_size) ~ O(n), where n is the length of the pattern
    """
    bad_char_array = [[0] * len(pattern) for _ in range(alphabet_size)]
    for i in range(len(pattern) - 1, -1, -1):
        position = ord(pattern[i]) - 97
        bad_char_array[position][i] = i + 1
        if i + 1 < len(pattern) and bad_char_array[position][i + 1] == 0:
            j = i + 1
            while j < len(pattern) and bad_char_array[position][j] == 0:
                bad_char_array[position][j] = i + 1
                j += 1
    return bad_char_array


def good_suffix_preprocess(z_suffix_array):
    """ Returns an array whereby ...

    :time complexity: O(m);
    :space complexity: O(m), where m is the length of the z_array

    """
    m = len(z_suffix_array)
    good_suffix_array = [-1] * (m + 1)
    for i in range(m - 1):
        index = m - z_suffix_array[i]
        good_suffix_array[index] = i

    return good_suffix_array


def match_prefix_preprocess(z_array):
    match_prefix_array = [0] * (len(z_array) + 1)
    i = len(z_array) - 1
    while i >= 0:
        if z_array[i] + i == len(z_array):
            match_prefix_array[i] = z_array[i]
        else:
            match_prefix_array[i] = match_prefix_array[i + 1]
        i -= 1
    return match_prefix_array


def galil_comparison(pattern, text, align_end_index, pattern_start, pattern_stop):
    """ Compares characters from right to left, while skipping characters in the pattern from
        pattern_start and pattern_stop. Returns True is no mismatch found, returns mismatching
        character's index (of text) """
    # compare characters from align_end_index (inclusive) to pattern_stop (exclusive)
    text_index = align_end_index
    pattern_index = len(pattern) - 1
    right_value, comparisons = compare(pattern, text, text_index, pattern_index, pattern_stop)
    if right_value is not None:
        return right_value, comparisons

    # compare characters from pattern_start (exclusive) to align_start_index (exclusive)
    align_start_index = align_end_index - len(pattern) + 1
    text_index = pattern_start - 1
    pattern_index = len(pattern) - (align_end_index - pattern_start) - 2
    return compare(pattern, text, text_index, pattern_index, align_start_index - 1)


def compare(pattern, text, text_index, pattern_index, stop):
    counter = 0
    while text_index > stop and text_index > -1 and pattern_index > -1:
        counter += 1
        if pattern[pattern_index] != text[text_index]:
            return text_index, counter
        pattern_index -= 1
        text_index -= 1
    return None, counter


def boyer_moore(pattern, text):
    m = len(pattern)
    bad_character_array = bad_character_preprocess(pattern, 26)
    good_suffix_array = good_suffix_preprocess(z_suffix(pattern))
    match_prefix_array = match_prefix_preprocess(z_algorithm(pattern))
    total_comparisons = 0

    output = []
    start = stop = len(pattern)
    pointer = len(pattern) - 1
    while pointer < len(text):
        mismatch, comparisons = galil_comparison(pattern, text, pointer, start, stop)
        total_comparisons += comparisons

        if mismatch is not None:
            mismatch_at_pattern = m - (pointer - mismatch) - 1

            # check bad character shift
            bad_character_index = ord(text[mismatch]) - 97
            bad_character_value = bad_character_array[bad_character_index][mismatch_at_pattern]
            bad_character_shift = max(1, mismatch_at_pattern - bad_character_value + 1)

            # check good suffix shift
            good_suffix_value = good_suffix_array[mismatch_at_pattern + 1]
            if good_suffix_value > -1:
                good_suffix_shift = m - good_suffix_value - 1
            else:
                # no good suffix, hence check prefix matching
                match_prefix_value = match_prefix_array[mismatch_at_pattern + 1]
                good_suffix_shift = m - match_prefix_value

            start = mismatch + 1
            stop = pointer
            pointer += max(good_suffix_shift, bad_character_shift)

        else:
            # all match, hence shift using prefix matching
            output += [pointer - m + 1]
            good_suffix_shift = m - match_prefix_array[1]

            stop = start = pointer
            pointer += good_suffix_shift

    return output, total_comparisons






