
c1 = '''
    select cd.macd, cd.diem
    from chuyen_di cd
    where cd.diem >= 4.5
'''
c2 = '''
    select dx.madx, dx.ddi, dx.dden, dx.tgdat
    from dat_xe dx 
    join kh k on dx.makh = k.makh
    where k.hoten like 'Nguyen Van A'
'''
c3 = '''
    select dx.madx, dx.matx, tx.hoten, tx.sdt, dx.tgbdau, dx.tgkthuc, dx.kqua
    from doi_xe dx 
    join tai_xe tx on dx.matx = tx.matx
    where tx.matx = 'TX005' and dx.kqua = 'TAI XE HUY'
'''
c4 = '''
    select k.makh, k.hoten, k.sdt, count(dx2.makh) as slcd 
    from chuyen_di cd
    join doi_xe dx on cd.madx = dx.madx 
    join dat_xe dx2 on dx.madx = dx2.madx
    join kh k on dx2.makh = k.makh
    where cd.gia >= 400000 and cd.htttoan = 'VIETCOMBANK'
    group by dx2.makh
    order by count(dx2.makh) asc
'''
c5 = '''
    select k.makh, k.hoten, k.sdt
    from kh k 
    join dat_xe dx on k.makh = dx.makh 
    join doi_xe dx2 on dx.madx = dx2.madx 
    join chuyen_di cd on dx2.madx = cd.madx
    group by k.makh
    having count(distinct cd.htttoan) = 1 and cd.htttoan = 'VIETCOMBANK'
'''
c6 = '''
        select k.makh, k.hoten, k.sdt
    from kh k 
    join dat_xe dx on k.makh = dx.makh 
    join doi_xe dx2 on dx.madx = dx2.madx 
    join chuyen_di cd on dx2.madx = cd.madx
    group by k.makh
    having count(distinct cd.htttoan) = 2 and cd.htttoan in ('VIETCOMBANK', 'TIEN MAT')
'''
c7 = '''
    select k.makh
    from kh k 
    join dat_xe dx on k.makh = dx.makh 
    group by k.makh
    having count(distinct dx.lxe) = (
        select count (distinct dx.lxe)
        from dat_xe dx
    )
'''

queries = [c1, c2, c3, c4, c5, c6, c7]
schemas = [
    ["MACD", "DIEM"],
    ["MADX", "DDI", "DDEN", "TGDAT"],
    ["MADX", "MATX", "HOTEN", "SDT", "TGBDAU", "TGKTHUC", "KQUA"],
    ["MAKH", "HOTEN", "SDT", "SLCD"],
    ["MAKH", "HOTEN", "SDT"],
    ["MAKH", "HOTEN", "SDT"],
    ["MAKH"]
]