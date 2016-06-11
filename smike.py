s = float(input("Tritte 1? "))
t = float(input("Zeit 1? "))
f = int(s / t * 60)

s2 = float(input("Tritte 2? "))
t2 = float(input("Zeit 2? "))
f2 = int(s2 / t2 * 60)

s3 = float(input("Tritte 3? "))
t3 = float(input("Zeit 3? "))
f3 = int(s3 / t3 * 60)


for i in range(f-10, f+10):
    if f2 == i:
        print("Treffer 1 und 2")
        for i in range(f-10, f+10):
            if f3 == i:
                print("Treffer 1 und 3")
                break
            elif i == f + 10:
                print("Kein Treffer zwischen 1 und 3")
                break
    elif i == f + 9:
        print("Kein Treffer zwischen 1 und 2")
        break
        

        
