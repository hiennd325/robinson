# Hàm phủ trả về logic phủ
# Trong logic vị từ, phủ của một vị từ là vị từ đó với dấu ngược lại
# Ví dụ: phủ của chame(x, y) là -chame(x, y) và ngược lại
def phu(x):
    tam = x.copy()
    # Nếu vị từ đã có dấu phủ (bắt đầu bằng '-'), bỏ dấu phủ đi
    if tam[0][0] == '-':
        tam[0] = tam[0][1:]
    # Nếu vị từ chưa có dấu phủ, thêm dấu phủ vào
    else:
        tam[0] = '-' + tam[0]
    return tam

# Hàm đổi biến
# Thay thế các biến trong danh sách vị từ theo một phép thế (substitution)
# Ví dụ: nếu có phép thế {x/A, y/B} thì vị từ chame(x, y) sẽ trở thành chame(A, B)
# tap_vitu: danh sách các vị từ cần thay thế
# tap_doi: danh sách các cặp đổi dạng [biến, giá trị] ví dụ [['x', 'A'], ['y', 'B']]
def doibien(tap_vitu, tap_doi):
    tap_vitu_new = []
    # Duyệt qua từng vị từ trong danh sách
    for vitu in tap_vitu:
        # Tạo bản sao của vị từ để không làm thay đổi vị từ gốc
        vitu_new = [vitu[0], vitu[1][:]]
        # Duyệt qua từng tham số của vị từ
        for i in range(len(vitu[1])):
            # Kiểm tra xem tham số này có trong phép thế không
            for j in range(len(tap_doi)):
                # Nếu tham số trùng với biến trong phép thế, thay thế bằng giá trị tương ứng
                if tap_doi[j][0] == vitu[1][i]:
                    vitu_new[1][i] = tap_doi[j][1]
        tap_vitu_new.append(vitu_new)
    return tap_vitu_new

# Hàm res trả về res(a, b)
# Thực hiện phép hợp giải (resolution) giữa hai mệnh đề a và b
# Trả về kết quả hợp giải và phép thế (nếu có)
# a, b: hai mệnh đề cần hợp giải
# bien: danh sách các biến
# giaTri: danh sách các hằng
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
            # Nếu tìm thấy cặp đối ngẫu (một vị từ và phủ của nó), loại bỏ khỏi kết quả
            ans.remove(tam)
            check = True
        else:
            ans.append(i)
            
    # Nếu tìm thấy cặp đối ngẫu ngay lập tức, trả về kết quả đơn
    if check:
        return ans, None

    # Bước 2: Tìm khả năng hợp nhất (unification) - khi cần phép thế để hợp giải
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
            # Kiểm tra xem hai vị từ có phải là phủ của nhau không
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
# Chuyển đổi danh sách vị từ thành chuỗi để hiển thị
# Ví dụ: [['chame', ['x', 'y']], ['-anhem', ['y', 'z']]] -> "chame(x,y) v -anhem(y,z)"
def tao_vitu(tap_vitu):
    tam = []
    for i in range(len(tap_vitu)):
        # Nối các tham số bằng dấu phẩy
        a = ','.join(tap_vitu[i][1])
        # Tạo chuỗi vị từ theo định dạng ten_vitri(tham_so1,tham_so2,...)
        a = tap_vitu[i][0] + '(' + a + ')'
        tam.append(a)
    # Nối các vị từ bằng dấu "v" (hoặc)
    tam = ' v '.join(tam)
    return tam

# Hàm tạo chuỗi hiển thị phép thế
# Chuyển đổi danh sách phép thế thành chuỗi để hiển thị
# Ví dụ: [['x', 'A'], ['y', 'B']] -> "x=A, y=B"
def tao_phepthe(doi):
    tam = doi.copy()
    tam2 = []
    for i in range(len(tam)):
        # Nối mỗi cặp phép thế bằng dấu "="
        tam2.append('='.join(tam[i]))
    # Nối các phép thế bằng dấu ", "
    return ', '.join(tam2)

# Hàm robinson chính
# Thực hiện thuật toán Robinson để chứng minh mệnh đề
# TAP: Danh sách các mệnh đề (clauses)
# bien: Danh sách các biến
# giaTri: Danh sách các hằng
def robinson(TAP, bien, giaTri):
    so = 1
    my_dict = {}
    
    # Khởi tạo các dòng ban đầu - đánh số thứ tự cho từng mệnh đề
    for vitu in TAP:
        my_dict[so] = vitu
        so += 1
        
    # In ra các dòng khởi tạo để người dùng theo dõi
    for key, val in my_dict.items():
        print("{:>3}. {}".format(key, tao_vitu(val)))
        
    # Tập hợp lưu các cặp đã duyệt để tránh duyệt lại
    da_duyet = set()
    i = 1
    
    # Vòng lặp chính của thuật toán
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
            # Chỉ xét các cặp chưa được duyệt
            if (i, j) not in da_duyet:
                # Gọi hàm res để thực hiện hợp giải giữa hai mệnh đề
                dong_moi, tap_doi = res(my_dict[i], my_dict[j], bien, giaTri)
                da_duyet.add((i, j)) # Đánh dấu đã duyệt
                
                # Trường hợp 1: tap_doi là None (res trực tiếp thành công mà không cần phép thế)
                if tap_doi is None:
                    # Nếu kết quả là rỗng [] -> Mâu thuẫn -> Chứng minh xong
                    if not dong_moi:
                        print("{:>3}. Res({:>2}, {:>3}) = {}.".format(so, i, j, '[]'))
                        print("=> Điều phải chứng minh.")
                        return True
                    
                    # Nếu kết quả chưa có trong từ điển, thêm vào
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
                        # Nếu kết quả là rỗng [] -> Mâu thuẫn -> Chứng minh xong
                        if not dong_moi[k]:
                             print("{:>3}. Res({:>2}, {:>3}) = {}. Thế ({})".format(
                                 so, i, j, '[]', tao_phepthe(tap_doi[k])))
                             print("=> Điều phải chứng minh.")
                             return True
                        
                        # Nếu kết quả chưa có trong từ điển, thêm vào
                        if dong_moi[k] not in my_dict.values():
                            print("{:>3}. Res({:>2}, {:>3}) = {}. Thế ({})".format(
                                so, i, j, tao_vitu(dong_moi[k]), tao_phepthe(tap_doi[k])))
                            my_dict[so] = dong_moi[k]
                            da_duyet.add((i, so))
                            da_duyet.add((j, so))
                            so += 1
        i += 1
    
    # Nếu duyệt hết mà không tìm được mâu thuẫn -> Không chứng minh được
    return False

# Hàm xử lý đầu vào
# Chuyển đổi chuỗi đầu vào thành dạng danh sách vị từ
# Ví dụ: "-chame(x, y) v -chame(x, z) v anhem(y, z)" 
# -> [[['-chame', ['x', 'y']], ['-chame', ['x', 'z']], ['anhem', ['y', 'z']]]]
def xuLyDauVao(dong):
    dong = dong.replace('\n', '') # Xóa xuống dòng
    dong = dong + ','  # Thêm dấu phẩy cuối cùng để xử lý dễ dàng
    # Tách theo '),'
    dong = dong.split('),')
    # Thêm lại dấu ')' cho các phần tử và loại bỏ phần tử rỗng cuối cùng
    dong = [i + ')' for i in dong][:-1]
    
    ket_qua = []
    # Duyệt qua từng mệnh đề
    for i in range(len(dong)):
        # Tách theo dấu ' v ' để lấy từng vị từ
        vitu_str = dong[i].split(' v ')
        logic_vitu = []
        # Xử lý từng vị từ
        for j in vitu_str:
            # Tách tên vị từ và các tham số: chame(x, y) -> ['chame', ['x', 'y']]
            part = j[:-1].split('(')  # Bỏ dấu ')' cuối cùng và tách theo '('
            ten = part[0].strip()     # Tên vị từ
            cac_bien = part[1].split(',')  # Các tham số
            cac_bien = [b.strip() for b in cac_bien]  # Loại bỏ khoảng trắng
            logic_vitu.append([ten, cac_bien])
        ket_qua.append(logic_vitu)
    return ket_qua

# --- MAIN ---
# Phần chạy chính của chương trình
if __name__ == "__main__":
    # Dữ liệu đầu vào từ bài toán
    # Biểu diễn các mệnh đề trong logic vị từ
    # Mỗi mệnh đề được ngăn cách bởi dấu phẩy
    TAP_input = '-chame(x, y) v -chame(x, z) v anhem(y, z), \
                 -chame(x, y) v -chame(z, t) v -anhem(x, z) v anhem(y, t), \
                 -anhem(x, y) v anhem(y, x), \
                 chame(B, N), chame(T, D), chame(A, B), chame(A, T), -anhem(N, D)'
    
    # Danh sách các biến trong logic vị từ
    bien = ['x', 'y', 'z', 't']
    # Danh sách các hằng (giá trị cụ thể)
    giaTri = ['A', 'B', 'N', 'T', 'D']

    # Xử lý đầu vào chuyển từ chuỗi sang dạng danh sách vị từ
    TAP = xuLyDauVao(TAP_input)
    
    # Chạy thuật toán Robinson để chứng minh
    print("Bắt đầu giải thuật Robinson:")
    ket_qua = robinson(TAP, bien, giaTri)
    
    # In kết quả cuối cùng
    if ket_qua:
        print("\nKết luận: Mệnh đề đã được chứng minh là ĐÚNG.")
    else:
        print("\nKết luận: Không thể chứng minh mệnh đề.")