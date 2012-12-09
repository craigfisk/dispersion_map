
-- recent shipments, with ipaddress_id
select ms.id, dt, msi.ipaddress_id from myfruitcake_shipment ms left join myfruitcake_shipment_ipaddresses msi on msi.shipment_id = ms.id order by dt desc limit 10;

-- recent shipments, with ipaddresses, cities, regions, countries [note the left joins]
select ms.id, dt, au.username, au.email, msi.ipaddress_id, mi.ipaddress, mi.city, mi.region, mi.country from myfruitcake_shipment ms left join myfruitcake_shipment_ipaddresses msi on msi.shipment_id = ms.id join auth_user au on au.id = ms.sender_id left join myfruitcake_ipaddress mi on mi.id = msi.ipaddress_id order by dt desc limit 10;

