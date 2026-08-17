create table stores (
    store_id integer not null primary key,
    store_name text not null unique,

    created_ts text default current_timestamp,
    updated_ts text default current_timestamp,
    deleted integer default false
) strict;
create trigger stores__update_updated_ts
after update on stores
begin
    update stores
    set updated_ts = current_timestamp
    where store_id = new.store_id;
end;


create table products (
    product_id integer not null primary key,
    product_name text not null unique,

    created_ts text default current_timestamp,
    updated_ts text default current_timestamp,
    deleted integer default false
) strict;
create trigger products__update_updated_ts
after update on products
begin
    update products
    set updated_ts = current_timestamp
    where product_id = new.product_id;
end;


create table inventory (
    store_id integer not null references stores (store_id),
    product_id text not null references products (product_id),

    in_stock integer not null check (in_stock >= 0),

    created_ts text default current_timestamp,
    updated_ts text default current_timestamp,
    deleted integer default false,

    primary key (store_id, product_id)
) strict;
create trigger inventory__update_updated_ts
after update on inventory
begin
    update inventory
    set updated_ts = current_timestamp
    where 1=1
        and store_id = new.store_id
        and product_id = new.product_id
    ;
end;
