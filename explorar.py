import duckdb
con = duckdb.connect("data/berka.duckdb", read_only=True)

consulta = """
    with cte as (SELECT account_id, strptime(CAST(date AS VARCHAR), '%y%m%d') as date, type, balance, (ROW_NUMBER() OVER 
    (PARTITION BY account_id ORDER BY date desc, trans_id desc) )as nro_trans
    FROM trans
    where year(strptime(CAST(date AS VARCHAR), '%y%m%d')) = 1997)

   ,cte1 as(select  account_id, date, type, balance from cte
    where nro_trans =1 
    order by account_id asc)

    select a.account_id
    from account a
    where not exists (
    select 1 from cte1 c
    where c.account_id = a.account_id
)
"""

consulta3 = """
    SELECT COUNT(*) FROM (
  SELECT account_id FROM trans
  WHERE date = 971231
  GROUP BY account_id HAVING COUNT(*) > 1
);
"""

consulta4 = """
    SELECT account_id, MIN(date) AS primera, MAX(date) AS ultima, COUNT(*) AS movimientos
FROM trans
WHERE account_id IN (138, 799, 1720, 2029)
GROUP BY account_id;
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

consulta5 = """   
        SELECT account_id, date FROM account
WHERE account_id IN (138, 799, 1720, 2029);


"""

types = """   
        select distinct(type) from trans

"""


query1 = """   
        select  count(distinct client_id) from card c right join disp d
        on c.disp_id = d.disp_id
        where c.disp_id is null and d.type ='OWNER'


"""
#select count (*) from cte_2
#        where ABS(balance - saldo_esperado) > 0.01
con.sql(query1).show()
con.close()