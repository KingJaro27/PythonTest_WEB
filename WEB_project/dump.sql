BEGIN TRANSACTION;
CREATE TABLE tasks (
	id INTEGER NOT NULL, 
	title VARCHAR(120) NOT NULL, 
	description TEXT NOT NULL, 
	difficulty VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "tasks" VALUES(1,'Sum Two Numbers','Write a function that takes two numbers from input and returns their sum.','Easy');
INSERT INTO "tasks" VALUES(2,'Even or Odd','Write a function that takes a number and returns ''Even'' if the number is even, ''Odd'' otherwise.','Easy');
INSERT INTO "tasks" VALUES(3,'Reverse String','Write a function that reverses a string.','Easy');
INSERT INTO "tasks" VALUES(4,'Count Vowels','Write a function that counts the number of vowels in a string (a, e, i, o, u).','Easy');
INSERT INTO "tasks" VALUES(5,'Find Maximum','Write a function that takes three numbers and returns the largest one.','Easy');
INSERT INTO "tasks" VALUES(6,'Calculate Average','Write a function that calculates the average of a list of numbers.','Easy');
INSERT INTO "tasks" VALUES(7,'Factorial Calculator','Write a function that calculates the factorial of a number.','Medium');
INSERT INTO "tasks" VALUES(8,'Prime Number Checker','Write a function that checks if a number is prime.','Medium');
INSERT INTO "tasks" VALUES(9,'Fibonacci Sequence','Write a function that returns the nth Fibonacci number.','Medium');
INSERT INTO "tasks" VALUES(10,'Palindrome Checker','Write a function that checks if a string is a palindrome (reads the same backward as forward).','Medium');
INSERT INTO "tasks" VALUES(11,'Anagram Checker','Write a function that checks if two strings are anagrams of each other.','Medium');
INSERT INTO "tasks" VALUES(12,'List Intersection','Write a function that returns the intersection of two lists (common elements).','Medium');
INSERT INTO "tasks" VALUES(13,'Binary Search','Implement the binary search algorithm to find an element in a sorted list.','Hard');
INSERT INTO "tasks" VALUES(14,'Merge Two Sorted Lists','Write a function that merges two sorted lists into one sorted list.','Hard');
INSERT INTO "tasks" VALUES(15,'Valid Parentheses','Write a function that checks if a string of parentheses is balanced.','Hard');
INSERT INTO "tasks" VALUES(16,'Longest Substring Without Repeating Characters','Find the length of the longest substring without repeating characters.','Hard');
INSERT INTO "tasks" VALUES(17,'Matrix Rotation','Rotate an N x N matrix 90 degrees clockwise.','Hard');
INSERT INTO "tasks" VALUES(18,'Word Break','Given a string and a dictionary of words, determine if the string can be segmented into space-separated words from the dictionary.','Hard');
INSERT INTO "tasks" VALUES(19,'Quantum Algorithm Simulator','Implement a quantum gate simulator that can handle Hadamard and CNOT gates. Minimum 50 lines of code required.','Beserk');
INSERT INTO "tasks" VALUES(20,'Blockchain Miner','Implement a proof-of-work blockchain miner with SHA-256 hashing. Minimum 60 lines of code required.','Beserk');
INSERT INTO "tasks" VALUES(21,'Neural Network Framework','Create a neural network from scratch with backpropagation. Minimum 70 lines of code required.','Beserk');
CREATE TABLE test_cases (
	id INTEGER NOT NULL, 
	task_id INTEGER NOT NULL, 
	input TEXT NOT NULL, 
	output TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(task_id) REFERENCES tasks (id)
);
INSERT INTO "test_cases" VALUES(1,1,'2, 3','5');
INSERT INTO "test_cases" VALUES(2,1,'10, -5','5');
INSERT INTO "test_cases" VALUES(3,2,'4','Even');
INSERT INTO "test_cases" VALUES(4,2,'7','Odd');
INSERT INTO "test_cases" VALUES(5,2,'0','Even');
INSERT INTO "test_cases" VALUES(6,3,'''hello''','olleh');
INSERT INTO "test_cases" VALUES(7,3,'''Python''','nohtyP');
INSERT INTO "test_cases" VALUES(8,3,'''''','');
INSERT INTO "test_cases" VALUES(9,4,'''hello''','2');
INSERT INTO "test_cases" VALUES(10,4,'''Python is awesome''','6');
INSERT INTO "test_cases" VALUES(11,4,'''xyz''','0');
INSERT INTO "test_cases" VALUES(12,5,'1, 2, 3','3');
INSERT INTO "test_cases" VALUES(13,5,'-5, -1, -10','-1');
INSERT INTO "test_cases" VALUES(14,5,'0, 0, 0','0');
INSERT INTO "test_cases" VALUES(15,6,'[1, 2, 3, 4, 5]','3.0');
INSERT INTO "test_cases" VALUES(16,6,'[10, 20, 30]','20.0');
INSERT INTO "test_cases" VALUES(17,6,'[-1, 0, 1]','0.0');
INSERT INTO "test_cases" VALUES(18,7,'5','120');
INSERT INTO "test_cases" VALUES(19,7,'0','1');
INSERT INTO "test_cases" VALUES(20,7,'10','3628800');
INSERT INTO "test_cases" VALUES(21,8,'7','True');
INSERT INTO "test_cases" VALUES(22,8,'4','False');
INSERT INTO "test_cases" VALUES(23,8,'1','False');
INSERT INTO "test_cases" VALUES(24,9,'0','0');
INSERT INTO "test_cases" VALUES(25,9,'1','1');
INSERT INTO "test_cases" VALUES(26,9,'10','55');
INSERT INTO "test_cases" VALUES(27,10,'''racecar''','True');
INSERT INTO "test_cases" VALUES(28,10,'''hello''','False');
INSERT INTO "test_cases" VALUES(29,10,'''A man a plan a canal Panama''','True');
INSERT INTO "test_cases" VALUES(30,11,'''listen'', ''silent''','True');
INSERT INTO "test_cases" VALUES(31,11,'''hello'', ''world''','False');
INSERT INTO "test_cases" VALUES(32,11,'''Tom Marvolo Riddle'', ''I am Lord Voldemort''','True');
INSERT INTO "test_cases" VALUES(33,12,'[1, 2, 3], [2, 3, 4]','[2, 3]');
INSERT INTO "test_cases" VALUES(34,12,'[''a'', ''b'', ''c''], [''x'', ''y'', ''z'']','[]');
INSERT INTO "test_cases" VALUES(35,12,'[1, 1, 2, 3], [1, 1, 1, 4]','[1]');
INSERT INTO "test_cases" VALUES(36,13,'[1, 3, 5, 7, 9], 5','2');
INSERT INTO "test_cases" VALUES(37,13,'[1, 3, 5, 7, 9], 2','-1');
INSERT INTO "test_cases" VALUES(38,13,'[], 1','-1');
INSERT INTO "test_cases" VALUES(39,14,'[1, 3, 5], [2, 4, 6]','[1, 2, 3, 4, 5, 6]');
INSERT INTO "test_cases" VALUES(40,14,'[], [1, 2, 3]','[1, 2, 3]');
INSERT INTO "test_cases" VALUES(41,14,'[5, 6, 7], [1, 2, 3]','[1, 2, 3, 5, 6, 7]');
INSERT INTO "test_cases" VALUES(42,15,'''()[]{}''','True');
INSERT INTO "test_cases" VALUES(43,15,'''(]''','False');
INSERT INTO "test_cases" VALUES(44,15,'''([{}])''','True');
INSERT INTO "test_cases" VALUES(45,16,'''abcabcbb''','3');
INSERT INTO "test_cases" VALUES(46,16,'''bbbbb''','1');
INSERT INTO "test_cases" VALUES(47,16,'''pwwkew''','3');
INSERT INTO "test_cases" VALUES(48,17,'[[1,2,3],[4,5,6],[7,8,9]]','[[7, 4, 1], [8, 5, 2], [9, 6, 3]]');
INSERT INTO "test_cases" VALUES(49,17,'[[1]]','[[1]]');
INSERT INTO "test_cases" VALUES(50,17,'[[1,2],[3,4]]','[[3, 1], [4, 2]]');
INSERT INTO "test_cases" VALUES(51,18,'''leetcode'', [''leet'', ''code'']','True');
INSERT INTO "test_cases" VALUES(52,18,'''applepenapple'', [''apple'', ''pen'']','True');
INSERT INTO "test_cases" VALUES(53,18,'''catsandog'', [''cats'', ''dog'', ''sand'', ''and'', ''cat'']','False');
INSERT INTO "test_cases" VALUES(54,19,'H|0>','(0.70710678+0j)|0> + (0.70710678+0j)|1>');
INSERT INTO "test_cases" VALUES(55,19,'CNOT|10>','|11>');
INSERT INTO "test_cases" VALUES(56,20,'''Hello'' 3','Valid nonce found: 42');
INSERT INTO "test_cases" VALUES(57,20,'''Test'' 4','Valid nonce found: 1234');
INSERT INTO "test_cases" VALUES(58,21,'XOR_dataset','Accuracy > 85%');
INSERT INTO "test_cases" VALUES(59,21,'Linear_dataset','Accuracy > 90%');
CREATE TABLE user_progress (
	user_id INTEGER NOT NULL, 
	task_id INTEGER NOT NULL, 
	completed BOOLEAN, 
	completion_date DATETIME, 
	PRIMARY KEY (user_id, task_id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(task_id) REFERENCES tasks (id)
);
INSERT INTO "user_progress" VALUES(1,1,1,'2025-05-12 21:59:21.852166');
INSERT INTO "user_progress" VALUES(1,2,1,'2025-05-12 22:01:42.768168');
INSERT INTO "user_progress" VALUES(1,3,1,'2025-05-12 22:02:02.129121');
INSERT INTO "user_progress" VALUES(1,4,1,'2025-05-12 22:02:18.300631');
INSERT INTO "user_progress" VALUES(1,5,1,'2025-05-12 22:02:33.391661');
INSERT INTO "user_progress" VALUES(1,6,0,NULL);
INSERT INTO "user_progress" VALUES(1,7,1,'2025-05-12 22:02:50.169781');
INSERT INTO "user_progress" VALUES(1,8,1,'2025-05-12 22:03:12.657944');
INSERT INTO "user_progress" VALUES(1,9,0,NULL);
INSERT INTO "user_progress" VALUES(1,10,0,NULL);
INSERT INTO "user_progress" VALUES(1,11,0,NULL);
INSERT INTO "user_progress" VALUES(1,12,0,NULL);
INSERT INTO "user_progress" VALUES(1,13,1,'2025-05-12 22:03:40.880600');
INSERT INTO "user_progress" VALUES(1,14,1,'2025-05-12 22:03:56.449370');
INSERT INTO "user_progress" VALUES(1,15,1,'2025-05-12 22:04:11.737511');
INSERT INTO "user_progress" VALUES(1,16,0,NULL);
INSERT INTO "user_progress" VALUES(1,17,0,NULL);
INSERT INTO "user_progress" VALUES(1,18,0,NULL);
INSERT INTO "user_progress" VALUES(1,19,1,'2025-05-12 22:11:28.112380');
INSERT INTO "user_progress" VALUES(1,20,0,NULL);
INSERT INTO "user_progress" VALUES(1,21,0,NULL);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(120) NOT NULL, 
	email VARCHAR(120), 
	join_date DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO "users" VALUES(1,'KingJaro27','scrypt:32768:8:1$q51IqlFnm9i7We7L$1d258a47bd954bf0115a06cf191eb5bf5e2d29a07e70fec0f060b6e95f3c5db39800cac81c1ecea6a9c697aa32b5c57fcd18f6c6e1094d58cd3af9f721a1ead5','','2025-05-12 21:58:58.331484');
COMMIT;
