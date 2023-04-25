---------------------------------
-- Script de insertado para valores de prueba
---------------------------------
INSERT INTO strain (strain_name, strain_type, strain_year, strain_thc, strain_cbd, strain_description, strain_effects, strain_flavors) VALUES 
('OG Kush', 'Hibrida', '1998','26','0.3','OG Kush es una variedad de marihuana híbrida con predominancia índica. Se originó en California a finales de la década de 1990 y rápidamente se convirtió en una de las cepas más populares en el mercado.','Relajacion Profunda,Euforia,Sedante','Terroso,Especiado'),
('Sour Diesel', 'Sativa', '2001','25','0.2','Sour Diesel es una cepa de marihuana sativa que se cree que es el resultado del cruce entre las variedades Super Skunk y Chemdawg 91. Es conocida por su aroma distintivo y sus efectos energizantes y eufóricos.','Euforia,Energizado','Picante,Citrico'),
('Northen Lights', 'Indica', '1976','21','0.1','Northern Lights es una variedad de marihuana índica que se originó en los años 70 en Estados Unidos, aunque se ha cruzado y cultivado en diferentes partes del mundo. Es conocida por su alto rendimiento y su efecto relajante y sedante.','Sedante,Relajacion Profunda','Dulce,Terroso,Especiado'),
('Girl Scout Cookies', 'Hibrida', '2010','28','0.2','Girl Scout Cookies es una cepa de marihuana híbrida que se cree que es el resultado del cruce entre las variedades Durban Poison y OG Kush. Es conocida por su sabor dulce y terroso y sus efectos relajantes y eufóricos.','Relajacion,Euforia,Estimulante','Dulce,Terroso,Amaderado'),
('White Widow', 'Hibrida', '1990','20','0.2','White Widow es una variedad de marihuana híbrida que se originó en los Países Bajos en la década de 1990. Es conocida por su alto contenido de THC y sus efectos eufóricos y relajantes.','Euforia,Relajacion','Afrutado,Floral'),
('Blue Dream', 'Hibrida', '2003','22','0.2','Blue Dream es una cepa de marihuana híbrida que se cree que es el resultado del cruce entre las variedades Blueberry y Haze. Es conocida por su sabor dulce y afrutado y sus efectos relajantes y eufóricos.','Relajacion,Euforia,Estimulante','Dulce,Afrutado'),
('Granddaddy Purple', 'Indica', '2003','23','0.1','Granddaddy Purple es una cepa de marihuana índica que se cree que es el resultado del cruce entre las variedades Purple Urkle y Big Bud. Es conocida por su sabor dulce y afrutado y sus efectos sedantes y relajantes.','Sedante,Relajacion Profunda','Dulce,Uva');

INSERT INTO creator (creators_name, creators_country, creators_mail, creators_phone, creators_license, creators_strain, creators_lab) VALUES 
('John Doe', 'Estados Unidos', 'johndoe@gmail.com', '15551234', '923845720356', '1', '10'),
('Jane Smith', 'Canadá', 'janesmith@hotmail.com', '15555678', '563291847632', '2', '9'),
('Juan Pérez', 'México', 'jperez@yahoo.com', '52554321', '209483615937', '3', '8'),
('Maria García', 'España', 'mgarcia@gmail.com', '34918765', '178452936082', '4', '7'),
('Robert Johnson', 'Reino Unido', 'rjohnson@hotmail.com', '44201234', '643521890365', '1', '6'),
('Hans Schmidt', 'Alemania', 'hschmidt@yahoo.com', '49305678', '901287345612', '2', '5'),
('Yuri Kim', 'Corea del Sur', 'ykim@gmail.com', '8221234', '435210986732', '3', '4'),
('Chen Wei', 'China', 'cwei@hotmail.com', '86105678', '769041532810', '1', '3'),
('Taro Yamada', 'Japón', 'tyamada@yahoo.co.jp', '8131234', '314275890216', '2', '2'),
('Muhammed Ali', 'Egipto', 'mali@gmail.com', '2025678', '695721834210', '3', '1');


INSERT INTO dispensary (dispensary_name, dispensary_state, dispensary_city, dispensary_address, dispensary_phone, dispensary_mail) 
VALUES 
('Green Hope', 'California', 'Los Angeles', '123 Main St', '5551234', 'info@greenhope.com'),
('Ganja Queen', 'Nevada', 'Las Vegas', '456 Broadway', '5555678', 'sales@ganjaqueen.com'),
('High Life', 'Colorado', 'Denver', '789 Oak St', '5559012', 'customerservice@highlife.com'),
('420 Emporium', 'Washington', 'Seattle', '234 Pine St', '5553456', 'support@420emporium.com'),
('Cannabis Connection', 'Oregon', 'Portland', '567 Elm St', '5557890', 'info@cannabisconnection.com'),
('The Green Joint', 'Colorado', 'Grand Junction', '901 Cherry Ave', '5552345', 'info@thegreenjoint.com'),
('Mellow Meadows', 'Arizona', 'Phoenix', '345 Oak St', '5556789', 'sales@mellowmeadows.com'),
('Bud Haven', 'California', 'San Francisco', '678 Pine St', '5550123', 'info@budhaven.com'),
('Pot Palace', 'Nevada', 'Reno', '901 Broadway', '5554567', 'support@potpalace.com'),
('High Society', 'Oregon', 'Eugene', '234 Main St', '5558901', 'customerservice@highsociety.com');


INSERT INTO award (awards_name, awards_date, awards_entity, awards_winner)
VALUES
('Cannabis Cup', '2020-01-01', 'High Times', '3'),
('420 Awards', '2020-02-15', 'Weedmaps', '2'),
('The Emerald Cup', '2020-03-30', 'The Emerald Cup', '1'),
('MJBizCon Awards', '2020-05-01', 'MJBizCon', '4'),
('Spannabis Champions Cup', '2020-06-15', 'Spannabis', '2'),
('Highlife Cup', '2020-08-01', 'Highlife Cup','1'),
('The Karma Cup', '2020-09-30', 'The Karma Cup', '3'),
('Chalice Festival Awards', '2020-11-15', 'Chalice Festival', '3'),
('Cannabis Business Awards', '2020-12-01', 'Cannabis Business Awards', '1'),
('The Emerald Cup', '2021-03-30', 'The Emerald Cup','1');

INSERT INTO concentrate (concentrate_name, concentrate_strain, concentrate_thc, concentrate_cbd, concentrate_dose, concentrate_type, concentrate_effects, concentrate_flavors, concentrate_description)
VALUES
('Cristales de CBD', '1', '0.1', '79.9', '20', 'Cristales', 'Relajante, analgésico, antiinflamatorio', 'Cítricos, dulce, pino', 'Los cristales de CBD se obtienen a partir de cáñamo orgánico y son ideales para añadir a alimentos, bebidas y productos para el cuidado personal.'),
('Aceite de CBD', '1', '0.2', '70', '10', 'Aceite', 'Alivio del dolor, reducción de la ansiedad, mejora del sueño', 'Dulce, terroso, picante', 'El aceite de CBD se obtiene a partir de plantas de cáñamo orgánico y se puede tomar directamente o mezclado con alimentos y bebidas.'),
('BHO', '2', '76', '1', '50', 'BHO', 'Euforia, relajación, sedación', 'Dulce, pino, terroso', 'El BHO es un concentrado de cannabis que se obtiene mediante extracción con butano y tiene un alto contenido de THC.'),
('Wax', '2', '74', '2', '30', 'Wax', 'Euforia, creatividad, relajación', 'Dulce, terroso, cítricos', 'El wax es un concentrado de cannabis que se obtiene mediante extracción con butano y tiene una textura similar a la cera.'),
('Rosin', '3', '78', '1', '40', 'Rosin', 'Euforia, relajación, sedación', 'Dulce, pino, terroso', 'El rosin es un concentrado de cannabis que se obtiene mediante la aplicación de presión y calor a las flores de cannabis.'),
('Kief', '4', '60', '1', '20', 'Kief', 'Euforia, estimulación, creatividad', 'Dulce, cítricos, picante', 'El kief es un concentrado de cannabis que se obtiene a partir de las glándulas de tricomas de las flores de cannabis.'),
('Live Resin', '3', '70', '1', '30', 'Live Resin', 'Euforia, relajación, sedación', 'Dulce, terroso, cítricos', 'El live resin es un concentrado de cannabis que se obtiene mediante extracción con solventes de flores frescas y congeladas de cannabis.'),
('Cristales de THC', '4', '99', '0.1', '10', 'Cristales', 'Euforia, relajación, sedación', 'Dulce, terroso, pino', 'Los cristales de cannabis son un tipo de concentrado de cannabis que se caracteriza por su alto contenido de THC');

