Author: Keith Schwarz (htiek@cs.stanford.edu)
Ported to Python by Dan Stromberg (strombrg@gmail.com)
Rewritten and optimized by Tyler Yep.

An implementation of a priority queue backed by a Fibonacci heap, as described
by Fredman and Tarjan. Fibonacci heaps are interesting theoretically because
they have asymptotically good runtime guarantees for many operations. In
particular, insert, peek, and decrease-key all run in amortized O(1) time.
dequeue_min and delete each run in amortized O(log n) time. This allows
algorithms that rely heavily on decrease-key to gain significant performance
boosts. For example, Dijkstra's algorithm for single-source shortest paths can
be shown to run in O(m + n log n) using a Fibonacci heap, compared to O(m log n)
using a standard binary or binomial heap.

Internally, a Fibonacci heap is represented as a circular, doubly-linked list
of trees obeying the min-heap property. Each node stores pointers to its
parent (if any) and some arbitrary child. Additionally, every node stores its
degree (the number of children it has) and whether it is a "marked" node.
Finally, each Fibonacci heap stores a pointer to the tree with the minimum
value.

To insert a node into a Fibonacci heap, a singleton tree is created and merged
into the rest of the trees. The merge operation works by simply splicing
together the doubly-linked lists of the two trees, then updating the min
pointer to be the smaller of the minima of the two heaps. Peeking at the
smallest element can therefore be accomplished by just looking at the min
element. All of these operations complete in O(1) time.

The tricky operations are dequeue_min and decrease_key. dequeue_min works by
removing the root of the tree containing the smallest element, then merging its
children with the topmost roots. Then, the roots are scanned and merged so
that there is only one tree of each degree in the root list. This works by
maintaining a dynamic array of trees, each initially null, pointing to the
roots of trees of each dimension. The list is then scanned and this array is
populated. Whenever a conflict is discovered, the appropriate trees are merged
together until no more conflicts exist. The resulting trees are then put into
the root list. A clever analysis using the potential method can be used to
show that the amortized cost of this operation is O(log n), see "Introduction to
Algorithms, Second Edition" by Cormen, Rivest, Leiserson, and Stein for more
details.

The other hard operation is decrease_key, which works as follows. First, we
update the key of the node to be the new value. If this leaves the node
smaller than its parent, we're done. Otherwise, we cut the node from its
parent, add it as a root, and then mark its parent. If the parent was already
marked, we cut that node as well, recursively mark its parent, and continue
this process. This can be shown to run in O(1) amortized time using yet
another clever potential function. Finally, given this function, we can
implement delete by decreasing a key to -infinity, then calling dequeue_min to
extract it.
