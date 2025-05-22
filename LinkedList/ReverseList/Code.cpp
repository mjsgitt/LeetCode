/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
```cpp
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
\```
