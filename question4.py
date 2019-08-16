def sequence(s):
    s=str(s)
    leng_num = len(s)
    i=leng_num-1
    firststr = "" 
    for j in range(0,leng_num):
        if i!=0:
            firststr = firststr +  s[i] + "."
            print firststr[:-1]
            mid_str = firststr
            i=i-1
        else:
            firststr = firststr + s[i]+ "."
            for k in range(1,leng_num-1):
                firststr = firststr + s[k] + "."
            print firststr[:-1]
            for p in range(0, len(mid_str)):
                if len(mid_str) > 0 :
                    print mid_str[:-1]
                    mid_str = mid_str[:-2]
s= 8594011122
sequence(s)