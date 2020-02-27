n = int(input())
array = input().split()
max = 1
for i in range(0 , n-1):
    number = 1
    ghabli = int(array[i])
    for j in range(i+1 , n):
        if int(array[j]) > int(ghabli):
            number+=1
            ghabli = int(array[j])
        else:
            break
    if max < number:
        max = number
print(max)





