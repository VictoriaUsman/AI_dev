bubble_sort <- function(arr) {
  n <- length(arr)
  
  for (i in 1:n) {
    for (j in 1:(n - i)) {
      if (arr[j] > arr[j + 1]) {
        temp <- arr[j]
        arr[j] <- arr[j + 1]
        arr[j + 1] <- temp
      }
    }
  }
  
  return(arr)
}

# Example
arr <- c(5, 2, 8, 12, 3)
print(bubble_sort(arr))




  def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

# Example
arr = [5, 2, 8, 12, 3]
print(bubble_sort(arr))
