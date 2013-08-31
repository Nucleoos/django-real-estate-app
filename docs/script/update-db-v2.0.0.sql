﻿INSERT INTO real_estate_app_apps_propertys_position_of_sun SELECT id, logical_exclude, logical_exclude, date(now()), position from real_estate_app_positionofsun;
INSERT INTO real_estate_app_apps_propertys_aditionalthings SELECT id, logical_exclude, logical_exclude, date(now()), name from real_estate_app_aditionalthings;
INSERT INTO real_estate_app_apps_propertys_property_aditionalthings_fk SELECT id, property_id, aditionalthings_id from real_estate_app_property_aditionalthings_fk; 
INSERT INTO real_estate_app_apps_propertys_classification SELECT id, logical_exclude, logical_exclude, date(now()), classification from real_estate_app_classification;
INSERT INTO real_estate_app_apps_propertys_district SELECT id, logical_exclude, logical_exclude, date(now()), district, state from real_estate_app_district;
INSERT INTO real_estate_app_apps_propertys_status_property SELECT id, logical_exclude, logical_exclude, date(now()), statusproperty FROM real_estate_app_statusproperty; 
INSERT INTO real_estate_app_apps_propertys_property (id, address, slug, zip_code, price, district_fk_id, condominio, iptu, classification_fk_id, statusproperty_fk_id, state,rooms, baths, garage, elevator,  furnishing, featured,  under_contruction, private_area,  position_of_sun_id,pub_date, pub_date_end, description, enable_publish, gmap_point_x, gmap_point_y, code_property,create_date, logical_exclude ) select id, address, slug, zip_code, price, district_fk_id, condominio, iptu, classification_fk_id, statusproperty_fk_id, state,rooms, baths, garage, elevator,  furnishing, featured,  under_contruction, private_area,  position_of_sun_id,date_init, date_end, description, enable_publish, gmap_point_x, gmap_point_y, code_property, date(now()), false from real_estate_app_property;
INSERT INTO real_estate_app_apps_propertys_property_domain SELECT id, property_id, site_id from real_estate_app_property_domain;
INSERT INTO real_estate_app_apps_photos_photo SELECT id , false, is_published, date(now()), album_id, photo,  width, height, slug, description, pub_date, image_destaque from real_estate_app_photo;
INSERT INTO real_estate_app_apps_newspapers_news (id, title,slug, pub_date, enable_publish, create_date,logical_exclude,content) select id,title, slug, pub_date, enable_publish, date(now()),false, content  from real_estate_app_news;
INSERT INTO real_estate_app_apps_real_estate_files_files (id, title, slug, pub_date, enable_publish , create_date, logical_exclude , files) SELECT id,title,slug,pub_date, false, date(now()), false, files FROM real_estate_app_files;
INSERT INTO real_estate_app_apps_real_estate_files_files SELECT file.id, img.slug, img.slug||file.id, img.pub_date, img.pub_date, false, date(now()), false, img.images FROM real_estate_app_images img, (SELECT max(id)+1 as id FROM real_estate_app_apps_real_estate_files_files) as file;
INSERT INTO real_estate_app_apps_marketing_marketing SELECT ppi.id, ppi.title, ppi.slug, ppi.date_init, ppi.date_end, ppi.enable_published , date(now()), false, ppi.description, img.portletpropagandaimage_id FROM real_estate_app_portletpropagandaimage ppi LEFT JOIN real_estate_app_images img ON img.portletpropagandaimage_id = ppi.id;
create table tmp_mgr_protlet_types (before varchar(50),new varchar(50));
insert into tmp_mgr_protlet_types values ('news','newspapers.News');
insert into tmp_mgr_protlet_types values ('images','marketing.MarketingObject');
insert into real_estate_app_apps_portlets_portlet (id, title,slug, pub_date, enable_publish, create_date, logical_exclude, featured, amount_featured, type_portlet) select id, title,title, date(now()),true,date(now()),false,featured_id, amount_featured, pt.new from real_estate_app_portlet p inner join tmp_mgr_protlet_types pt ON p.type_portlet = pt.before where type_portlet in ('news','images');
/* PUT SEQUENCES O NEXT VALUE FROM IDs */
SELECT setval('real_estate_app_apps_photos_photo_id_seq', (select max(id)+1 from real_estate_app_apps_photos_photo));
SELECT setval('real_estate_app_apps_portlets_portlet_id_seq', (select max(id)+1 from real_estate_app_apps_portlets_portlet));
SELECT setval('real_estate_app_apps_propertys_classification_id_seq', (select max(id)+1 from real_estate_app_apps_propertys_classification));
SELECT setval('real_estate_app_apps_propertys_district_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_district));
SELECT setval('real_estate_app_apps_propertys_position_of_sun_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_position_of_sun));
SELECT setval('real_estate_app_apps_propertys_property_domain_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_property_domain));
SELECT setval('real_estate_app_apps_propertys_property_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_property));
SELECT setval('real_estate_app_apps_propertys_property_realtor_fk_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_property_realtor_fk));
SELECT setval('real_estate_app_apps_propertys_status_property_id_seq',(select max(id)+1 from real_estate_app_apps_propertys_status_property));
SELECT setval('real_estate_app_apps_realtors_realtor_id_seq',(select max(id)+1 from real_estate_app_apps_realtors_realtor));
SELECT setval('real_estate_app_apps_real_estate_files_files_id_seq',(select max(id)+1 from real_estate_app_apps_real_estate_files_files));
SELECT setval('real_estate_app_apps_propertys_aditionalthings_id_seq', (select max(id)+1 from real_estate_app_apps_propertys_aditionalthings));
drop table tmp_mgr_protlet_types;