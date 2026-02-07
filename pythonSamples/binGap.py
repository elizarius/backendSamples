def solution(N):
    binary = bin(N)[2:]  # Convert to binary, remove '0b'
    #gaps = binary.strip('0').split('1')
    gaps = binary.strip('0')
    print ('Aelz 1: ', gaps)
    gaps = gaps.split('1')
    print ('Aelz 2: ', gaps)
    #print (gaps)
    gap_len = 0
    if gaps:
        gap_len = max(len(gap) for gap in gaps)
    return gap_len

print(solution(9), '\n')  # Output: 2
print(solution(529), '\n')  # Output: 4