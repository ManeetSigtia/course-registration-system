# function that determines the pivot index
def partition(low, high, array):
    i = (low - 1)   # index of the smaller element that shows the correct position of pivot so far
    pivot = array[high].course_name  # selecting the last element as pivot that will be placed in the correct position

    for j in range(low, high):
        if array[j].course_name <= pivot:   # if the current element is smaller than the pivot,
            i = i + 1   # increment the index of the smaller element
            array[i], array[j] = array[j], array[i]  # swap the smallest and current element

    # at this point, all elements smaller than pivot are on the left of where the pivot should be placed
    # all elements larger than pivot are on the right of where the pivot should be placed

    array[i + 1], array[high] = array[high], array[i + 1]   # swap that places the pivot in its correct position
    return i + 1    # returning the correct index position of pivot


# function to perform quicksort
def quicksort(low, high, array):
    if low < high:
        # determining the pivot position
        pi = partition(low, high, array)
        # recursively calling quicksort on the left side of pivot
        quicksort(low, pi - 1, array)
        # recursively calling quicksort on the right side of pivot
        quicksort(pi + 1, high, array)
