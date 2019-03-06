ar = [0]*26
for v in [1,-1]:
	s = input()
	for i in range(0,len(s)):
		if s[i] == '(':
			v *= -1
		elif s[i] == ':':
			v *= -2
		elif s[i] == ')':
			v //= 2
		else:
			ar[ord(s[i])-ord('A')] += v
print(all(x == 0 for x in ar))	
