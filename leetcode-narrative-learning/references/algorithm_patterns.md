# 算法模式库

常见 LeetCode 算法模式分类及代表题目,用于"举一反三"环节的题目推荐。

---

## 1. 哈希表 (Hash Table)

**核心思想**: 用空间换时间,快速查找

**适用场景**:
- 需要快速查找元素是否存在
- 需要记录元素出现的频率
- 需要建立映射关系

**代表题目**:
- [1] Two Sum (Easy)
- [454] 4Sum II (Medium)
- [49] Group Anagrams (Medium)
- [128] Longest Consecutive Sequence (Medium)
- [380] Insert Delete GetRandom O(1) (Medium)

---

## 2. 双指针 (Two Pointers)

**核心思想**: 用两个指针遍历,减少时间复杂度

### 2.1 对撞指针

**适用场景**:
- 有序数组查找
- 回文判断
- 区间问题

**代表题目**:
- [167] Two Sum II (Medium)
- [15] 3Sum (Medium)
- [11] Container With Most Water (Medium)
- [42] Trapping Rain Water (Hard)
- [125] Valid Palindrome (Easy)

### 2.2 快慢指针

**适用场景**:
- 链表环检测
- 寻找中点
- 删除倒数第N个节点

**代表题目**:
- [141] Linked List Cycle (Easy)
- [142] Linked List Cycle II (Medium)
- [876] Middle of the Linked List (Easy)
- [19] Remove Nth Node From End (Medium)
- [287] Find the Duplicate Number (Medium)

### 2.3 滑动窗口

**适用场景**:
- 子串/子数组问题
- 固定或可变窗口大小
- 最优解区间

**代表题目**:
- [3] Longest Substring Without Repeating Characters (Medium)
- [76] Minimum Window Substring (Hard)
- [438] Find All Anagrams in a String (Medium)
- [209] Minimum Size Subarray Sum (Medium)
- [567] Permutation in String (Medium)

---

## 3. 二分查找 (Binary Search)

**核心思想**: 在有序数据中快速定位

**适用场景**:
- 有序数组查找
- 寻找边界
- 最小化最大值/最大化最小值

**代表题目**:
- [704] Binary Search (Easy)
- [34] Find First and Last Position (Medium)
- [33] Search in Rotated Sorted Array (Medium)
- [153] Find Minimum in Rotated Sorted Array (Medium)
- [4] Median of Two Sorted Arrays (Hard)

---

## 4. 栈 (Stack)

**核心思想**: 后进先出,处理嵌套结构

**适用场景**:
- 括号匹配
- 单调栈问题
- 递归转迭代

**代表题目**:
- [20] Valid Parentheses (Easy)
- [84] Largest Rectangle in Histogram (Hard)
- [739] Daily Temperatures (Medium)
- [155] Min Stack (Medium)
- [32] Longest Valid Parentheses (Hard)

---

## 5. 队列 (Queue)

**核心思想**: 先进先出,处理顺序问题

**适用场景**:
- BFS 遍历
- 滑动窗口最大值
- 任务调度

**代表题目**:
- [102] Binary Tree Level Order Traversal (Medium)
- [239] Sliding Window Maximum (Hard)
- [622] Design Circular Queue (Medium)
- [933] Number of Recent Calls (Easy)
- [346] Moving Average from Data Stream (Easy)

---

## 6. 链表 (Linked List)

**核心思想**: 动态数据结构,插入删除高效

**适用场景**:
- 反转链表
- 合并链表
- 链表环问题

**代表题目**:
- [206] Reverse Linked List (Easy)
- [21] Merge Two Sorted Lists (Easy)
- [23] Merge k Sorted Lists (Hard)
- [2] Add Two Numbers (Medium)
- [25] Reverse Nodes in k-Group (Hard)

---

## 7. 树 (Tree)

### 7.1 二叉树遍历

**代表题目**:
- [94] Binary Tree Inorder Traversal (Easy)
- [144] Binary Tree Preorder Traversal (Easy)
- [145] Binary Tree Postorder Traversal (Easy)
- [102] Binary Tree Level Order Traversal (Medium)
- [103] Binary Tree Zigzag Level Order Traversal (Medium)

### 7.2 二叉搜索树 (BST)

**代表题目**:
- [98] Validate Binary Search Tree (Medium)
- [230] Kth Smallest Element in a BST (Medium)
- [235] Lowest Common Ancestor of a BST (Medium)
- [108] Convert Sorted Array to Binary Search Tree (Easy)
- [450] Delete Node in a BST (Medium)

### 7.3 树的递归

**代表题目**:
- [104] Maximum Depth of Binary Tree (Easy)
- [226] Invert Binary Tree (Easy)
- [112] Path Sum (Easy)
- [543] Diameter of Binary Tree (Easy)
- [124] Binary Tree Maximum Path Sum (Hard)

---

## 8. 图 (Graph)

### 8.1 DFS

**代表题目**:
- [200] Number of Islands (Medium)
- [133] Clone Graph (Medium)
- [79] Word Search (Medium)
- [417] Pacific Atlantic Water Flow (Medium)
- [207] Course Schedule (Medium)

### 8.2 BFS

**代表题目**:
- [102] Binary Tree Level Order Traversal (Medium)
- [127] Word Ladder (Hard)
- [433] Minimum Genetic Mutation (Medium)
- [542] 01 Matrix (Medium)
- [994] Rotting Oranges (Medium)

### 8.3 拓扑排序

**代表题目**:
- [207] Course Schedule (Medium)
- [210] Course Schedule II (Medium)
- [269] Alien Dictionary (Hard)
- [310] Minimum Height Trees (Medium)

---

## 9. 动态规划 (Dynamic Programming)

### 9.1 一维 DP

**代表题目**:
- [70] Climbing Stairs (Easy)
- [198] House Robber (Medium)
- [300] Longest Increasing Subsequence (Medium)
- [139] Word Break (Medium)
- [152] Maximum Product Subarray (Medium)

### 9.2 二维 DP

**代表题目**:
- [64] Minimum Path Sum (Medium)
- [72] Edit Distance (Hard)
- [10] Regular Expression Matching (Hard)
- [97] Interleaving String (Medium)
- [115] Distinct Subsequences (Hard)

### 9.3 背包问题

**代表题目**:
- [416] Partition Equal Subset Sum (Medium)
- [322] Coin Change (Medium)
- [518] Coin Change 2 (Medium)
- [474] Ones and Zeroes (Medium)

---

## 10. 回溯 (Backtracking)

**核心思想**: 穷举所有可能,剪枝优化

**适用场景**:
- 排列组合问题
- 棋盘问题
- 子集问题

**代表题目**:
- [46] Permutations (Medium)
- [78] Subsets (Medium)
- [39] Combination Sum (Medium)
- [51] N-Queens (Hard)
- [79] Word Search (Medium)

---

## 11. 贪心 (Greedy)

**核心思想**: 每步选择局部最优,期待全局最优

**适用场景**:
- 区间调度
- 最小生成树
- 霍夫曼编码

**代表题目**:
- [55] Jump Game (Medium)
- [45] Jump Game II (Medium)
- [763] Partition Labels (Medium)
- [134] Gas Station (Medium)
- [435] Non-overlapping Intervals (Medium)

---

## 12. 分治 (Divide and Conquer)

**核心思想**: 分解问题,递归求解,合并结果

**代表题目**:
- [23] Merge k Sorted Lists (Hard)
- [53] Maximum Subarray (Medium)
- [215] Kth Largest Element in an Array (Medium)
- [912] Sort an Array (Medium)
- [169] Majority Element (Easy)

---

## 13. 位运算 (Bit Manipulation)

**核心思想**: 利用位运算的特性

**代表题目**:
- [136] Single Number (Easy)
- [191] Number of 1 Bits (Easy)
- [338] Counting Bits (Easy)
- [260] Single Number III (Medium)
- [201] Bitwise AND of Numbers Range (Medium)

---

## 14. 数学 (Math)

**代表题目**:
- [204] Count Primes (Medium)
- [172] Factorial Trailing Zeroes (Medium)
- [50] Pow(x, n) (Medium)
- [29] Divide Two Integers (Medium)
- [149] Max Points on a Line (Hard)

---

## 使用指南

在生成"举一反三"页面时:

1. **识别题目所属模式**
2. **从该模式中选择 5 道题**:
   - 1 道更简单 (巩固基础)
   - 2 道同难度 (横向拓展)
   - 2 道更难 (进阶挑战)
3. **说明题目与当前题的联系** (共享什么核心思想)
4. **按难度递增排列**

示例:
```
当前题: Two Sum (Easy, 哈希表)

推荐:
1. Contains Duplicate (Easy) - 哈希表基础应用
2. 4Sum II (Medium) - 哈希表空间换时间的进阶
3. Group Anagrams (Medium) - 哈希表构建映射关系
4. Longest Consecutive Sequence (Medium) - 哈希表 + 去重优化
5. Substring with Concatenation (Hard) - 哈希表 + 滑动窗口结合
```
