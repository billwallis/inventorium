drop table if exists stores;
drop table if exists products;
drop table if exists inventory;

drop trigger if exists stores__update_updated_ts;
drop trigger if exists products__update_updated_ts;
drop trigger if exists inventory__update_updated_ts;
