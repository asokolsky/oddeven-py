"""
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing
together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:

1a>2a>4a
1b>3b>4b

1b>1a>2a>3b>4a>4b


Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:

Input: list1 = [], list2 = []
Output: []

Example 3:

Input: list1 = [], list2 = [0]
Output: [0]



Constraints:

    The number of nodes in both lists is in the range [0, 50].
    -100 <= Node.val <= 100
    Both list1 and list2 are sorted in non-decreasing order.


"""


class ListNode(object):
    '''
    Definition for singly-linked list.
    '''
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def identical(self, node) -> bool:
        if node is None:
            return False
        if self.val != node.val:
            return False
        if self.next is None:
            return node.next is None
        return self.next.identical(node.next)


class Solution(object):
    def mergeTwoLists(self, list1, list2):
        """
        :type list1: Optional[ListNode]
        :type list2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """

        if list1 is None:
            return list2
        elif list2 is None:
            return list1
        if list1.val < list2.val:
            return ListNode(list1.val, self.mergeTwoLists(list1.next, list2))
        return ListNode(list2.val, self.mergeTwoLists(list1, list2.next))



sol = Solution()

list1 = ListNode(1,ListNode(2,ListNode(4)))
list2 = ListNode(1,ListNode(3,ListNode(4)))
assert ListNode(1,ListNode(1,ListNode(2,ListNode(3,ListNode(4,ListNode(4)))))).identical(sol.mergeTwoLists(list1, list2))

list1 = None
list2 = None
assert None == sol.mergeTwoLists(list1, list2)

list1 = None
list2 = ListNode(0)
assert ListNode(0).identical(sol.mergeTwoLists(list1, list2))
