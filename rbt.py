"""
Red-Black Tree Implementation
Based on: Guibas & Sedgewick (1978) - "A Dichromatic Framework for Balanced Trees"

Red-Black Tree Properties:
1. Every node is RED or BLACK
2. Root is BLACK
3. Every leaf (NIL) is BLACK
4. If a node is RED, both children are BLACK
5. All paths from a node to descendant NILs have the same number of BLACK nodes
"""

RED = True
BLACK = False


class RBNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(None, None)
        self.NIL.color = BLACK
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.root = self.NIL
        self._size = 0
        self._operation_log = []

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self._log("rotate_left", x.key)

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self._log("rotate_right", x.key)

    def insert(self, key, value):
        node = RBNode(key, value)
        node.left = self.NIL
        node.right = self.NIL
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            elif node.key > current.key:
                current = current.right
            else:
                current.value = value
                self._log("update", key)
                return {"action": "update", "key": key, "value": value}
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._size += 1
        self._log("insert", key)
        self._insert_fixup(node)
        return {"action": "insert", "key": key, "value": value}

    def _insert_fixup(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                    self._log("recolor", z.key)
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                uncle = z.parent.parent.left
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                    self._log("recolor", z.key)
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def search(self, key):
        node = self._search_node(self.root, key)
        if node != self.NIL:
            self._log("search_found", key)
            return {"found": True, "key": key, "value": node.value}
        self._log("search_not_found", key)
        return {"found": False, "key": key, "value": None}

    def _search_node(self, node, key):
        if node == self.NIL or node.key == key:
            return node
        if key < node.key:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    def delete(self, key):
        z = self._search_node(self.root, key)
        if z == self.NIL:
            return {"action": "not_found", "key": key}
        self._delete_node(z)
        self._size -= 1
        self._log("delete", key)
        return {"action": "delete", "key": key}

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _log(self, action, key):
        self._operation_log.append({"action": action, "key": key})

    def clear_log(self):
        self._operation_log = []

    def size(self):
        return self._size

    def to_dict(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return None
        return {
            "key": node.key,
            "value": node.value,
            "color": "red" if node.color == RED else "black",
            "left": self.to_dict(node.left),
            "right": self.to_dict(node.right),
        }

    def all_keys(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node != self.NIL:
            self._inorder(node.left, result)
            result.append({"key": node.key, "value": node.value})
            self._inorder(node.right, result)

    def verify_black_height(self):
        def check(node):
            if node == self.NIL:
                return 1
            left_bh = check(node.left)
            right_bh = check(node.right)
            if left_bh == -1 or right_bh == -1:
                return -1
            if left_bh != right_bh:
                return -1
            return left_bh + (1 if node.color == BLACK else 0)
        bh = check(self.root)
        return bh != -1, max(bh, 0)

    def verify_red_property(self):
        def check(node):
            if node == self.NIL:
                return True
            if node.color == RED:
                if node.left.color == RED or node.right.color == RED:
                    return False
            return check(node.left) and check(node.right)
        return check(self.root)

    def full_verify(self):
        bh_valid, bh = self.verify_black_height()
        red_valid = self.verify_red_property()
        root_black = self.root == self.NIL or self.root.color == BLACK
        return {
            "valid": bh_valid and red_valid and root_black,
            "black_height": bh,
            "black_height_valid": bh_valid,
            "red_property_valid": red_valid,
            "root_is_black": root_black,
        }