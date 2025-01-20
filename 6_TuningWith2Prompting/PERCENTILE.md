xài: 
```bash
=PERCENTILE(FILTER(C:C, (A:A="RoleB") * (C:C>0)), 0.5)
```


----

1. Hàm PERCENTILE
- Hàm PERCENTILE.INC (Bao gồm biên)
```
=PERCENTILE.INC(range, k)
```

- Hàm PERCENTILE.EXC (Bỏ biên)
```
=PERCENTILE.EXC(range, k)
```
2. Thêm range:

```bash
=PERCENTILE.INC(FILTER(C:C, A:A="RoleB"), k)
```


FILTER(C:C, A:A="RoleB"): Lấy các giá trị từ cột C mà cột A là RoleB.
k: Percentile cần tính (ví dụ, 0.5 cho 50%).

3. Thêm điều kiện: các giá trị > 0 
```
=FILTER(C:C, (A:A="RoleB")*(C:C>0))
```


```
=PERCENTILE.INC(FILTER(C:C, (A:A="RoleB")*(C:C>0)), k)
```


4. Trên lark: 

```bash
=FILTER(C:C, (A:A="RoleB") * (C:C>0))
```
- Giá trị trả ra sẽ là 1 cột chứa các giá trị mình muốn, cơ mà nó bị lệch dòng với giá trị ban đầu. 

```bash
=PERCENTILE(FILTER(C:C, (A:A="RoleB") * (C:C>0)), 0.5)
```


5. Cách khác: 

```bash
=IF(AND(A2="RoleB", C2>0), C2, "")
```
