

# 1

def odd_string_count(s):

    cache = {}
    if len(s) == 1:
        return cache

    i = 1
    while i<len(s):
        if s[i] in cache.keys():
            cache[s[i]] += 1

        else:
            cache[s[i]] = 1

        i+=2

    i = 0
    while i<len(s):
        if s[i] in cache.keys():
            cache[s[i]] += 1

        i+=2

    return cache


print(odd_string_count("bbabdloseckc"))




# 2

def find_second_min_max(a1, a2):

    a_combined = a1 + a2

    max_v = [0,0]
    min_v = [a_combined[0], a_combined[1]]

    for i in range(2,len(a_combined)):
        # check max
        if a_combined[i] > max_v[0] and max_v[0] <= max_v[1]:
            max_v[0] = a_combined[i]
            continue

        elif a_combined[i] > max_v[1] and max_v[1] < max_v[0]:
            max_v[1] = a_combined[i]
            continue

        if a_combined[i] < min_v[0] and min_v[0] >= min_v[1]:
            min_v[0] = a_combined[i]

        elif a_combined[i] < min_v[1] and min_v[1] > min_v[0]:
            min_v[1] = a_combined[i]

    return [min(max_v), max(min_v)]


print(find_second_min_max([10,5,7,2,4,1,24], [8,23,29,25,40,0,24]))





def find_palindromic_substring(s):

    i = 0
    j = len(s)
    iteration = 0

    while i < j-1:

        if is_palindrom(s[i:j]):
            palindrom = s[i:j]
            s_without = s[0:i]
            if j < len(s):
                s_without += s[j:]

            return {"palindrom" : palindrom, "start_idx" : i, "end_idx" : j, "palindrom_removed" : s_without}

        else:
            if iteration % 2 == 0:
                i +=1
            else:
                j -=1
            iteration += 1

    return {"palindrom" : "", "start_idx" : i, "end_idx" : len(s), "palindrom_removed" : s}




def is_palindrom(s):

    i = 0
    j = len(s)-1

    while i < j:
        if s[i] != s[j]:
            return False

        i+=1
        j-=1

    return True


print(find_palindromic_substring("eve"))
