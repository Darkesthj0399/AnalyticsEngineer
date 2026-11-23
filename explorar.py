import duckdb
con = duckdb.connect("data/berka.duckdb", read_only=True)

consulta = """
    with cte as (SELECT account_id, date, type, amount, (ROW_NUMBER() OVER 
    (PARTITION BY account_id ORDER BY date asc, trans_id asc) )as nro_trans
    FROM trans)

    select  account_id, date, type, amount from cte
    where nro_trans =1 and account_id =576
    order by account_id asc
"""

consulta1 = """
    select  account_id, date, type, amount from trans
    where account_id =576
    order by date asc
    limit 3
"""

tipo = """
     with cte as (SELECT account_id, date, type, amount, (ROW_NUMBER() OVER 
        (PARTITION BY account_id ORDER BY date asc, trans_id asc) )as nro_trans
        FROM trans)
    
        select  type, COUNT(*) from cte
        where nro_trans=1
        group by type
"""

lag1 = """   
        with cte as(select account_id, trans_id, date, type, amount, balance, LAG(balance) OVER (partition by account_id order by date asc, trans_id asc) as saldo_anterior from trans)

        ,cte_2 as(select *, case when type = 'PRIJEM' then saldo_anterior + amount when type in ('VYDAJ','VYBER') then saldo_anterior - amount else null end as saldo_esperado from cte)

        select count(*) as cantidad, sum(case when saldo_anterior is null then 1 else 0 end) as no_conciliables, sum( case when ABS(balance - saldo_esperado) > 0.01 then 1 else 0 end) as fallan,
         SUM(CASE WHEN type not in ('PRIJEM','VYDAJ','VYBER') THEN 1 ELSE 0 END) as tipos_desconocidos   from cte_2


"""


types = """   
        select distinct(type) from trans

"""
#select count (*) from cte_2
#        where ABS(balance - saldo_esperado) > 0.01
con.sql(lag1).show()
con.close()