# Tạo một ds rỗng để lưu KQ
j=[]
# Duyệt qua All các số trong đoạn từ 2000 -> 3200, kt xem số i chia hết cho 7 và kh phải là bội của 5 không
for i in range(2000 , 3200):
    if (i % 7 == 0) and (i % 5 != 0):
        j.append(str(i))
print (','.join(j))