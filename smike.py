s = float(input("Tritte 1? "))
t = float(input("Zeit 1? "))
f = float(s / t * 60)

s2 = float(input("Tritte 2? "))
t2 = float(input("Zeit 2? "))
f2 = float(s2 / t2 * 60)

s3 = float(input("Tritte 3? "))
t3 = float(input("Zeit 3? "))
f3 = float(s3 / t3 * 60)


for i in range(f-10, f+10):
    if f2 == f:
        for i in range(f-10, f+10):
            if f3 == f:
                print("Musik wird abgespielt")
                break
            else:
                print("Keine Überstimmung")
                break
    else:
        print("Keine Überstimmung")
        break
        
