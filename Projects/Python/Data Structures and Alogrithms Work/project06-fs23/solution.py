"""
Project 6
CSE 331 FS23
Gabriel Sotelo
starter.py
"""
import math
from typing import TypeVar, Generator, List, Tuple, Optional
from collections import deque
import json
from queue import SimpleQueue

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
# represents a Node object (forward-declare to use in Node __init__)
Node = TypeVar("Node")
# represents a custom type used in application
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")


class Node:
    """
    Implementation of an BST and AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return repr(self)


####################################################################################################

class BinarySearchTree:
    """
    Implementation of an BSTree.
    Modify only below indicated line.
    """

    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty BST tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BST tree
        """
        if self.origin is None:
            return "Empty BST Tree"

        lines = pretty_print_binary_tree(self.origin, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def __str__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="bst_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Calculate and return the height of the given node in the AVL tree.
        The height of a node is the length of the longest path from that node to a leaf node.

        Parameters:
        root (Node): The node for which the height is to be calculated.

        Returns:
        int: The height of the node. If the node is None, the height is -1.
        """
        if root is None:
            return -1
        return root.height

    def insert(self, root: Node, val: T) -> Node:
        """
        Insert a new node with the given value into the AVL tree rooted at 'root'.
        If 'root' is None, a new node is created as the root of the tree.

        Parameters:
        root (Node): The root of the AVL tree where the new node is to be inserted.
        val (T): The value to be inserted into the AVL tree.

        Returns:
        Node: The root of the AVL tree after the insertion.
        """
        if root is None:
            if self.origin is None:
                self.origin = Node(val)
            self.size += 1
            return Node(val)

        if val < root.value:
            root.left = self.insert(root.left, val)
            root.left.parent = root
        elif val > root.value:
            root.right = self.insert(root.right, val)
            root.right.parent = root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return root

    def remove(self, root: Node, val: T) -> Node:
        """
        Remove a node with the given value from the AVL tree rooted at 'root'.

        Parameters:
        root (Node): The root of the AVL tree where the node with 'val' is to be removed.
        val (T): The value to be removed from the AVL tree.

        Returns:
        Node: The root of the AVL tree after the removal.
        """
        if root is None:
            return None

        # If the value to be deleted is smaller than the root's value,
        # then it lies in the left subtree
        if val < root.value:
            root.left = self.remove(root.left, val)

        # If the value to be deleted is greater than the root's value,
        # then it lies in the right subtree
        elif val > root.value:
            root.right = self.remove(root.right, val)

        # If value is the same as root's value, then this is the node to be deleted
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                self.size -= 1
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                self.size -= 1
                return temp

            # Node with two children: Get the inorder predecessor (largest in the left subtree)
            temp = self.get_max_value_node(root.left)

            # Copy the inorder predecessor's content to this node
            root.value = temp.value

            # Delete the inorder predecessor
            root.left = self.remove(root.left, temp.value)

        # Update the height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        return root

    def get_max_value_node(self, node):
        """
        Find and return the node with the maximum value in the AVL tree rooted at 'node'.
        This function is used to find the inorder predecessor during node removal.

        Parameters:
        node: The root of the AVL tree or a subtree to search in.

        Returns:
        Node: The node with the maximum value in the AVL tree rooted at 'node'.
        """
        current = node
        # Loop down to find the rightmost leaf
        while current.right is not None:
            current = current.right
        return current

    def search(self, root: Node, val: T) -> Node:
        """
        Search for a node with the given value in the AVL tree rooted at 'root'.
        If the node with 'val' is not found, it returns the nearest available node.

        Parameters:
        root (Node): The root of the AVL tree to search in.
        val (T): The value to be searched for in the AVL tree.

        Returns:
        Node: The node with the value 'val' if found, or the nearest available node if not found.
        """
        if root is None or root.value == val:
            return root

        if val < root.value:
            return self.search(root.left, val) if root.left else root
        else:
            return self.search(root.right, val) if root.right else root


class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """

    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string.

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        return super(AVLTree, self).__repr__()

    def __str__(self) -> str:
        """
        Represent the AVLTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="avl_tree_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Calculate the height of the subtree rooted at 'root'. The height of an empty subtree is -1.
        """
        if root is None:
            return -1
        return root.height

    def left_rotate(self, root: Node) -> Node:
        """
        Perform a left rotation on the given node 'root' in the AVL tree.

        Parameters:
        root (Node): The node to perform the left rotation on.

        Returns:
        Node: The new root of the rotated subtree.
        """
        if root is None or root.right is None:
            return root

        new_root = root.right
        root.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = root

        new_root.parent = root.parent
        if root.parent is None:
            self.origin = new_root
        elif root == root.parent.left:
            root.parent.left = new_root
        else:
            root.parent.right = new_root

        new_root.left = root
        root.parent = new_root

        # Update heights
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def right_rotate(self, root: Node) -> Node:
        """
        Perform a right rotation on the given node 'root' in the AVL tree.

        Parameters:
        root (Node): The node to perform the right rotation on.

        Returns:
        Node: The new root of the rotated subtree.
        """
        if root is None or root.left is None:
            return root

        new_root = root.left
        root.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = root

        new_root.parent = root.parent
        if root.parent is None:
            self.origin = new_root
        elif root == root.parent.right:
            root.parent.right = new_root
        else:
            root.parent.left = new_root

        new_root.right = root
        root.parent = new_root

        # Update heights
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def balance_factor(self, root: Node) -> int:
        """
        Compute the balance factor of a node in the AVL tree.
        The balance factor is the difference in heights of the left and right subtrees.
        A balance factor of -1, 0, or 1 indicates the subtree is balanced.

        Parameters:
        root (Node): The node whose balance factor is to be computed.

        Returns:
        int: The balance factor of the node.
        """
        if root is None:
            return 0
        return self.height(root.left) - self.height(root.right)

    def rebalance(self, root: Node) -> Optional[Node]:
        """
        Perform rebalancing of the AVL tree rooted at 'root' after insertions or deletions.

        Parameters:
        root (Node): The root of the subtree to be rebalanced.

        Returns:
        Optional[Node]: The new root of the rebalanced subtree.
        """
        if root is None:
            return None

        balance_factor = self.balance_factor(root)

        # Left-Left (LL) Case
        if balance_factor > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        # Right-Right (RR) Case
        if balance_factor < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right (LR) Case
        if balance_factor > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left (RL) Case
        if balance_factor < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def insert(self, root: Node, val: T) -> Node:
        """
        Insert a new node with the given value into the AVL tree rooted at 'root'.
        If 'root' is None, a new node is created as the root of the tree.

        Parameters:
        root (Node): The root of the AVL tree where the new node is to be inserted.
        val (T): The value to be inserted into the AVL tree.

        Returns:
        Node: The root of the AVL tree after the insertion.
        """
        # Step 1: Perform the normal BST insertion
        if root is None:
            if self.origin is None:
                self.origin = Node(val)
            self.size += 1
            return Node(val)
        elif val < root.value:
            root.left = self.insert(root.left, val)
            root.left.parent = root
        elif val > root.value:
            root.right = self.insert(root.right, val)
            root.right.parent = root

        # Step 2: Update height of this ancestor node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Step 3: Get the balance factor of this ancestor node to check whether this node became unbalanced
        balance = self.balance_factor(root)

        # Step 4: If the node is unbalanced, then try out the 4 cases
        # Left Left Case
        if balance > 1 and val < root.left.value:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and val > root.right.value:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and val > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and val < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # Step 5: Return the (unchanged) node pointer
        return root

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Remove a node with the given value from the AVL tree rooted at 'root'.

        Parameters:
        root (Node): The root of the AVL tree where the node with 'val' is to be removed.
        val (T): The value to be removed from the AVL tree.

        Returns:
        Optional[Node]: The root of the AVL tree after the removal.
        """
        # Base case: The node is not found
        if root is None:
            return None

        # Step 1: Perform standard BST delete
        if val < root.value:
            root.left = self.remove(root.left, val)
        elif val > root.value:
            root.right = self.remove(root.right, val)
        else:
            # Node with only one child or no child
            if root.left is None or root.right is None:
                temp = root.left if root.left else root.right
                if temp is None:  # No child case
                    temp = root
                    root = None
                else:  # One child case
                    root = temp

                self.size -= 1
            else:
                # Node with two children, get the in-order successor
                temp = self.max(root.left)
                root.value = temp.value
                root.left = self.remove(root.left, temp.value)

        # If the tree had only one node, then return
        if root is None:
            return root

        # Step 2: Update the height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Step 3: Get the balance factor
        balance = self.balance_factor(root)

        # Step 4: Balance the tree
        # Left Left Case
        if balance > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def min(self, root: Node) -> Optional[Node]:
        """
        Finds the node with the minimum value in the subtree rooted at `root`.

        Parameters:
        root (Node): The root of the subtree to search.

        Returns:
        Node: The node with the maximum value, or None if the subtree is empty.
        """
        current = root
        while current and current.left:
            current = current.left
        return current

    def max(self, root: Node) -> Node:
        """
        Finds the node with the maximum value in the subtree rooted at `root`.

        Parameters:
        root (Node): The root of the subtree to search.

        Returns:
        Node: The node with the maximum value, or None if the subtree is empty.
        """
        current = root
        while current and current.right:
            current = current.right
        return current

    def search(self, root: Node, val: T) -> Node:
        """
        Searches for and returns the Node containing the value `val` in the subtree rooted at `root`.
        If `val` is not present, returns the Node below which `val` would be inserted as a child.

        Parameters:
        root (Node): The root of the subtree in which to search for `val`.
        val (T): The value to search for.

        Returns:
        Node: The Node containing `val`, or the Node below which `val` would be inserted.
        """
        if root is None:
            return None

        if val < root.value:
            return self.search(root.left, val) if root.left else root
        elif val > root.value:
            return self.search(root.right, val) if root.right else root
        else:
            return root

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform an inorder traversal of the AVL tree starting from the given root.
        In an inorder traversal, the left subtree is visited first, then the root node, and finally the right subtree.
        This method uses a generator to yield nodes in the traversal order.

        :param root: The root node of the subtree to start the traversal.
        :return: A generator yielding the nodes in inorder.
        """
        if root:
            yield from self.inorder(root.left)
            yield root
            yield from self.inorder(root.right)

    def __iter__(self) -> Generator[Node, None, None]:
        """
        Perform an inorder traversal of the AVL tree starting from the root.
        This method allows the AVL tree object to be iterated over.

        Returns:
        Generator[Node, None, None]: A generator yielding the nodes in inorder.
        """
        return self.inorder(self.origin)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a preorder traversal of the AVL tree starting from the given root.
        In a preorder traversal, the root node is visited first, then the left subtree, and finally the right subtree.
        This method uses a generator to yield nodes in the traversal order.

        :param root: The root node of the subtree to start the traversal.
        :return: A generator yielding the nodes in preorder.
        """
        if root:
            yield root
            yield from self.preorder(root.left)
            yield from self.preorder(root.right)

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a postorder traversal of the AVL tree starting from the given root.
        In a postorder traversal, the left subtree is visited first, then the right subtree, and finally the root node.
        This method uses a generator to yield nodes in the traversal order.

        :param root: The root node of the subtree to start the traversal.
        :return: A generator yielding the nodes in postorder.
        """
        if root:
            yield from self.postorder(root.left)
            yield from self.postorder(root.right)
            yield root

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a level order (breadth-first) traversal of the AVL tree starting from the given root.
        In a level order traversal, nodes are visited level by level from top to bottom and left to right.
        This method uses a generator to yield nodes in the traversal order.

        :param root: The root node of the subtree to start the traversal.
        :return: A generator yielding the nodes in level order.
        """
        if root:
            queue = SimpleQueue()
            queue.put(root)
            while not queue.empty():
                current = queue.get()
                yield current
                if current.left:
                    queue.put(current.left)
                if current.right:
                    queue.put(current.right)


####################################################################################################


class AVLWrappedDictionary:
    """
    Implementation of a helper class which will be used as tree node values in the
    NearestNeighborClassifier implementation.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["key", "dictionary"]

    def __init__(self, key: float) -> None:
        """
        Construct a AVLWrappedDictionary with a key to search/sort on and a dictionary to hold data.

        :param key: floating point key to be looked up by.
        """
        self.key = key
        self.dictionary = {}

    def __repr__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        pprinted_dict = json.dumps(self.dictionary, indent=2)
        return f"key: {self.key} dict:{self.dictionary}"

    def __str__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return repr(self)

    def __eq__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement == operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating whether keys of AVLWrappedDictionaries are equal
        """
        return abs(self.key - other.key) < 1e-6

    def __lt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement < operator to compare 2 AVLWrappedDictionarys by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key < other.key and not abs(self.key - other.key) < 1e-6

    def __gt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement > operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key > other.key and not abs(self.key - other.key) < 1e-6


class NearestNeighborClassifier:
    """
    Implementation of a one-dimensional nearest-neighbor classifier with AVL tree lookups.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["resolution", "tree"]

    def __init__(self, resolution: int) -> None:
        """
        Construct a one-dimensional nearest neighbor classifier with AVL tree lookups.
        Data are assumed to be floating point values in the closed interval [0, 1].

        :param resolution: number of decimal places the data will be rounded to, effectively
                           governing the capacity of the model - for example, with a resolution of
                           1, the classifier could maintain up to 11 nodes, spaced 0.1 apart - with
                           a resolution of 2, the classifier could maintain 101 nodes, spaced 0.01
                           apart, and so on - the maximum number of nodes is bounded by
                           10^(resolution) + 1.
        """
        self.tree = AVLTree()
        self.resolution = resolution

        # pre-construct lookup tree with AVLWrappedDictionary objects storing (key, dictionary)
        # pairs, but which compare with <, >, == on key only
        for i in range(10 ** resolution + 1):
            w_dict = AVLWrappedDictionary(key=(i / 10 ** resolution))
            self.tree.insert(self.tree.origin, w_dict)

    def __repr__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def __str__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return repr(self)

    def visualize(self, filename: str = "nnc_visualization.svg") -> str:
        svg_string = svg(self.tree.origin, 48, nnc_mode=True)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def fit(self, data: List[Tuple[float, str]]) -> None:
        """
        Train the Nearest Neighbor Classifier with a dataset, learning associations between
        feature values (x) and target labels (y).

        This method iterates through each (x, y) pair in the dataset, rounds the x value to
        the specified precision (based on self.resolution), finds the corresponding node in
        the tree using the rounded x value as a key, and updates the count of the label y in
        the associated dictionary.

        Parameters:
        data (List[Tuple[float, str]]): A list of (x, y) pairs representing the training data.

        Returns:
        None
        """
        for x, y in data:
            rounded = round(x, self.resolution)
            wrapped = AVLWrappedDictionary(rounded)
            searched = self.tree.search(self.tree.origin, wrapped)

            if searched is None:
                new_node = AVLWrappedDictionary(rounded)
                self.tree.insert(self.tree.origin, new_node)
                new_node.dictionary[y] = 1
            else:
                searched.value.dictionary[y] = searched.value.dictionary.get(y, 0) + 1

    def predict(self, x: float, delta: float) -> Optional[str]:
        """
        Predict the target label (y) for a given feature value (x) within a specified range (delta).

        This method rounds the x value to the specified precision (based on self.resolution), searches
        for nodes in the tree whose keys are within ± delta of the rounded x value, accesses the
        AVLWrappedDictionary objects at these nodes, and determines the most common label y across
        all these dictionaries.

        Parameters:
        x (float): Feature value to be predicted.
        delta (float): Range to search for neighboring feature values.

        Returns:
        Optional[str]: A string representing the predicted target label y, or None if no suitable
        data points are found within the specified range.
        """
        label_counts = {}
        lower_bound = round(x - delta, self.resolution)
        upper_bound = round(x + delta, self.resolution)

        for node in self.tree:
            node_key = node.value.key
            if lower_bound <= node_key <= upper_bound:
                for label, count in node.value.dictionary.items():
                    label_counts[label] = label_counts.get(label, 0) + count

        if not label_counts:
            return None

        return max(label_counts, key=label_counts.get)


####################################################################################################


"""
For the curious students, the following functions are used to visualize and compare the performance
of BinarySearchTree and AVLTree under extreme conditions. You do not need to modify (or run) these
functions, but you are welcome to play around with them if you wish.

You should know that AVLTree is faster than BinarySearchTree in the worst case, but how much faster?
The following functions will help you answer this question, shall you choose to try them out.

Uncomment the line under "if __name__ == '__main__':" to run the performance comparison (after completing
the rest of the project) and you will be greeted with a plot of the results. The function will require
matplotlib, make sure to install it if you do not have it already.
"""


def compare_times(structure: dict, sizes: List[int], trial: int) -> dict:
    """
    Comparing time on provide data structures in the worst case of BST tree
    :param structure: provided data structures
    :param sizes: size of test input
    :param trial: number of trials to test
    :return: dict with list of average times per input size for each algorithm
    """
    import sys
    import time
    result = {}
    sys.stdout.write('\r')
    sys.stdout.write('Start...\n')
    total = len(sizes) * len(structure)
    count = 0
    for algorithm, value in structure.items():
        ImplementedTree = value
        if algorithm not in result:
            result[algorithm] = []
        for size in sizes:
            sum_times = 0
            for _ in range(trial):
                tree = ImplementedTree()
                start = time.perf_counter()
                for i in range(size):
                    tree.insert(tree.origin, i)
                for i in range(size, -1, -1):
                    tree.remove(tree.origin, i)
                end = time.perf_counter()
                sum_times += (end - start)
            count += 1
            result[algorithm].append(sum_times / trial)
            sys.stdout.write("[{:<20s}] {:d}%\n".format('=' * ((count * 20) // total),
                                                        count * 100 // total))
            sys.stdout.flush()
    return result


def plot_time_comparison():
    """
    Use compare_times to make a time comparison of normal binary search tree and AVL tree
    in a worst case scenario.
    Requires matplotlib. Comment this out if you do not wish to install matplotlib.
    """
    import matplotlib.pyplot as plt
    import sys
    sys.setrecursionlimit(2010)
    structures = {
        "bst": BinarySearchTree,
        "avl": AVLTree
    }
    sizes = [4, 5, 6, 7, 8, 9, 10, 25, 50, 100, 300, 500, 1000, 2000]
    trials = 5
    data = compare_times(structures, sizes, trials)

    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(12, 8))

    for structure in structures:
        plt.plot(sizes, data[structure], label=structure)
    plt.legend()
    plt.xlabel("Input Size")
    plt.ylabel("Time to Sort (sec)")
    plt.title("BST vs AVL")
    plt.show()


_SVG_XML_TEMPLATE = """
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {{
        font: 300 16px monospace;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }}
    .dict {{
        font: 300 16px monospace;
        dominant-baseline: middle;
    }}
    .node {{
        fill: lightgray;
        stroke-width: 1;
    }}
</style>
<g stroke="#000000">
{body}
</g>
</svg>
"""

_NNC_DICT_BOX_TEXT_TEMPLATE = """<text class="dict" y="{y}" xml:space="preserve">
    <tspan x="{label_x}" dy="1.2em">{label}</tspan>
    <tspan x="{bracket_x}" dy="1.2em">{{</tspan>
    {values}
    <tspan x="{bracket_x}" dy="1.2em">}}</tspan>
</text>
"""


def pretty_print_binary_tree(root: Node, curr_index: int, include_index: bool = False,
                             delimiter: str = "-", ) -> \
        Tuple[List[str], int, int, int]:
    """
    Taken from: https://github.com/joowani/binarytree

    Recursively walk down the binary tree and build a pretty-print string.
    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.
    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: Level-order_ index of the current node (root node is 0).
    :type curr_index: int
    :param include_index: If set to True, include the level-order_ node indexes using
        the following format: ``{index}{delimiter}{value}`` (default: False).
    :type include_index: bool
    :param delimiter: Delimiter character between the node index and the node
        value (default: '-').
    :type delimiter:
    :return: Box of characters visually representing the current subtree, width
        of the box, and start-end positions of the repr string of the new root
        node value.
    :rtype: ([str], int, int, int)
    .. _Level-order:
        https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if include_index:
        node_repr = "{}{}{}".format(curr_index, delimiter, root.value)
    else:
        if type(root.value) == AVLWrappedDictionary:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value.key) if root.parent else "None"}'
        else:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value) if root.parent else "None"}'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = pretty_print_binary_tree(
        root.left, 2 * curr_index + 1, include_index, delimiter
    )
    r_box, r_box_width, r_root_start, r_root_end = pretty_print_binary_tree(
        root.right, 2 * curr_index + 2, include_index, delimiter
    )

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(" " * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = " " * gap_size
    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def svg(root: Node, node_radius: int = 16, nnc_mode=False) -> str:
    """
    Taken from: https://github.com/joowani/binarytree

    Generate SVG XML.
    :param root: Generate SVG for tree rooted at root
    :param node_radius: Node radius in pixels (default: 16).
    :type node_radius: int
    :return: Raw SVG XML.
    :rtype: str
    """
    tree_height = root.height
    scale = node_radius * 3
    xml = deque()
    nodes_for_nnc_visualization: list[AVLWrappedDictionary] = []

    def scale_x(x: int, y: int) -> float:
        diff = tree_height - y
        x = 2 ** (diff + 1) * x + 2 ** diff - 1
        return 1 + node_radius + scale * x / 2

    def scale_y(y: int) -> float:
        return scale * (1 + y)

    def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
        xml.appendleft(
            '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                x1=scale_x(parent_x, parent_y),
                y1=scale_y(parent_y),
                x2=scale_x(node_x, node_y),
                y2=scale_y(node_y),
            )
        )

    def add_node(node_x: int, node_y: int, node: Node) -> None:
        x, y = scale_x(node_x, node_y), scale_y(node_y)
        xml.append(
            f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')

        if nnc_mode:
            nodes_for_nnc_visualization.append(node.value)
            xml.append(
                f'<text class="value" x="{x}" y="{y + 5}">key={node.value.key}</text>')
        else:
            xml.append(
                f'<text class="value" x="{x}" y="{y + 5}">{node.value}</text>')

    current_nodes = [root.left, root.right]
    has_more_nodes = True
    y = 1

    add_node(0, 0, root)

    while has_more_nodes:

        has_more_nodes = False
        next_nodes: List[Node] = []

        for x, node in enumerate(current_nodes):
            if node is None:
                next_nodes.append(None)
                next_nodes.append(None)
            else:
                if node.left is not None or node.right is not None:
                    has_more_nodes = True

                add_edge(x // 2, y - 1, x, y)
                add_node(x, y, node)

                next_nodes.append(node.left)
                next_nodes.append(node.right)

        current_nodes = next_nodes
        y += 1

    svg_width = scale * (2 ** tree_height)
    svg_height = scale * (2 + tree_height)
    if nnc_mode:

        line_height = 20
        box_spacing = 10
        box_margin = 5
        character_width = 10

        max_key_count = max(
            map(lambda obj: len(obj.dictionary), nodes_for_nnc_visualization))
        box_height = (max_key_count + 3) * line_height + box_margin

        def max_length_item_of_node_dict(node: AVLWrappedDictionary):
            # Check if dict is empty so max doesn't throw exception
            if len(node.dictionary) > 0:
                item_lengths = map(lambda pair: len(
                    str(pair)), node.dictionary.items())
                return max(item_lengths)
            return 0

        max_value_length = max(
            map(max_length_item_of_node_dict, nodes_for_nnc_visualization))
        box_width = max(max_value_length * character_width, 110)

        boxes_per_row = svg_width // box_width
        rows_needed = math.ceil(
            len(nodes_for_nnc_visualization) / boxes_per_row)

        nodes_for_nnc_visualization.sort(key=lambda node: node.key)
        for index, node in enumerate(nodes_for_nnc_visualization):
            curr_row = index // boxes_per_row
            curr_column = index % boxes_per_row

            box_x = curr_column * (box_width + box_spacing)
            box_y = curr_row * (box_height + box_spacing) + svg_height
            box = f'<rect x="{box_x}" y="{box_y}" width="{box_width}" ' \
                  f'height="{box_height}" fill="white" />'
            xml.append(box)

            value_template = '<tspan x="{value_x}" dy="1.2em">{key}: {value}</tspan>'
            text_x = box_x + 10

            def item_pair_to_svg(pair):
                return value_template.format(key=pair[0], value=pair[1], value_x=text_x + 10)

            values = map(item_pair_to_svg, node.dictionary.items())
            text = _NNC_DICT_BOX_TEXT_TEMPLATE.format(
                y=box_y,
                label=f"key = {node.key}",
                label_x=text_x,
                bracket_x=text_x,
                values='\n'.join(values)
            )
            xml.append(text)

        svg_width = boxes_per_row * (box_width + box_spacing * 2)
        svg_height += rows_needed * (box_height + box_spacing * 2)

    return _SVG_XML_TEMPLATE.format(
        width=svg_width,
        height=svg_height,
        body="\n".join(xml),
    )


if __name__ == "__main__":
    # plot_time_comparison()
    pass
