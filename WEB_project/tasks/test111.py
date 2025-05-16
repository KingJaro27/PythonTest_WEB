#Sum Two Numbers

a, b = map(int, input().split())
print(a + b)

#Even or Odd

num = int(input())
print("Even" if num % 2 == 0 else "Odd")

#Reverse String

s = input().strip()
print(s[::-1])

#Count Vowels

s = input()
vowels = 'aeiouAEIOU'
print(sum(1 for char in s if char in vowels))

#Find Maximum

nums = list(map(int, input().split()))
print(max(nums))

#Calculate avarage

nums = eval(input())
print(sum(nums)/len(nums))

#count vowels

s = input().strip()
print(len(s.split()) if s else 0)

#find min number

nums = eval(input())
print(min(nums))

#check palindrome

num = input().strip()
print(num == num[::-1])

#Factorial Calculator

def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)
print(factorial(int(input())))

#Prime Number Checker

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
print(is_prime(int(input())))



#fibonachi

n = int(input())
a, b = 0, 1
for _ in range(n):
    a, b = b, a + b
print(a)

#palindrome

s = ''.join(c.lower() for c in input() if c.isalnum())
print(s == s[::-1])

#anagram


s1, s2 = input().split(', ')
print(sorted(s1.lower().replace(' ', '')) == sorted(s2.lower().replace(' ', '')))

#list intersection

l1, l2 = eval(input())
print([x for x in set(l1) if x in set(l2)])

# roman

s = input().strip()
roman = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
total = 0
prev = 0
for c in s[::-1]:
    curr = roman[c]
    total += curr if curr >= prev else -curr
    prev = curr
print(total)

#group anagram

from collections import defaultdict
strs = eval(input())
anagrams = defaultdict(list)
for s in strs:
    key = ''.join(sorted(s))
    anagrams[key].append(s)
print(list(anagrams.values()))

#binary tree

from collections import deque
tree = eval(input())

q = deque([0])
result = []

while q:
    level_size = len(q)
    level = []
    for _ in range(level_size):
        idx = q.popleft()
        if idx < len(tree) and tree[idx] is not None:
            level.append(tree[idx])
            left = 2*idx + 1
            right = 2*idx + 2
            if left < len(tree):
                q.append(left)
            if right < len(tree):
                q.append(right)
    if level:
        result.append(level)
print(result)

#Binary Search

def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

import ast
arr, target = ast.literal_eval(input())
print(binary_search(arr, target))

#Merge Two Sorted Lists

def merge_lists(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result

import ast
list1, list2 = ast.literal_eval(input())
print(merge_lists(list1, list2))

#Valid Parentheses

def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or mapping[char] != stack.pop():
                return False
        else:
            continue
    return not stack

s = input()
print(is_valid(s))

#longest sub

s = input().strip()
char_set = set()
left = max_len = 0
for right in range(len(s)):
    while s[right] in char_set:
        char_set.remove(s[left])
        left += 1
    char_set.add(s[right])
    max_len = max(max_len, right - left + 1)
print(max_len)

#matrix rotation

matrix = eval(input())
n = len(matrix)
for i in range(n//2):
    for j in range(i, n-i-1):
        temp = matrix[i][j]
        matrix[i][j] = matrix[n-1-j][i]
        matrix[n-1-j][i] = matrix[n-1-i][n-1-j]
        matrix[n-1-i][n-1-j] = matrix[j][n-1-i]
        matrix[j][n-1-i] = temp
print(matrix)

#word break

import sys
from collections import defaultdict

input_str = sys.stdin.read().strip()
s, word_dict_str = input_str.split(", ", 1)
s = s.strip("\"'")
word_dict = []
in_word = False
current_word = []
for char in word_dict_str.strip("[]"):
    if char == "'":
        if in_word:
            word_dict.append("".join(current_word))
            current_word = []
        in_word = not in_word
    elif in_word:
        current_word.append(char)

word_set = set(word_dict)
n = len(s)

dp = [False] * (n + 1)
dp[0] = True
for i in range(1, n + 1):
    for j in range(i):
        if dp[j] and s[j:i] in word_set:
            dp[i] = True
            break

print(dp[n])



#matrix sum

import sys
n = int(sys.stdin.readline())
matrix = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
total = 0
for i in range(n):
    total += matrix[i][i] 
    total += matrix[i][n-1-i]
if n % 2 == 1:
    total -= matrix[n//2][n//2]
print(total)

#count words

import sys
from collections import defaultdict
n = int(sys.stdin.readline())
freq = defaultdict(int)
for _ in range(n):
    line = sys.stdin.readline().lower()
    for word in line.split():
        freq[word] += 1
for word, count in freq.items():
    print(f"{word}: {count}")
    
#binary converter

import sys
data = sys.stdin.read().split()
n = int(data[0])
nums = list(map(int, data[1:n+1]))
binary_str = ''.join(bin(num)[2:] for num in nums)
print(binary_str.count('1'))

#unipue difference

import sys
nums = [int(sys.stdin.readline()) for _ in range(int(sys.stdin.readline()))]
diffs = set()
for i in nums:
    for j in nums:
        diffs.add(i - j)
for d in sorted(diffs):
    print(d)
    
#fraction

import sys
from math import gcd
data = list(map(int, sys.stdin.read().split()))
n = data[0]
total_num = 0
total_den = 1

for i in range(n):
    num = data[2*i+1]
    den = data[2*i+2]
    total_num = total_num * den + num * total_den
    total_den *= den
    common = gcd(total_num, total_den)
    total_num //= common
    total_den //= common

print(f"{total_num}/{total_den}")

# prime generator

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

a, b = map(int, input().split())
primes = [str(i) for i in range(a, b+1) if is_prime(i)]
print(' '.join(primes))


#rain dropper

height = eval(input())
left, right = 0, len(height) - 1
left_max = right_max = water = 0
while left < right:
    if height[left] < height[right]:
        left_max = max(left_max, height[left])
        water += left_max - height[left]
        left += 1
    else:
        right_max = max(right_max, height[right])
        water += right_max - height[right]
        right -= 1
print(water)

#window max

from collections import deque
nums, k = eval(input())
q = deque()
result = []
for i, num in enumerate(nums):
    while q and nums[q[-1]] < num:
        q.pop()
    q.append(i)
    if q[0] == i - k:
        q.popleft()
    if i >= k - 1:
        result.append(nums[q[0]])
print(result)

#min window

def solve():
    import sys
    from collections import defaultdict
    
    # Read input and parse the two strings
    input_str = sys.stdin.read().strip()
    if not input_str:
        print("")
        return
    
    # Split the input into s and t
    parts = input_str.split(', ')
    if len(parts) != 2:
        print("")
        return
    
    s = parts[0].strip("'\"")
    t = parts[1].strip("'\"")
    
    if not t or not s:
        print("")
        return
    
    dict_t = defaultdict(int)
    for char in t:
        dict_t[char] += 1
    
    required = len(dict_t)
    l, r = 0, 0
    formed = 0
    window_counts = defaultdict(int)
    ans = (float("inf"), None, None)
    
    while r < len(s):
        character = s[r]
        window_counts[character] += 1
        
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1
        
        while l <= r and formed == required:
            character = s[l]
            
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1
            
            l += 1
        
        r += 1
    
    print("" if ans[0] == float("inf") else s[ans[1]:ans[2]+1])

solve()