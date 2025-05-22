# ReverseList

This section provides an overview and visual aid for this problem.

<details>
<summary>Click to view the Approach Diagram</summary>
<br/>

![Approach Diagram](image/approach.png)

</details>

### Description
This folder contains the solution for reversing a singly linked list. The problem involves reversing the direction of pointers in a linked list so that the last node becomes the first node and vice versa.

### Code
<!-- CODE_START -->
```cpp
## Solution

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode* reverseList(struct ListNode* head) {
    struct ListNode* tail = NULL;
    struct ListNode* taild = NULL;
    struct ListNode* taild2 = NULL;
    if(head && head->next){
        tail = head->next;
        taild = head;
        while(tail->next){
            taild->next = taild2;
            taild2 = taild;
            taild = tail;
            tail = tail->next;
        }
        taild->next = taild2;
        tail->next = taild;
        head = tail;
        return head;
    }
    return head;
}

```
```
<!-- CODE_END -->