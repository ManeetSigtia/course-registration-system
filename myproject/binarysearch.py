def find_one_term(terms, low, high, course_name):
    # array is the sorted array of elements, character is the value to be found
    # initially, low is index position 0 and high is number of array elements - 1
    if high >= low:
        mid = (high + low) // 2  # mid is the average of high and low indices

        if terms[mid].course_name == course_name:   # the value has been found
            return True

        elif terms[mid].name > course_name:
            # recursively repeat binary search on the left side of the element
            return find_one_term(terms, low, mid - 1, course_name)

        else:
            # recursively repeat binary search on the ride side of the middle element
            return find_one_term(terms, mid + 1, high, course_name)
    else:
        return False  # value not found
