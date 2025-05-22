struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    struct ListNode* frontline = head;
    struct ListNode* backline = head;
    int linkedlistlength = 0;
    int currentlistlenght = 0;
    
    while(frontline && ++linkedlistlength){
        frontline = frontline->next;
    }
    frontline = head;

    while(frontline){
        if((linkedlistlength - (currentlistlenght++)) == n){
            if(linkedlistlength == n){
                head = head->next;
                break;
            }
            backline->next = frontline->next;
            frontline = frontline->next;
            break;
        }
        backline = frontline;
        frontline = frontline->next;
    }
    return head;
}