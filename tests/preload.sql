INSERT INTO device (name, description) VALUES ('name1', 'description1');
INSERT INTO user (role_id, username, password) VALUES (2, 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');
INSERT INTO task (name, command, device_id) VALUES ('name1', 'echo, hello world', 1);
