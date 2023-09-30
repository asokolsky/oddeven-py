# Optimizing Box Weights

A set of items needs to be packed into two boxes.
Given an integer array of the item weights to be packed,
divide the item weights into two subsets, A and B, for packing into the
associated boxes, while respecting the following conditions:

* The intersection of A and B is null.
* The union A and B is equal to the original array.
* The number of elements in subset A is minimal.
* The sum of A's weights is greater than the sum of B's weights.

Return the subset A:

* in increasing order
* where the sum of A's weights is greater than the sum of B's weights.

If more than one subset A exists, return the one with the max total weight.

## Test 0

[3, 7, 5, 6, 2]

The 2 subsets that satisfy the conditions for A are [5, 7] and [6, 7]:

* A is minimal (size 2)
* Sum(A) = (5 + 7) = 12 > Sum(B) = (2 + 3 + 6) = 11
* Sum(A) = (6 + 7) = 13 > Sum(B) = (2 + 3 + 5) = 10
* The intersection of A and B is null and their union is equal to arr.
* The subset A where the sum of its weight is maximal is [6, 7].


## Test 1

[5, 3, 2, 4, 1, 2]

The subset of A that satisfies the conditions is [4, 5] :

* A is minimal (size 2)
* Sum(A) = (4 + 5) = 9 > Sum(B) = (1 + 2 + 2 +  3) = 8
* The intersection of A and B is null and their union is equal to arr.
* The subset A with the maximal sum is [4, 5].


## Test 2

[4, 2, 5, 1, 6]

The subset of A that satisfies the conditions is [5, 6]:

* A is minimal (size 2)
* Sum(A) = (5 + 6) = 11 > Sum(B) = (1 + 2 + 4) = 7
* Sum(A) = (4 + 6) = 10 > Sum(B) = (1 + 2 + 5) = 8
* The intersection of A and B is null and their union is equal to arr.
* The subset A with the maximal sum is [5, 6].
