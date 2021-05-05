from unittest import TestCase
import random

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            ### BEGIN SOLUTION
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left
            ### END SOLUTION

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def rebalance(t):
        ### BEGIN SOLUTION
        balance = 2
        while balance > 1 or balance < -1:
            if t.left != None:
                lefth = AVLTree.Node.height(t.left)
            else:
                lefth = 0
            if t.right != None:
                righth = AVLTree.Node.height(t.right)
            else:
                righth = 0
            balance = righth - lefth
            if balance > 1: # more on right
                lh = height(t.right.left)
                rh = height(t.right.right)
                if lh > rh: # RL
                    t.right.rotate_right()
                    t.rotate_left()
                elif lh < rh: # RR
                    t.rotate_left()
            elif balance < -1: # more on right
                lh = height(t.left.left)
                rh = height(t.left.right)
                if lh > rh: # LL
                    t.rotate_right()
                elif lh < rh: # LR
                    t.left.rotate_left()
                    t.rotate_right()
        ### END SOLUTION

    def add(self, val):
        assert(val not in self)
        ### BEGIN SOLUTION
        if self.root == None:
            self.root = AVLTree.Node(val)
        else:
            cursor = self.root
            found = False
            ancestors = []
            while not found:
                if val > cursor.val: # goes right of cursor
                    if cursor.right != None:
                        ancestors.append(cursor)
                        cursor = cursor.right
                    else:
                        cursor.right = AVLTree.Node(val)
                        self.size += 1
                        found = True
                elif val < cursor.val: # goes left of cursor
                    if cursor.left != None:
                        ancestors.append(cursor)
                        cursor = cursor.left
                    else:
                        cursor.left = AVLTree.Node(val)
                        self.size += 1
                        found = True
            for i in range(len(ancestors) - 1, -1, -1):
                node = ancestors[i]
                self.rebalance(node)
        ### END SOLUTION

    def __delitem__(self, val):
        assert(val in self)
        ### BEGIN SOLUTION
        if val == self.root.val and self.root.left == None and self.root.right == None:
            self.root = None
        else:
            cursor = self.root
            ancestors = []
            found = False
            while not found: # sets cursor to node to be deleted
                if val < cursor.val:
                    ancestors.append(cursor)
                    cursor = cursor.left
                elif val > cursor.val:
                    ancestors.append(cursor)
                    cursor = cursor.right
                else:
                    found = True
            curparent = ancestors[-1] # node that is before the node to be deleted
            if cursor.left != None and cursor.right == None:
                if cursor.left.val > curparent.val:
                    curparent.right = cursor.left
                else:
                    curparent.left = cursor.left
            elif cursor.right != None and cursor.left == None:
                if cursor.right.val > curparent.val:
                    curparent.right = cursor.right
                else:
                    curparent.left = cursor.right
            elif cursor.right == None and cursor.left == None:
                if cursor.val > curparent.val:
                    curparent.right = None
                else:
                    curparent.left = None
            else:
                current = cursor.left
                prev = None
                hold = []
                while current.right != None:
                    prev = current
                    hold.append(current)
                    current = current.right
                if prev == None:
                    current.right = cursor.right
                else:
                    if current.left != None:
                        ancestors[-1].right = current.left
                    current.left = cursor.left
                    current.right = cursor.right
                if current.val > curparent.val:
                    curparent.right = current
                else:
                    curparent.left = current
            for i in range(len(ancestors) - 1, -1, -1):
                node = ancestors[i]
                self.rebalance(node)
        ### END SOLUTION

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
# TEST CASES
################################################################################
def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

# LL-fix (simple) test
# 10 points
def test_ll_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 2, 1]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RR-fix (simple) test
# 10 points
def test_rr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 2, 3]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# LR-fix (simple) test
# 10 points
def test_lr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 1, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RL-fix (simple) test
# 10 points
def test_rl_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 3, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# ensure key order is maintained after insertions and removals
# 30 points
def test_key_order_after_ops():
    tc = TestCase()
    vals = list(range(0, 100000000, 333333)) 
    random.shuffle(vals)

    t = AVLTree()
    for x in vals:
        t.add(x)

    for _ in range(len(vals) // 3):
        to_rem = vals.pop(random.randrange(len(vals)))
        del t[to_rem]

    vals.sort()

    for i,val in enumerate(t):
        tc.assertEqual(val, vals[i])

# stress testing
# 30 points
def test_stress_testing():
    tc = TestCase()

    def check_balance(t):
        tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

    t = AVLTree()
    vals = list(range(1000))
    random.shuffle(vals)
    for i in range(len(vals)):
        t.add(vals[i])
        for x in vals[:i+1]:
            tc.assertIn(x, t, 'Element added not in tree')
        traverse(t.root, check_balance)

    random.shuffle(vals)
    for i in range(len(vals)):
        del t[vals[i]]
        for x in vals[i+1:]:
            tc.assertIn(x, t, 'Incorrect element removed from tree')
        for x in vals[:i+1]:
            tc.assertNotIn(x, t, 'Element removed still in tree')
        traverse(t.root, check_balance)



################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_ll_fix_simple,
              test_rr_fix_simple,
              test_lr_fix_simple,
              test_rl_fix_simple,
              test_key_order_after_ops,
              test_stress_testing]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
