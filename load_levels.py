from sqlalchemy import create_engine, Table, MetaData, Column, String
import pandas as pd

DATABASE_URI = "sqlite:///levels_fyi.db"

engine = create_engine(
    DATABASE_URI,
    connect_args={"check_same_thread": False}
)

positions_df = pd.read_sql_query("""
select c.name company_name,
    p.name position,
    level ladder_level,
case instr(salary, 'k')
when 0 then cast(replace(replace(salary, '$', ''), 'm', '') as decimal) * 1000
else cast(replace(replace(salary, '$', ''), 'k', '') as decimal)
end salary
from position p
inner join salary s on p.id = s.position
inner join company c on p.company = c.id
order by 4 desc
""", engine)

benefits_df = pd.read_sql_query("""
select c.name company_name, b.name benefit
from benefit b
inner join company c on b.company = c.id
""", engine)

