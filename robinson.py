# Hàm phủ trả về logic phủ
def phu(x):
    tam = x.copy()
    if tam[0][0] == '-':
        tam[0] = tam[0][1:]
    else:
        tam[0] = '-' + tam[0]
    return tam

# Hàm đổi biến
def doibien(tap_vitu, tap_doi):
    tap_vitu_new = []
    for vitu in tap_vitu:
        vitu_new = [vitu[0], vitu[1][:]]
        for i in range(len(vitu[1])):
            for j in range(len(tap_doi)):
                if tap_doi[j][0] == vitu[1][i]:
                    vitu_new[1][i] = tap_doi[j][1]
        tap_vitu_new.append(vitu_new)
    return tap_vitu_new

# Hàm res trả về res(a, b)
def res(a, b, bien, giaTri):
    ans = []
    # Bước 1: Gộp a và b vào ans, loại bỏ trùng lặp
    for i in a:
        if i not in ans:
            ans.append(i)
    
    check = False
    for i in b:
        if i in ans:
            continue
        tam = phu(i)
        if tam in ans:
            ans.remove(tam)
            check = True
        else:
            ans.append(i)
            
    # Nếu tìm thấy cặp đối ngẫu ngay lập tức
    if check:
        return ans, None

    # Bước 2: Tìm khả năng hợp nhất (unification)
    tap_ketqua = []
    tap_doi = []
    vitu_chon = []

    # Chọn các vị từ có chứa giá trị cụ thể để ưu tiên
    for i in ans:
        for j in i[1]:
            if j in giaTri:
                vitu_chon.append(i)
                break
    
    # Duyệt để tìm cặp có thể hợp nhất
    for i in vitu_chon:
        hang_doi = []
        check = False
        # Kiểm tra xem có vị từ nào đối ngẫu về tên hàm không (ví dụ chame và -chame)
        for j in ans:
            if i[0] == '-' + j[0] or '-' + i[0] == j[0]:
                check = True
                # Kiểm tra độ dài tham số phải bằng nhau
                if len(i[1]) == len(j[1]):
                    for k in range(len(j[1])):
                        # Điều kiện để không thể hợp nhất: cả 2 đều là hằng hoặc biến nhưng khác nhau
                        if ((j[1][k] in giaTri and i[1][k] in giaTri) or \
                            (j[1][k] in bien and i[1][k] in bien)) and j[1][k] != i[1][k]:
                            check = False
                            break
            if check:
                hang_doi.append(j)

        # Xử lý hàng đợi để tạo phép thế
        for j in hang_doi:
            doi = []
            da_the = []
            valid_substitution = True # Biến kiểm tra xem phép thế có hợp lệ không
            
            for k in range(len(j[1])):
                # Trường hợp 1: i là hằng, j chưa là hằng và chưa được thế
                if i[1][k] in giaTri and j[1][k] not in giaTri and j[1][k] not in da_the:
                    doi.append([j[1][k], i[1][k]])
                    da_the.append(j[1][k])
                # Trường hợp 2: i chưa là hằng, j là hằng và i chưa được thế
                elif i[1][k] not in giaTri and j[1][k] in giaTri and i[1][k] not in da_the:
                    doi.append([i[1][k], j[1][k]])
                    da_the.append(i[1][k])
                # Trường hợp 3: Cả 2 đều là biến khác nhau (logic mở rộng thêm để code chặt chẽ hơn)
                elif i[1][k] in bien and j[1][k] in bien and i[1][k] != j[1][k]:
                     # Có thể thêm logic thế biến theo biến ở đây nếu cần, 
                     # nhưng theo slide thì tập trung vào thế hằng.
                     pass
            
            # Thực hiện đổi biến và gọi đệ quy
            if len(doi) > 0:
                a_new = doibien(a, doi)
                b_new = doibien(b, doi)
                tmp1, tmp2 = res(a_new, b_new, bien, giaTri)
                
                # Nếu là kết quả đơn (tmp2 is None), tmp1 là một clause list
                # Nếu là kết quả multiple (tmp2 is not None), tmp1 là một list of clause lists
                if tmp2 is None:
                    # Kết quả đơn - thêm tmp1 như một clause list
                    if tmp1 not in tap_ketqua:
                        tap_ketqua.append(tmp1)
                        tap_doi.append(doi)
                else:
                    # Kết quả multiple - extend và thêm tất cả substitutions tương ứng
                    for idx, result in enumerate(tmp1):
                        if result not in tap_ketqua:
                            tap_ketqua.append(result)
                            # Combine the current doi with the recursive doi
                            combined_doi = doi + tmp2[idx]
                            tap_doi.append(combined_doi)

    return tap_ketqua, tap_doi

# Hàm tạo chuỗi hiển thị logic vị từ
def tao_vitu(tap_vitu):
    tam = []
    for i in range(len(tap_vitu)):
        a = ','.join(tap_vitu[i][1])
        a = tap_vitu[i][0] + '(' + a + ')'
        tam.append(a)
    tam = ' v '.join(tam)
    return tam

# Hàm tạo chuỗi hiển thị phép thế
def tao_phepthe(doi):
    tam = doi.copy()
    tam2 = []
    for i in range(len(tam)):
        tam2.append('='.join(tam[i]))
    return ', '.join(tam2)

# Hàm robinson chính
def robinson(TAP, bien, giaTri):
    so = 1
    my_dict = {}
    
    # Khởi tạo các dòng ban đầu
    for vitu in TAP:
        my_dict[so] = vitu
        so += 1
        
    # In ra các dòng khởi tạo
    for key, val in my_dict.items():
        print("{:>3}. {}".format(key, tao_vitu(val)))
        
    da_duyet = set()
    i = 1
    
    while i < so:
        # Duyệt các dòng j từ i trở đi
        keys = list(my_dict.keys())
        # Tìm index của i trong keys để bắt đầu vòng lặp j
        start_idx = 0
        for idx, k in enumerate(keys):
            if k == i:
                start_idx = idx
                break
                
        for j in keys[start_idx:]:
            if (i, j) not in da_duyet:
                # Gọi hàm res
                dong_moi, tap_doi = res(my_dict[i], my_dict[j], bien, giaTri)
                da_duyet.add((i, j)) # Đánh dấu đã duyệt
                
                # Trường hợp 1: tap_doi là None (res trực tiếp thành công)
                if tap_doi is None:
                    if not dong_moi: # Nếu rỗng [] -> Chứng minh xong
                        print("{:>3}. Res({:>2}, {:>3}) = {}.".format(so, i, j, '[]'))
                        print("=> Điều phải chứng minh.")
                        return True
                    
                    if dong_moi not in my_dict.values():
                        print("{:>3}. Res({:>2}, {:>3}) = {}.".format(so, i, j, tao_vitu(dong_moi)))
                        my_dict[so] = dong_moi
                        # Cập nhật da_duyet để không res lại dòng cha với con vừa sinh ra ngay
                        da_duyet.add((i, so))
                        da_duyet.add((j, so))
                        so += 1
                        continue

                # Trường hợp 2: Có phép thế (trả về danh sách các khả năng)
                else:
                    for k in range(len(dong_moi)):
                        if not dong_moi[k]: # Nếu rỗng []
                             print("{:>3}. Res({:>2}, {:>3}) = {}. Thế ({})".format(
                                 so, i, j, '[]', tao_phepthe(tap_doi[k])))
                             print("=> Điều phải chứng minh.")
                             return True
                        
                        if dong_moi[k] not in my_dict.values():
                            print("{:>3}. Res({:>2}, {:>3}) = {}. Thế ({})".format(
                                so, i, j, tao_vitu(dong_moi[k]), tao_phepthe(tap_doi[k])))
                            my_dict[so] = dong_moi[k]
                            da_duyet.add((i, so))
                            da_duyet.add((j, so))
                            so += 1
        i += 1
    
    return False

# Hàm xử lý đầu vào
def xuLyDauVao(dong):
    dong = dong.replace('\n', '') # Xóa xuống dòng
    dong = dong + ','
    dong = dong.split('),')
    dong = [i + ')' for i in dong][:-1] # Loại bỏ phần tử rỗng cuối cùng
    
    ket_qua = []
    for i in range(len(dong)):
        vitu_str = dong[i].split(' v ') # Cắt theo dấu v
        logic_vitu = []
        for j in vitu_str:
            # Tách tên và biến: chame(x, y) -> ['chame', ['x', 'y']]
            part = j[:-1].split('(')
            ten = part[0].strip()
            cac_bien = part[1].split(',')
            cac_bien = [b.strip() for b in cac_bien]
            logic_vitu.append([ten, cac_bien])
        ket_qua.append(logic_vitu)
    return ket_qua

# --- MAIN ---
if __name__ == "__main__":
    # Dữ liệu đầu vào từ bài toán
    TAP_input = '-chame(x, y) v -chame(x, z) v anhem(y, z), \
                 -chame(x, y) v -chame(z, t) v -anhem(x, z) v anhem(y, t), \
                 -anhem(x, y) v anhem(y, x), \
                 chame(B, N), chame(T, D), chame(A, B), chame(A, T), -anhem(N, D)'
    
    bien = ['x', 'y', 'z', 't']
    giaTri = ['A', 'B', 'N', 'T', 'D']

    # Xử lý đầu vào
    TAP = xuLyDauVao(TAP_input)
    
    # Chạy thuật toán
    print("Bắt đầu giải thuật Robinson:")
    robinson(TAP, bien, giaTri)