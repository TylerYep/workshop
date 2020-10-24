/*
 * An implementation of a priority queue class backed by a
 * binomial heap.  A descripton of how such heaps work can
 * be found in "Introduction to Algorithms, Second Edition"
 * by Cormen, Leisserson, Rivest, and Stein.  The
 * implementation contained in this file is optimized for
 * readability rather than speed, but all of the heap
 * operations have the correct asymptotic runtime.
 *
 * A class representing a binomial heap, which is a priority
 * queue supporting the following operations with the following
 * runtimes.  Because of character limitations in C++ code,
 * the @ sign should be taken to mean big-Theta
 *
 * Operation             | Runtime
 * ----------------------+----------
 * Create empty heap     | @(1)
 * Insert single element | O(lg N)
 * Query min value       | @(lg N)
 * Merge heaps           | O(lg N)
 * Delete min            | @(lg N)
 */
template <typename T> class BinomialHeap {
public:
  /* void push(const T&);
   * Usage: myHeap.push(137);
   * --------------------------------------------------------
   * Adds a new element to the min-heap.
   */
  void push(const T&);

  /* const T& top() const;
   * Usage: cout << myHeap.top() << endl;
   * --------------------------------------------------------
   * Returns an immutable reference to the minimum element in
   * the heap.
   */
  const T& top() const;

  /* void pop();
   * Usage: myHeap.pop();
   * --------------------------------------------------------
   * Removes the top element of the min-heap.
   */
  void pop();

  /* void merge(BinomialHeap& other);
   * Usage: one.merge(two);
   * --------------------------------------------------------
   * Merges the contents of two BinomialHeaps into this
   * BinomialHeap.  The other heap is destructively modified
   * and emptied.
   */
  void merge(BinomialHeap& other);

  /* size_t size() const;
   * bool   empty() const;
   * Usage: while (!myHeap.empty()) { ... }
   * --------------------------------------------------------
   * Returns the number of elements in the heap and whether the
   * heap is empty, respectively.
   */
  size_t size() const;
  bool empty() const;

  /* void swap(BinomialHeap& other);
   * Usage: one.swap(two);
   * --------------------------------------------------------
   * Exchanges the contents of this heap and another heap.
   */
  void swap(BinomialHeap& other);
};

/******** Implementation Below This Point ***********/

/* Definition of the BinomialNode class and assorted operations on it. */
namespace detail {

  /* A node in a binomial tree.  Each node stores a pointer to its first
   * child and to its rightmost sibling.
   */
  template <typename T> struct BinomialNode {
    T mValue;
    BinomialNode* mRight; // Right sibling
    BinomialNode* mChild; // Child node

    /* Constructs a BinomialNode given its value, right sibling, and child. */
    BinomialNode(const T& value, BinomialNode* right, BinomialNode* child) {
      mValue = value;
      mRight = right;
      mChild = child;
    }
  };

  /* To find the least element, we scan the tops of all of the trees in the
   * heap and return the smallest value.  This requires the use of a helper
   * function.
   *
   * Because some trees may be NULL, this comparison first checks if the either
   * tree is NULL.  If so, that tree is considered "heavier" than the other
   * tree.  That is, the comparison places all NULL elements after all
   * non-NULL elements.
   */
  template <typename T>
  bool CompareNodesByValue(const BinomialNode<T>* lhs,
                           const BinomialNode<T>* rhs) {
    /* If either of the trees is null, put the non-null tree in front of the
     * null tree.
     */
    if (!lhs || !rhs)
      return !lhs < !rhs;

    /* Otherwise do a straight comparison of the values. */
    return lhs->mValue < rhs->mValue;
  }

  /* Utility function which, given two binomial trees obeying the min-heap
   * property, merges them together into one tree and returns it as the result.
   */
  template <typename T>
  BinomialNode<T>* MergeTrees(BinomialNode<T>* lhs, BinomialNode<T>* rhs) {
    /* Check that the rhs isn't bigger and, if it is, swap the two so that
     * lhs <= rhs.
     */
    if (rhs->mValue < lhs->mValue)
      std::swap(lhs, rhs);

    /* Because we are assuming these trees are roots, the pointer rewiring is
     * not particularly tricky.  We change rhs's right pointer (currently
     * empty) to be lhs's first child, and then retarget lhs's child pointer
     * to be rhs.
     */
    rhs->mRight = lhs->mChild;
    lhs->mChild = rhs;

    /* Return whichever one is now the root. */
    return lhs;
  }

  /* Utility function which, given two lists of BinomialTrees, merges those
   * trees together.
   *
   * This function destructively modifies lhs and rhs by assigning lhs the
   * result and emptying rhs.
   *
   * Binomial heap merging is very similar to addition of binary numbers.
   * Because for each order there's either a tree of that order present or
   * there isn't, we can think of a binomial heap as a binary number where
   * each bit is 0 if a binomial tree of the proper order is missing and 1
   * otherwise.  When merging two heaps, we essentially "add" the two numbers
   * together using the following math:
   *
   * The sum of two empty trees is an empty tree (0 + 0 = 0)
   * The sum of an empty tree and a nonempty tree is a nonempty tree (0+1 = 1)
   * The sum of two nonempty trees is a merge of those trees, which has size
   *     twice as large as the original tree (1+1 = 10b)
   *
   * The logic to implement this code works as follows.  We iterate across the
   * trees from lowest-order to highest-order, summing them as we go and
   * writing the result bit by bit to some output list of trees.  At each step
   * we maintain a "carry" which holds the overflow from the previous step,
   * if there was one.  This is analogous to the carrying performed in
   *grade-school addition.
   */
  
/* Dequeuing the min element consists of:
 * 1. Locating it.
 * 2. Breaking its children apart into a collection of trees.
 * 3. Merging those trees in with this one.
 */
template <typename T>
void BinomialHeap<T>::pop() {
  /* Locate the smallest element. */
  typename std::vector<detail::BinomialNode<T>*>::iterator minElem =
    std::min_element(mTrees.begin(), mTrees.end(),
                     detail::CompareNodesByValue<T>);

  /* Build up a list of its direct children. */
  std::vector<detail::BinomialNode<T>*> children;
  for (detail::BinomialNode<T>* child = (*minElem)->mChild;
       child != NULL; child = child->mRight)
    children.push_back(child);

  /* These children were added in reverse order because as they're
   * merged, higher-order trees have lower-order trees as children
   * but the trees are stored in ascending orders in the vectors.
   * Therefore, we need to reverse the list. Thanks to Till Nilssen
   * for pointing this out.
   */
  std::reverse(children.begin(), children.end());

  /* The children are all currently linked together due to the left-
   * child/right-sibling representation. We need to detach them so
   * that they appear to be a collection of independent trees.
   */
  for (size_t i = 0; i < children.size(); ++i)
    children[i]->mRight = NULL;

  /* Free the memory from the tree we just removed, then remove it
   * from the list of trees.
   */
  delete *minElem;
  *minElem = NULL;

  /* Shrink forest size if we just got rid of the last tree. */
  if (minElem == mTrees.end() - 1)
    mTrees.pop_back();

  /* Merge this list back in. */
  detail::BinomialHeapMerge(mTrees, children);

  /* Track our size. */
  --mSize;
}
